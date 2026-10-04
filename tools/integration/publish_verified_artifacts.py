"""Publish complete verified jars under a fresh, stable directory; never expose a partial jar."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import uuid
import zipfile


def publish(report_path, output):
    report = json.loads(report_path.read_text(encoding='utf-8-sig'))
    if report.get('status') != 'passed':
        raise ValueError('Artifact verification did not pass')
    root = Path(__file__).resolve().parents[2] / 'build/verified'
    root.mkdir(parents=True, exist_ok=True)
    pending = root / ('.pending-' + str(uuid.uuid4()))
    pending.mkdir()
    records = {}
    for platform in ('forge', 'neoforge'):
        expected = report[platform]
        source = Path(expected['path'])
        target = pending / source.name
        shutil.copyfile(source, target)
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        if digest != expected['sha256'] or target.stat().st_size != expected['bytes']:
            raise ValueError(f'{platform} changed after verification; incomplete copy was not published')
        with zipfile.ZipFile(target) as archive:
            if archive.testzip() is not None:
                raise ValueError(f'{platform} copy failed ZIP CRC verification')
        records[platform] = {'name': source.name, 'bytes': expected['bytes'], 'sha256': digest,
                             'zip_crc_checked': True}
    name = datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%SZ') + '-' + records['forge']['sha256'][:8]
    final = root / name
    for record in records.values():
        record['path'] = str(final / record['name'])
    manifest = {'status': 'passed', 'scope': 'Verified complete copies; runtime evidence is recorded separately',
                'directory': str(final), 'verification_report': str(report_path.resolve()),
                'verification_report_sha256': hashlib.sha256(report_path.read_bytes()).hexdigest(),
                'artifacts': records}
    (pending / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (pending / 'SHA256SUMS.txt').write_text(''.join(r['sha256'] + '  ' + r['name'] + '\n'
                                               for r in records.values()), encoding='utf-8')
    # The complete directory appears in one rename, after both copied jars pass.
    os.rename(pending, final)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(output.name + '.' + str(uuid.uuid4()) + '.tmp')
    temporary.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    os.replace(temporary, output)
    print(f'Published complete dual artifacts: {final}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verification-report', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        publish(args.verification_report, args.output)
    except (OSError, ValueError, KeyError, zipfile.BadZipFile) as error:
        parser.exit(1, f'Artifact publication failed: {error}\n')


if __name__ == '__main__':
    main()
