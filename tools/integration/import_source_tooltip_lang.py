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
    chinese = {}
    for line in ns.zh_patch.read_text(encoding='utf-8').splitlines():
        row = line.lstrip()
        if row.startswith('S:') and '=' in row:
            key, value = row[2:].split('=', 1)
            chinese[key] = value
    keys = sorted(set(re.findall(r'Component.translatable\("(gt\.lang\.[^"]+)"\)', ns.java.read_text(encoding='utf-8'))))
    changes, missing = {}, []
    for locale, imported in [('en_us', english), ('zh_cn', chinese)]:
        file = ns.repo / f'core/src/main/resources/assets/gregtech/lang/{locale}.json'
        data = json.loads(file.read_text(encoding='utf-8'))
        changes[locale] = {}
        for key in keys:
            if key not in imported:
                if locale == 'en_us': raise ValueError('Original English key missing: ' + key)
                missing.append(key)
                continue
            if data.get(key) != imported[key]: changes[locale][key] = {'before': data.get(key), 'after': imported[key]}
            data[key] = imported[key]
        file.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    paths = [root/'LH.java', root/'CS.java', ns.zh_patch]
    ns.audit.parent.mkdir(parents=True, exist_ok=True)
    ns.audit.write_text(json.dumps({'keys': keys, 'changes': changes, 'missing_chinese': missing,
        'source_files': [{'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths],
        'license': 'Original LH/CS: LGPL-3.0-or-later; Chinese strings copied verbatim from the user-provided patch.'}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'keys': len(keys), 'changed': {k: len(v) for k,v in changes.items()}, 'missing_chinese': missing}, ensure_ascii=False))


if __name__ == '__main__': main()
