"""Validate one development-client smoke receipt; Python 3.10+.

PNG/log evidence does not prove that the menu looks correct or that gameplay works.
Pillow is required for a complete image-decode check; it is never installed implicitly.
"""

import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import sys
import tempfile
import uuid
import zlib


VERSIONS = {'forge': '1.20.1', 'neoforge': '1.21.1'}
MARKER = re.compile(r'\bCLIENT_SMOKE_(STARTED|SUCCESS|FAILED)\b')
ANSI = re.compile(r'\x1b\[[0-?]*[ -/]*[@-~]')
PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'
TITLE_SCREEN = 'net.minecraft.client.gui.screens.TitleScreen'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def integer(value):
    return isinstance(value, int) and not isinstance(value, bool)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f'Duplicate JSON receipt key: {key}')
        result[key] = value
    return result


def decode_log(raw):
    # PowerShell logs may use UTF-16; neither replacement nor ignored bytes are evidence.
    if raw.startswith((b'\xff\xfe', b'\xfe\xff')):
        return raw.decode('utf-16')
    return raw.decode('utf-8-sig')


def parse_run(text, platform, exit_code):
    require(exit_code == 0, f'Game/Gradle exit code is {exit_code}, expected 0')
    receipts = {'STARTED': [], 'SUCCESS': [], 'FAILED': []}
    build_success_lines = []
    for line_number, raw_line in enumerate(text.splitlines(), 1):
        line = ANSI.sub('', raw_line)
        if re.search(r'\bBUILD SUCCESSFUL\b', line):
            build_success_lines.append(line_number)
        markers = list(MARKER.finditer(line))
        require(len(markers) <= 1, f'Multiple smoke markers on line {line_number}')
        for match in markers:
            phase = match.group(1)
            # A FAILED marker is disqualifying even if its following JSON is malformed.
            if phase == 'FAILED':
                receipts[phase].append((line_number, None))
                continue
            try:
                receipt = json.loads(line[match.end():].strip(),
                                     object_pairs_hook=unique_object)
            except (ValueError, TypeError) as error:
                raise ValueError(f'Invalid {phase} JSON on line {line_number}: {error}') from error
            require(isinstance(receipt, dict), f'{phase} receipt must be a JSON object')
            receipts[phase].append((line_number, receipt))
    require(not receipts['FAILED'], 'CLIENT_SMOKE_FAILED is present')
    for phase in ('STARTED', 'SUCCESS'):
        require(len(receipts[phase]) == 1,
                f'Expected exactly one CLIENT_SMOKE_{phase}, found {len(receipts[phase])}')
    start_line, started = receipts['STARTED'][0]
    success_line, success = receipts['SUCCESS'][0]
    require(start_line < success_line, 'SUCCESS precedes STARTED')
    require(any(line > success_line for line in build_success_lines),
            'No BUILD SUCCESSFUL after the screenshot success')
    for phase, receipt in (('STARTED', started), ('SUCCESS', success)):
        require(receipt.get('platform') == platform, f'{phase} platform does not match {platform}')
        require(receipt.get('minecraft') == VERSIONS[platform],
                f'{phase} Minecraft version does not match {VERSIONS[platform]}')
        elapsed = receipt.get('elapsedMs')
        require(integer(elapsed) and elapsed >= 0, f'{phase} elapsedMs must be a nonnegative integer')
    require(success['elapsedMs'] > 0 and success['elapsedMs'] >= started['elapsedMs'],
            'SUCCESS elapsedMs must be positive and at least STARTED elapsedMs')
    require(integer(success.get('renderedFrames')) and success['renderedFrames'] >= 5,
            'SUCCESS must contain at least five rendered frames')
    require(success.get('screen') == TITLE_SCREEN, 'SUCCESS screen is not the actual TitleScreen class')
    for key in ('width', 'height'):
        require(integer(success.get(key)) and success[key] > 0,
                f'SUCCESS {key} must be a positive integer')
    screenshot = success.get('screenshot')
    require(isinstance(screenshot, str) and screenshot, 'SUCCESS screenshot path is missing')
    path = Path(screenshot)
    require(path.is_absolute(), 'SUCCESS screenshot path must be absolute')
    pattern = (r'gregtech-client-smoke-' + re.escape(platform) + '-' +
               re.escape(VERSIONS[platform]) + r'-([0-9a-f-]{36})\.png')
    match = re.fullmatch(pattern, path.name)
    require(match is not None, 'Screenshot name has no current platform/version/UUID PNG receipt')
    run_uuid = uuid.UUID(match.group(1))
    require(str(run_uuid) == match.group(1) and run_uuid.version == 4,
            'Screenshot token must be a canonical random UUID version 4')
    return started, success, path, str(run_uuid)


