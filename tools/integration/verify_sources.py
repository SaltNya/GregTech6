"""Verify preserved source snapshots against the captured SHA-256 manifests.

Never writes to a source directory or updates the authoritative capture.
Use --list for a cheap summary; full verification reads every captured file.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path, PureWindowsPath


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', choices=['all', 'saltnya', 'brokestar233', 'masson'], default='all')
    parser.add_argument('--sources-dir', type=Path, help='Override the parent Libs directory')
    parser.add_argument('--list', action='store_true')
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    provenance = repo / 'docs/integration/provenance'
    summary = json.loads((provenance / 'summary.json').read_text(encoding='utf-8'))
    if len(summary) != 3 or {e['author'] for e in summary} != {'saltnya', 'brokestar233', 'masson'}:
        raise SystemExit('Source summary must contain exactly the three captured sources')
    failed = False
    for entry in summary:
        name = entry['author']
        if args.source != 'all' and name != args.source:
            continue
        manifest_path = provenance / entry['manifest_file']
        packed = manifest_path.read_bytes()
        raw = gzip.decompress(packed) if manifest_path.suffix == '.gz' else packed
        if hashlib.sha256(raw).hexdigest() != entry['manifest_sha256']:
            print(f'{name}: authoritative manifest SHA-256 mismatch')
            failed = True
            continue
        manifest = json.loads(raw)
        if not manifest['files'] or len(manifest['files']) != entry['files']:
            raise SystemExit(f'{name}: empty or inconsistent source manifest')
        if args.list:
            print(f"{name}: {entry['files']} files, {entry['bytes']} bytes; manifest verified")
            continue
        source = Path(manifest['source_path'])
        source_name = PureWindowsPath(manifest['source_path']).name
        if args.sources_dir:
            source = args.sources_dir / source_name
        elif not source.is_dir():
            source = repo.parent / 'Libs' / source_name
        if not source.is_dir():
            print(f'{name}: source directory missing: {source}')
            failed = True
            continue
        expected = {f['path']: f for f in manifest['files']}
        missing, changed = [], []
        for relative, record in expected.items():
            path = source / relative
            if not path.is_file():
                missing.append(relative)
            elif path.stat().st_size != record['bytes'] or hashlib.sha256(path.read_bytes()).hexdigest() != record['sha256']:
                changed.append(relative)
        actual = {path.relative_to(source).as_posix() for path in source.rglob('*') if path.is_file()}
        extra = sorted(actual - expected.keys())
        result = {'source': name, 'files': len(expected), 'missing': missing, 'changed': changed, 'extra': extra}
        print(json.dumps(result, ensure_ascii=False))
        failed |= bool(missing or changed or extra)
    return int(failed)


if __name__ == '__main__':
    raise SystemExit(main())
