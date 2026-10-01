"""Compare an immutable supplied-source manifest with a fetched original Git tree."""
import argparse
import gzip
import hashlib
import json
import subprocess
from pathlib import Path


def git(*args):
    return subprocess.run(['git', *args], check=True, capture_output=True).stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', choices=['saltnya', 'brokestar233', 'masson'], required=True)
    parser.add_argument('--ref', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    provenance = repo / 'docs/integration/provenance'
    entry = next(e for e in json.loads((provenance / 'summary.json').read_text(encoding='utf-8')) if e['author'] == args.source)
    raw_manifest = gzip.decompress((provenance / entry['manifest_file']).read_bytes())
    if hashlib.sha256(raw_manifest).hexdigest() != entry['manifest_sha256']:
        raise SystemExit('Manifest checksum mismatch')
    expected = {e['path']: e for e in json.loads(raw_manifest)['files']}
    tree = {}
    gitlinks = {}
    for record in git('ls-tree', '-rz', '--full-tree', args.ref).split(b'\0'):
        if not record:
            continue
        metadata, path = record.split(b'\t', 1)
        mode, kind, oid = metadata.decode('ascii').split()
        name = path.decode('utf-8')
        if kind == 'blob':
            tree[name] = oid
        elif kind == 'commit':
            gitlinks[name] = oid
    scratch = repo / 'work'
    scratch.mkdir(exist_ok=True)
    requests = scratch / f'history-requests-{args.source}.txt'
    requests.write_text(''.join(oid + '\n' for oid in sorted(set(tree.values()))), encoding='ascii')
    hashes = {}
    with requests.open('rb') as input_file:
        process = subprocess.Popen(['git', 'cat-file', '--batch'], stdin=input_file, stdout=subprocess.PIPE)
        try:
            for oid in sorted(set(tree.values())):
                header = process.stdout.readline().decode('ascii').strip().split()
                if len(header) != 3 or header[0] != oid or header[1] != 'blob':
                    raise ValueError(f'Unexpected Git batch response: {header}')
                data = process.stdout.read(int(header[2]))
                if len(data) != int(header[2]) or process.stdout.read(1) != b'\n':
                    raise ValueError('Truncated Git object stream')
                hashes[oid] = hashlib.sha256(data).hexdigest()
            if process.wait() != 0:
                raise ValueError('Git cat-file failed')
        finally:
            if process.poll() is None:
                process.terminate()
    matching = [name for name, oid in tree.items() if name in expected and hashes[oid] == expected[name]['sha256']]
    missing = sorted(name for name in tree if name not in expected)
    changed = sorted(name for name, oid in tree.items() if name in expected and hashes[oid] != expected[name]['sha256'])
    extra = sorted(set(expected) - tree.keys())
    result = {
        'source': args.source, 'ref': args.ref,
        'commit': git('rev-parse', f'{args.ref}^{{commit}}').decode().strip(),
        'manifest_sha256': entry['manifest_sha256'],
        'git_tracked_blobs': len(tree), 'matching_blobs': len(matching),
        'changed_from_git': changed, 'missing_from_snapshot': missing,
        'snapshot_only': extra, 'gitlinks': gitlinks,
        'status': 'exact-tracked-file-match' if not changed and not missing else 'snapshot-differs',
        'scope': 'Git blob byte comparison; extra snapshot files and submodule contents are reported separately',
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(f"{args.source}: {len(matching)}/{len(tree)} tracked files identical; changed={len(changed)}, missing={len(missing)}, extra={len(extra)}, gitlinks={len(gitlinks)}")


if __name__ == '__main__':
    main()