def check_png(data):
    require(data.startswith(PNG_SIGNATURE), 'Screenshot has no PNG signature')
    offset, chunks, dimensions, has_idat = 8, 0, None, False
    while offset < len(data):
        require(offset + 12 <= len(data), 'Truncated PNG chunk header/CRC')
        length = struct.unpack_from('>I', data, offset)[0]
        kind = data[offset + 4:offset + 8]
        end = offset + 12 + length
        require(end <= len(data), f'Truncated PNG {kind!r} chunk')
        payload = data[offset + 8:offset + 8 + length]
        expected_crc = struct.unpack_from('>I', data, offset + 8 + length)[0]
        require(zlib.crc32(kind + payload) & 0xffffffff == expected_crc,
                f'Invalid PNG {kind!r} CRC')
        if chunks == 0:
            require(kind == b'IHDR' and length == 13, 'PNG must start with a 13-byte IHDR')
            dimensions = struct.unpack_from('>II', payload)
            require(all(value > 0 for value in dimensions), 'PNG dimensions must be positive')
        else:
            require(kind != b'IHDR', 'Duplicate PNG IHDR')
        chunks += 1
        has_idat = has_idat or kind == b'IDAT'
        if kind == b'IEND':
            require(length == 0 and end == len(data), 'PNG IEND must be empty and final')
            require(has_idat, 'PNG has no image data')
            return dimensions
        offset = end
    raise ValueError('PNG has no final IEND')


def verify(log, platform, exit_code):
    result = {'schema_version': 1, 'passed': False, 'platform': platform,
              'minecraft': VERSIONS[platform], 'log': str(log.resolve()),
              'exit_code': exit_code, 'visual_review_pending': True,
              'gameplay_verified': False, 'png_structure_verified': False,
              'image_decode_verified': False, 'errors': []}
    try:
        raw = log.read_bytes()
        result['log_sha256'] = hashlib.sha256(raw).hexdigest()
        started, receipt, screenshot, run_uuid = parse_run(decode_log(raw), platform, exit_code)
        result.update({'run_uuid': run_uuid, 'screenshot': str(screenshot),
                       'started_elapsed_ms': started['elapsedMs'],
                       'success_elapsed_ms': receipt['elapsedMs'],
                       'rendered_frames': receipt['renderedFrames'], 'screen': receipt['screen']})
        require(screenshot.is_file(), f'Screenshot does not exist: {screenshot}')
        data = screenshot.read_bytes()
        require(bool(data), 'Screenshot is empty')
        result['screenshot_sha256'] = hashlib.sha256(data).hexdigest()
        result['screenshot_bytes'] = len(data)
        dimensions = check_png(data)
        result.update({'png_structure_verified': True,
                       'width': dimensions[0], 'height': dimensions[1]})
        require(dimensions == (receipt['width'], receipt['height']),
                'PNG IHDR dimensions differ from SUCCESS receipt')
        try:
            from PIL import Image
        except ImportError:
            result['image_decode_status'] = 'pillow_unavailable'
            raise ValueError('Pillow is unavailable; PNG structure passed, image decoding remains unverified')
        with Image.open(screenshot) as image:
            require(image.format == 'PNG', 'Pillow did not recognize a PNG')
            image.verify()
        # verify() checks format integrity; reopen and load() actually decode the pixels.
        with Image.open(screenshot) as image:
            image.load()
            require(image.size == dimensions, 'Decoded dimensions differ from PNG/receipt')
        result.update({'image_decode_verified': True, 'image_decode_status': 'pillow_verified',
                       'passed': True})
    except Exception as error:
        result['errors'].append(f'{type(error).__name__}: {error}')
    return result


