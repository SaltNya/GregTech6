"""Compare original GT6 declarations with a freshly exported runtime material catalog.

Run check_registration.py first. Identity presence does NOT certify property/recipe parity.
Unresolved dynamic declarations are reported, never silently counted as covered.
"""
import argparse
import json
import re
from pathlib import Path
from collections import Counter
from transpile_gt6_materials import collect_materials, parse_strings_and_numbers, split_args

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = ROOT.parent / 'gregtech6-master/gregtech6-master/src/main/java/gregapi/data'


def declarations(source):
    source = re.sub(r'/\*.*?\*/|//[^\n]*', '', source, flags=re.S)
    _, collected = collect_materials(source)
    rows = []
    for field, (factory, args, _) in collected.items():
        parsed = parse_strings_and_numbers(split_args(args))
        rows.append({'field': field, 'factory': factory, 'id': parsed['id'], 'name': parsed['name']})
    # MT particle / AM chained aliases are not matched by the historical importer.
    for match in re.finditer(r'\b(\w+)\s*=\s*(?:\w+\s*=\s*)*(\w+)\s*\(\s*(\d+)\s*,\s*"([^"]+)"', source):
        field, factory, identity, name = match.groups()
        if not any(row['id'] == int(identity) and row['name'] == name for row in rows):
            rows.append({'field': field, 'factory': factory, 'id': int(identity), 'name': name})
    return rows


def canonical(name):
    return name.replace(' ', '').replace('-', '').replace("'", '')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog', type=Path, default=ROOT / 'build/registration-material-catalog.json')
    parser.add_argument('--report', type=Path, default=ROOT / 'build/material-coverage.json')
    args = parser.parse_args()
    current = json.loads(args.catalog.read_text(encoding='utf-8'))
    names = {row['name']: row['id'] for row in current}
    rows = []
    for source_name in ('MT.java', 'AM.java'):
        for row in declarations((ORIGINAL / source_name).read_text(encoding='utf-8')):
            row['source'] = source_name
            name = row['name']
            if not name or row['id'] < 0:
                status = 'unresolved_or_virtual'
            elif canonical(name) not in names:
                status = 'missing_identity'
            elif names[canonical(name)] != row['id']:
                status = 'id_mismatch'
            else:
                status = 'identity_present_not_behavior_verified'
            row['status'] = status
            rows.append(row)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps({'note': 'Identity-only comparison; aliases/dynamic factories may need manual review.',
                                     'runtimeCatalog': str(args.catalog), 'entries': rows}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(dict(Counter(row['status'] for row in rows)))
    print('Report:', args.report)


if __name__ == '__main__':
    main()
