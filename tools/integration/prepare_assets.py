"""Repair a Mojang asset cache with hash-verified reuse and bounded downloads.

The index is produced by the normal Minecraft/Gradle setup. Sources remain untouched.
TLS verification stays enabled. Every reused/downloaded object must match size and SHA-1.
"""
import argparse
import concurrent.futures
import hashlib
import json
import re
import urllib.request
from pathlib import Path


def matches(path, record):
    return path.is_file() and path.stat().st_size == record['size'] and hashlib.sha1(path.read_bytes()).hexdigest() == record['hash']


def prepare(record, destination, reuse):
    digest = record['hash']
    if not re.fullmatch(r'[0-9a-f]{40}', digest):
        raise ValueError('Invalid Mojang object hash')
    relative = Path('objects') / digest[:2] / digest
    target = destination / relative
    if matches(target, record):
        return 'existing'
    target.parent.mkdir(parents=True, exist_ok=True)
    for candidate_root in reuse:
        candidate = candidate_root / relative
        if matches(candidate, record):
            target.write_bytes(candidate.read_bytes())
            return 'reused'
    url = f'https://resources.download.minecraft.net/{digest[:2]}/{digest}'
    last = None
    for _ in range(3):
        try:
            with urllib.request.urlopen(url, timeout=25) as response:
                data = response.read()
            if len(data) != record['size'] or hashlib.sha1(data).hexdigest() != digest:
                raise ValueError(f'Object checksum mismatch: {digest}')
            target.write_bytes(data)
            return 'downloaded'
        except Exception as error:
            last = error
    raise RuntimeError(f'{digest}: {last}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--index', type=Path, required=True)
    parser.add_argument('--destination', type=Path, required=True)
    parser.add_argument('--reuse', type=Path, action='append', default=[])
    args = parser.parse_args()
    objects = json.loads(args.index.read_text(encoding='utf-8'))['objects']
    records = {record['hash']: record for record in objects.values()}
    counts = {'existing': 0, 'reused': 0, 'downloaded': 0}
    errors = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(prepare, record, args.destination, args.reuse): digest for digest, record in records.items()}
        for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
            try:
                counts[future.result()] += 1
            except Exception as error:
                errors.append(str(error))
            if i % 250 == 0 or i == len(futures):
                print(f'{i}/{len(futures)} validated objects; {counts}; errors={len(errors)}', flush=True)
    if errors:
        print(json.dumps(errors, ensure_ascii=False))
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