def self_test():
    """Small rejection checks and one structural fixture, never game/visual evidence."""
    started = {'platform': 'forge', 'minecraft': '1.20.1', 'elapsedMs': 0}
    success = {'platform': 'forge', 'minecraft': '1.20.1', 'elapsedMs': 3000,
               'renderedFrames': 5, 'screen': TITLE_SCREEN, 'width': 1, 'height': 1}
    work = Path(__file__).resolve().parents[2] / 'work'
    work.mkdir(exist_ok=True)
    checked = 0
    with tempfile.TemporaryDirectory(prefix='client-smoke-self-test-', dir=work) as directory:
        folder = Path(directory).resolve()
        require(folder.is_relative_to(work.resolve()), 'Self-test scratch escaped the work directory')
        screenshot = folder / f'gregtech-client-smoke-forge-1.20.1-{uuid.uuid4()}.png'
        success['screenshot'] = str(screenshot)
        good = ('CLIENT_SMOKE_STARTED ' + json.dumps(started) + '\nCLIENT_SMOKE_SUCCESS ' +
                json.dumps(success) + '\nBUILD SUCCESSFUL in 3s\n')
        parse_run(good, 'forge', 0)
        checked += 1
        cases = [('BUILD SUCCESSFUL in 1s\n', 0),
                 ('CLIENT_SMOKE_STARTED ' + json.dumps(started) +
                  '\nCLIENT_SMOKE_FAILED {"phase":"timeout"}\nBUILD SUCCESSFUL\n', 0),
                 ('CLIENT_SMOKE_STARTED ' + json.dumps(started) + '\n' + good, 0),
                 (good, 1)]
        for text, exit_code in cases:
            try:
                parse_run(text, 'forge', exit_code)
            except ValueError:
                checked += 1
            else:
                raise AssertionError('Invalid log/exit code was accepted')
        def chunk(kind, payload):
            return (struct.pack('>I', len(payload)) + kind + payload +
                    struct.pack('>I', zlib.crc32(kind + payload) & 0xffffffff))
        png = (PNG_SIGNATURE + chunk(b'IHDR', struct.pack('>IIBBBBB', 1, 1, 8, 2, 0, 0, 0)) +
               chunk(b'IDAT', zlib.compress(b'\x00\x11\x22\x33')) + chunk(b'IEND', b''))
        require(check_png(png) == (1, 1), 'Structural fixture failed')
        checked += 1
        for bad_png in (png[:-12], png[:-1]):
            try:
                check_png(bad_png)
            except ValueError:
                checked += 1
            else:
                raise AssertionError('Incomplete PNG was accepted')
        screenshot.write_bytes(png)
        log = folder / 'fixture.log'
        log.write_text(good, encoding='utf-8')
        result = verify(log, 'forge', 0)
        if result.get('image_decode_status') == 'pillow_unavailable':
            require(not result['passed'] and result['png_structure_verified'],
                    'Missing Pillow must not claim a decode pass')
        else:
            require(result['passed'] and result['image_decode_verified'], 'Pillow fixture failed')
        checked += 1
        wrong_size = dict(success, width=2)
        log.write_text('CLIENT_SMOKE_STARTED ' + json.dumps(started) +
                       '\nCLIENT_SMOKE_SUCCESS ' + json.dumps(wrong_size) +
                       '\nBUILD SUCCESSFUL\n', encoding='utf-8')
        result = verify(log, 'forge', 0)
        require(not result['passed'] and any('dimensions differ' in error for error in result['errors']),
                'Mismatched screenshot dimensions were accepted')
        checked += 1
    return {'self_test_passed': True, 'checks': checked, 'fixture_is_not_runtime_evidence': True}


