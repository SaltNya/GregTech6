"""Launch a distribution jar against an installed loader in a fresh workspace instance.

The installed launcher files, mods and assets are read only. A separate test mod
captures the actual title screen and exits; it is not part of the GT distribution.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import uuid
import zipfile

from verify_client_smoke import check_png


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def allowed(rules):
    if not rules:
        return True
    enabled = False
    for rule in rules:
        system = rule.get('os', {})
        if system.get('name', 'windows') != 'windows':
            continue
        if system.get('arch', 'x86_64') not in ('x86_64', 'amd64'):
            continue
        if 'version' in system:
            windows = sys.getwindowsversion()
            if not re.search(system['version'], f'{windows.major}.{windows.minor}.{windows.build}'):
                continue
        features = rule.get('features', {})
        if any(value != (key == 'has_custom_resolution') for key, value in features.items()):
            continue
        enabled = rule['action'] == 'allow'
    return enabled


def arguments(values, replacements):
    result = []
    for value in values:
        if isinstance(value, dict):
            if not allowed(value.get('rules')):
                continue
            value = value['value']
        for argument in (value if isinstance(value, list) else [value]):
            for key, replacement in replacements.items():
                argument = argument.replace('${' + key + '}', replacement)
            if '${' in argument:
                raise ValueError(f'Unresolved launcher argument: {argument}')
            result.append(argument)
    return result


def launch(args):
    root = args.minecraft_root.resolve()
    installed = root / 'versions' / args.version
    descriptor = installed / (args.version + '.json')
    version = json.loads(descriptor.read_text(encoding='utf-8-sig'))
    if version.get('inheritsFrom'):
        raise ValueError('Use a complete installed version JSON, not an inherited descriptor')
    workspace = Path(__file__).resolve().parents[2]
    run = workspace / 'build/production-smoke' / (args.platform + '-' + str(uuid.uuid4()))
    run.mkdir(parents=True)
    mods = run / 'mods'
    natives = run / 'natives'
    mods.mkdir()
    natives.mkdir()
    mod_records = []
    for source in [args.jar, args.probe, *sorted((installed / 'mods').glob('*.jar'))]:
        if source.parent.resolve() == (installed / 'mods').resolve() and source.name.startswith('gregtech'):
            continue
        with zipfile.ZipFile(source) as archive:
            bad = archive.testzip()
            if bad:
                raise ValueError(f'Corrupt mod: {source}: {bad}')
            if source.resolve() == args.probe.resolve():
                names = archive.namelist()
                if (any('refmap' in name or name == 'gregtech.mixins.json' for name in names)
                        or b'MixinConfigs' in archive.read('META-INF/MANIFEST.MF')):
                    raise ValueError('The startup probe must not supply production Mixin mappings')
        destination = mods / source.name
        if destination.exists():
            raise ValueError(f'Duplicate mod name: {source.name}')
        shutil.copyfile(source, destination)
        mod_records.append({'name': source.name, 'sha256': sha(destination), 'bytes': destination.stat().st_size})
    classpath = []
    libraries = root / 'libraries'
    for library in version['libraries']:
        if not allowed(library.get('rules')):
            continue
        downloads = library.get('downloads', {})
        artifact = downloads.get('artifact')
        if artifact is None:
            group, name, release, *classifier = library['name'].split(':')
            suffix = '-' + classifier[0] if classifier else ''
            artifact = {'path': f'{group.replace(".", "/")}/{name}/{release}/{name}-{release}{suffix}.jar'}
        path = libraries / artifact['path']
        if not path.is_file():
            raise ValueError(f'Missing installed library: {path}')
        classpath.append(str(path))
        native_name = library.get('natives', {}).get('windows')
        native_path = path
        if native_name:
            native_name = native_name.replace('${arch}', '64')
            native_path = libraries / downloads['classifiers'][native_name]['path']
        with zipfile.ZipFile(native_path) as archive:
            for entry in archive.infolist():
                if entry.filename.lower().endswith('.dll'):
                    destination = natives / Path(entry.filename).name
                    destination.write_bytes(archive.read(entry))
    client = installed / (args.version + '.jar')
    if not client.is_file():
        raise ValueError(f'Missing installed client jar: {client}')
    classpath.append(str(client))
    # Launcher JSONs can repeat an inherited library; PCL also deduplicates these.
    classpath = list(dict.fromkeys(classpath))
    (run / 'options.txt').write_text(
        'onboardAccessibility:false\npauseOnLostFocus:false\nmaxFps:60\nrenderDistance:4\n'
        'simulationDistance:5\nsoundCategory_master:0.0\nfullscreen:false\n', encoding='utf-8')
    replacements = {
        'natives_directory': str(natives), 'launcher_name': 'GTDeliveryCheck', 'launcher_version': '1',
        'classpath': os.pathsep.join(classpath), 'classpath_separator': os.pathsep,
        'library_directory': str(libraries), 'version_name': args.version,
        'auth_player_name': 'GTDeliveryCheck', 'game_directory': str(run),
        'assets_root': str(root / 'assets'), 'assets_index_name': version['assetIndex']['id'],
        'auth_uuid': '00000000000000000000000000000001', 'auth_access_token': '0',
        'clientid': '0', 'auth_xuid': '0', 'user_type': 'legacy', 'version_type': 'delivery-check',
        'resolution_width': '1280', 'resolution_height': '720',
    }
    java_args = ['-Xmx4G', '-Dfile.encoding=UTF-8', *arguments(version['arguments']['jvm'], replacements),
                 version['mainClass'], *arguments(version['arguments']['game'], replacements)]
    argument_file = run / 'java-arguments.txt'
    argument_file.write_text('\n'.join('"' + a.replace('\\', '\\\\').replace('"', '\\"') + '"'
                                       for a in java_args) + '\n', encoding='utf-8')
    log = run / 'launch.log'
    command = [str(args.java.resolve()), *java_args]
    if len(subprocess.list2cmdline(command)) >= 30000:
        # Windows' native Java launcher reads argument files in the ANSI code page,
        # even when the VM itself uses UTF-8. Direct Unicode argv avoids that issue.
        argument_file.write_text(argument_file.read_text(encoding='utf-8'), encoding='mbcs')
        command = [str(args.java.resolve()), '@' + str(argument_file)]
    print(f'Starting production {args.platform} {args.version}; isolated log: {log}', flush=True)
    started = time.monotonic()
    with log.open('wb') as output:
        process = subprocess.Popen(command, cwd=run,
                                   stdout=output, stderr=subprocess.STDOUT,
                                   creationflags=subprocess.CREATE_NO_WINDOW)
        try:
            exit_code = process.wait(timeout=args.timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
            raise ValueError(f'Production client timed out; see {log}')
    text = log.read_text(encoding='utf-8', errors='replace')
    for marker in ('PRODUCTION_SMOKE_FAILED', 'Mixin apply failed', 'MixinTransformerError',
                   'zip END header not found', 'Failed to initialize the mod loading system'):
        if marker in text:
            raise ValueError(f'Production client failure: {marker}; see {log}')
    receipts = re.findall(r'PRODUCTION_SMOKE_SUCCESS (\{[^\r\n]+\})', text)
    if exit_code != 0 or len(receipts) != 1:
        raise ValueError(f'Production client exit={exit_code}, success receipts={len(receipts)}; see {log}')
    receipt = json.loads(receipts[0])
    screenshot = Path(receipt['screenshot'])
    if (receipt['platform'] != args.platform or receipt['screen'] != 'net.minecraft.client.gui.screens.TitleScreen'
            or receipt['renderedFrames'] < 5 or screenshot.resolve().parent != (run / 'screenshots').resolve()):
        raise ValueError('Production title-screen receipt is incomplete')
    surface = receipt.get('surfaceChecks', {})
    if (surface.get('surfaceItemModelsChecked') != 16
            or surface.get('surfaceSpringSpritesChecked') != 7
            or surface.get('surfaceBerryStageColorsChecked') != 36
            or len(surface.get('surfaceItems', [])) != 16
            or surface.get('machineModelsChecked') != 6
            or len(surface.get('machineItems', [])) != 6):
        raise ValueError('Production surface mesh/color receipt is incomplete')
    dimensions = check_png(screenshot.read_bytes())
    if dimensions != (receipt['width'], receipt['height']):
        raise ValueError('Production screenshot dimensions differ from receipt')
    for source in (args.jar, args.probe):
        copied = next(record for record in mod_records if record['name'] == source.name)
        if sha(source) != copied['sha256']:
            raise ValueError(f'{source} changed during the production check')
    result = {'status': 'passed', 'scope': 'Actual distribution jar in isolated installed-loader client; title screen only',
              'platform': args.platform, 'version': args.version, 'java': str(args.java.resolve()),
              'java_version': subprocess.check_output([str(args.java), '-version'], stderr=subprocess.STDOUT, text=True).strip(),
              'exit_code': exit_code, 'elapsed_seconds': round(time.monotonic() - started, 2),
              'installed_files_modified': False, 'version_json_sha256': sha(descriptor),
              'distribution': {'path': str(args.jar.resolve()), 'sha256': sha(args.jar)},
              'probe': {'path': str(args.probe.resolve()), 'sha256': sha(args.probe)},
              'mods': mod_records, 'log': str(log), 'log_sha256': sha(log), 'receipt': receipt,
              'screenshot_sha256': sha(screenshot), 'visually_reviewed': False}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Production {args.platform} title-screen check passed: {dimensions}; {args.output}', flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--platform', required=True, choices=('forge', 'neoforge'))
    parser.add_argument('--minecraft-root', required=True, type=Path)
    parser.add_argument('--version', required=True)
    parser.add_argument('--java', required=True, type=Path)
    parser.add_argument('--jar', required=True, type=Path)
    parser.add_argument('--probe', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--timeout', type=int, default=360)
    args = parser.parse_args()
    try:
        launch(args)
    except (OSError, ValueError, KeyError, zipfile.BadZipFile) as error:
        parser.exit(1, f'Production check failed: {error}\n')


if __name__ == '__main__':
    main()
