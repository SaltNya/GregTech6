"""Copy selected native tooltip keys from original LH/CS and the user's Chinese patch.

No translations are generated. Missing source keys fail; missing patch values are
reported and retain Minecraft's English fallback. The audit preserves exact values.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', type=Path, required=True)
    ap.add_argument('--zh-patch', type=Path, required=True)
    ap.add_argument('--java', type=Path, required=True)
    ap.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[2])
    ap.add_argument('--audit', type=Path, required=True)
    ap.add_argument('--keys', nargs='*', default=[], help='Additional shared rule keys, validated against original source.')
    ap.add_argument('--extra-java', type=Path, action='append', default=[], help='Additional port Java files containing tooltip keys.')
    ap.add_argument('--extra-source', type=Path, action='append', default=[], help='Original source files containing literal LH.add keys.')
    ap.add_argument('--alias', nargs=2, action='append', default=[], metavar=('PORT_KEY', 'SOURCE_KEY'),
                    help='Existing port language key mapped to an original LH/CS key, without translating it.')
    ns = ap.parse_args()
    root = ns.source / 'src/main/java/gregapi/data'
    lh = (root / 'LH.java').read_text(encoding='utf-8')
    cs = (root / 'CS.java').read_text(encoding='utf-8')
    literal = r'("(?:\\.|[^"\\])*")'
    constants = {m[1]: json.loads(m[2]) for m in re.finditer(r'(\w+)\s*=\s*' + literal, lh)}
    english = {constants[m[1]]: json.loads(m[2]) for m in re.finditer(r'\badd\(\s*(\w+)\s*,\s*' + literal, lh) if m[1] in constants}
    tools = {m[1]: json.loads(m[2]) for m in re.finditer(r'(TOOL_\w+)\s*=\s*' + literal, cs)}
    for m in re.finditer(r'LH.add\(TOOL_LOCALISER_PREFIX\s*\+\s*(TOOL_\w+)\s*,\s*' + literal, cs):
        english['gt.lang.tool.name.' + tools[m[1]]] = json.loads(m[2])
    rm = (root / 'RM.java').read_text(encoding='utf-8')
    td = (root / 'TD.java').read_text(encoding='utf-8')
    for m in re.finditer(r'("gt\.recipe\.[^"\\]+")\s*,\s*' + literal, rm):
        english[json.loads(m[1])] = json.loads(m[2])
    for m in re.finditer(r'TagData\.createTagData\(\s*' + literal + r'\s*,\s*' + literal + r'\s*,\s*' + literal, td):
        name = json.loads(m[1]).lower()
        english['gt.td.short.' + name] = json.loads(m[2])
        english['gt.td.long.' + name] = json.loads(m[3])
    for file in ns.extra_source:
        file.resolve().relative_to(ns.source.resolve())
        contents = file.read_text(encoding='utf-8')
        contents = re.sub(r'"(?:\\.|[^"\\])*"|//[^\n]*|/\*[\s\S]*?\*/',
                          lambda m: m[0] if m[0].startswith('"') else re.sub(r'[^\n]', ' ', m[0]), contents)
        for m in re.finditer(r'LH\.add\(\s*' + literal + r'\s*,\s*' + literal, contents):
            english[json.loads(m[1])] = json.loads(m[2])
    chinese = {}
    for line in ns.zh_patch.read_text(encoding='utf-8').splitlines():
        row = line.lstrip()
        if row.startswith('S:') and '=' in row:
            key, value = row[2:].split('=', 1)
            chinese[key] = value
    aliases = dict(ns.alias)
    java_keys = set()
    for file in [ns.java, *ns.extra_java]:
        java_keys.update(re.findall(r'"(gt\.(?:lang|recipe|tooltip|td)\.[^"\\]+)"', file.read_text(encoding='utf-8')))
    keys = sorted(java_keys | set(ns.keys) | set(aliases))
    changes, missing = {}, []
    for locale, imported in [('en_us', english), ('zh_cn', chinese)]:
        file = ns.repo / f'core/src/main/resources/assets/gregtech/lang/{locale}.json'
        data = json.loads(file.read_text(encoding='utf-8'))
        changes[locale] = {}
        for key in keys:
            source_key = aliases.get(key, key)
            if source_key not in imported:
                if locale == 'en_us': raise ValueError('Original English key missing: ' + source_key)
                missing.append(key)
                continue
            if data.get(key) != imported[source_key]: changes[locale][key] = {'before': data.get(key), 'after': imported[source_key]}
            data[key] = imported[source_key]
        file.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    paths = [root/'LH.java', root/'CS.java', root/'RM.java', root/'TD.java', root/'../code/TagData.java', *ns.extra_source, ns.zh_patch]
    ns.audit.parent.mkdir(parents=True, exist_ok=True)
    ns.audit.write_text(json.dumps({'keys': keys, 'aliases': aliases, 'changes': changes, 'missing_chinese': missing,
        'source_files': [{'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths],
        'license': 'Original LH/CS/RM/TD/TagData: LGPL-3.0-or-later; Chinese strings copied verbatim from the user-provided patch.'}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'keys': len(keys), 'changed': {k: len(v) for k,v in changes.items()}, 'missing_chinese': missing}, ensure_ascii=False))


if __name__ == '__main__': main()