def verify_world_pair(prepare_log, verify_log, exit_codes, manifest_path):
    """Validate the existing Neo probe's two real JVM runs, not title-screen evidence."""
    from PIL import Image
    manifest = json.loads(manifest_path.read_text(encoding='utf-8-sig'))
    result = {'schema_version': 1, 'passed': False, 'platform': 'neoforge',
              'minecraft': '1.21.1', 'runs': [], 'source_world_unchanged': False,
              'visual_review_pending': True, 'full_survival_verified': False,
              'installed_production_jar_verified': False, 'errors': []}
    try:
        require(len(exit_codes) == 2 and all(code == 0 for code in exit_codes),
                'Both real game/Gradle exit codes must be zero')
        token = manifest['specimenId']
        require(str(uuid.UUID(token)) == token, 'Noncanonical specimen UUID')
        pattern = re.compile(r'\bCLIENT_WORLD_(SMOKE_STARTED|SMOKE_SUCCESS|SMOKE_FAILED|CAPTURE_SUCCESS)\b')
        roles = ['world', 'crusher-gui', 'mixer-gui']
        all_tokens = set()
        for phase, log, exit_code in zip(('prepare', 'verify'), (prepare_log, verify_log), exit_codes):
            raw = log.read_bytes()
            text = decode_log(raw)
            require('CLIENT_WORLD_OPERATOR_ABORT' not in text, 'Run was aborted')
            entries = {key: [] for key in ('SMOKE_STARTED', 'SMOKE_SUCCESS', 'SMOKE_FAILED', 'CAPTURE_SUCCESS')}
            builds = []
            for number, line in enumerate(text.splitlines(), 1):
                line = ANSI.sub('', line)
                if 'BUILD SUCCESSFUL' in line:
                    builds.append(number)
                for match in pattern.finditer(line):
                    kind = match.group(1)
                    require(kind != 'SMOKE_FAILED', 'World smoke failed')
                    receipt = json.loads(line[match.end():].strip(), object_pairs_hook=unique_object)
                    entries[kind].append((number, receipt))
            require(len(entries['SMOKE_STARTED']) == len(entries['SMOKE_SUCCESS']) == 1,
                    'Expected exactly one start and one success')
            start_line, start = entries['SMOKE_STARTED'][0]
            end_line, end = entries['SMOKE_SUCCESS'][0]
            require(start_line < end_line and any(line > end_line for line in builds),
                    'Missing successful terminal ordering')
            captures = entries['CAPTURE_SUCCESS']
            require([receipt['role'] for _, receipt in captures] == roles,
                    'Expected exactly the three ordered real world/menu captures')
            require(start.get('stage') == 0 and end.get('stage') == 14,
                    'Incomplete world lifecycle')
            require(end.get('normalIntegratedServerStop') is True and end.get('savedWorldExists') is True,
                    'No normal integrated-server save/stop')
            for receipt in [start, end] + [r for _, r in captures]:
                require(receipt.get('platform') == 'neoforge' and receipt.get('minecraft') == '1.21.1',
                        'Wrong platform/version')
                require(receipt.get('phase') == phase and receipt.get('worldName') == manifest['worldName']
                        and receipt.get('specimenId') == token and receipt.get('pid') == start.get('pid'),
                        'World/process identity mismatch')
            require(integer(start.get('pid')) and start['pid'] > 0, 'Missing JVM process ID')
            require(end['elapsedMs'] > start['elapsedMs'], 'Invalid elapsed order')
            proof = end['proof']
            loaded = proof['loadedWorld']
            require(loaded.get('serverClass') == 'net.minecraft.client.server.IntegratedServer'
                    and loaded.get('originalSpecimenId') == manifest['original_specimen_id']
                    and loaded.get('copiedStoppedMachinesLoaded') is True,
                    'No original stopped-machine integrated-world checkpoint')
            require(loaded.get('restoredTransferredStock') == (phase == 'verify')
                    and loaded.get('restoredNamedWaterAmount') == (1000 if phase == 'prepare' else 1500),
                    'Saved input/fluid was not restored before verification')
            for key in ('actualRightClickCrusherMenu', 'actualRightClickMixerMenu',
                        'namedItemClientServerTransferOrReload'):
                require(proof.get(key) is True, f'Missing real menu proof: {key}')
            require(proof.get('namedFluidClientAmount') == 1500
                    and proof.get('liveFluidPacketUpdate') == (phase == 'prepare'),
                    'No real fluid update/reloaded amount')
            require(end.get('captures') == [r for _, r in captures], 'Terminal capture receipts differ')
            image_rows = []
            for number, receipt in captures:
                require(start_line < number < end_line, 'Capture outside run')
                path = Path(receipt['screenshot'])
                require(path.is_absolute() and path.parent == Path(manifest['target']).parents[1] / 'screenshots',
                        'Screenshot escaped isolated run directory')
                match = re.fullmatch(r'gregtech-client-world-neoforge-1\.21\.1-' + phase + '-' +
                                     receipt['role'] + r'-([0-9a-f-]{36})\.png', path.name)
                require(match is not None, 'Wrong screenshot name')
                image_token = match.group(1)
                require(str(uuid.UUID(image_token)) == image_token and uuid.UUID(image_token).version == 4
                        and image_token not in all_tokens, 'Screenshot UUID must be fresh canonical v4')
                all_tokens.add(image_token)
                data = path.read_bytes()
                dimensions = check_png(data)
                require(dimensions == (receipt['width'], receipt['height']), 'PNG dimensions mismatch')
                with Image.open(path) as image:
                    image.verify()
                with Image.open(path) as image:
                    image.load()
                    require(image.size == dimensions and image.format == 'PNG', 'Image decoding failed')
                image_rows.append(dict(receipt, sha256=hashlib.sha256(data).hexdigest(), bytes=len(data),
                                       png_structure_verified=True, image_decode_verified=True))
            result['runs'].append({'phase': phase, 'pid': start['pid'], 'exit_code': exit_code,
                                   'log': str(log.resolve()), 'log_sha256': hashlib.sha256(raw).hexdigest(),
                                   'receipt': end, 'screenshots': image_rows})
        require(result['runs'][0]['pid'] != result['runs'][1]['pid'], 'Reload reused the same JVM')
        source = Path(manifest['source'])
        expected = {row['path']: row for row in manifest['files']}
        actual = {p.relative_to(source).as_posix(): p for p in source.rglob('*')
                  if p.is_file() and p.name != 'session.lock'}
        require(actual.keys() == expected.keys(), 'Original source-world file inventory changed')
        for relative, path in actual.items():
            data = path.read_bytes()
            require(len(data) == expected[relative]['bytes'] and
                    hashlib.sha256(data).hexdigest() == expected[relative]['sha256'],
                    f'Original source world changed: {relative}')
        result.update(passed=True, source_world_unchanged=True, source_file_count=len(expected),
                      copied_world=manifest, source_manifest_sha256=hashlib.sha256(manifest_path.read_bytes()).hexdigest())
    except Exception as error:
        result['errors'].append(f'{type(error).__name__}: {error}')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--log', type=Path)
    parser.add_argument('--platform', choices=VERSIONS)
    parser.add_argument('--exit-code', type=int)
    parser.add_argument('--output', type=Path, help='Write the JSON evidence receipt here, including failures')
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--world-prepare-log', type=Path)
    parser.add_argument('--world-verify-log', type=Path)
    parser.add_argument('--world-manifest', type=Path)
    parser.add_argument('--world-exit-codes', type=int, nargs=2)
    args = parser.parse_args()
    if args.self_test:
        print(json.dumps(self_test(), ensure_ascii=False))
        return 0
    if args.world_prepare_log is not None:
        if any(value is None for value in (args.world_verify_log, args.world_manifest,
                                           args.world_exit_codes, args.output)):
            parser.error('World mode requires prepare/verify logs, manifest, two real exit codes and output')
        if args.output.resolve() in {args.world_prepare_log.resolve(), args.world_verify_log.resolve(),
                                     args.world_manifest.resolve()}:
            parser.error('Output must not overwrite source evidence')
        result = verify_world_pair(args.world_prepare_log, args.world_verify_log,
                                   args.world_exit_codes, args.world_manifest)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(json.dumps({'passed': result['passed'], 'errors': result['errors']}, ensure_ascii=False))
        return 0 if result['passed'] else 1
    if args.log is None or args.platform is None or args.exit_code is None or args.output is None:
        parser.error('--log, --platform, --exit-code and --output are required')
    if args.output.resolve() == args.log.resolve():
        parser.error('--output must not overwrite the source log')
    result = verify(args.log, args.platform, args.exit_code)
    if result.get('screenshot') and args.output.resolve() == Path(result['screenshot']).resolve():
        parser.error('--output must not overwrite the screenshot')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
