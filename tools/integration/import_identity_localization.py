"""Import language bindings by adopted registry identity. Dry run unless --write.

Input is LanguageIdentities.java's export from the current compiled core. The
original checkout is read-only; unsupported English expressions remain reported.
"""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from localization import ROOT, LANG_PATH, CONFIG_PATH, load_source, read_json, json_text, expected_chinese
from generate_machine_material_data import calls, masked

STRING = r'"(?:\\.|[^"\\])*"'


def original_english(original):
    found, files = defaultdict(set), [original / 'src/main/java/gregapi/data/MT.java']
    def put(key, text):
        found[key].add(text)
    material_text = masked((original / 'src/main/java/gregapi/data/MT.java').read_text(encoding='utf-8'))
    material_names = defaultdict(set)
    for m in re.finditer(r'\bwoodnormal\(\s*\d+\s*,\s*(' + STRING + r')\s*,\s*(' + STRING + ')', material_text):
        put('gt.material.'+json.loads(m[1]),json.loads(m[2]))
    for m in re.finditer(r'(\w+)\s*=\s*\w+\s*\(\s*\d+\s*,\s*(' + STRING + ')', material_text):
        material_names[m[1]].add(json.loads(m[2]))
    def material(expr):
        match = re.fullmatch(r'MT\.(\w+)', re.sub(r'\s+', '', expr))
        names = material_names.get(match[1], set()) if match else set()
        return next(iter(names)) if len(names) == 1 else None
    def name(expr, mat=None):
        # Preserve all literal whitespace/case. No word matching or translated-name inference.
        parts = re.findall(STRING + r'|aMat\.getLocal\(\)|\+', expr)
        if re.sub(r'\s+', '', ''.join(parts)) != re.sub(r'\s+', '', expr):
            return None
        values = []
        for part in parts:
            if part == '+': continue
            if part == 'aMat.getLocal()':
                if mat is None: return None
                values.append(mat)
            else: values.append(json.loads(part))
        return ''.join(values)
    for path in sorted((original / 'src/main/java').rglob('*.java')):
        raw = masked(path.read_text(encoding='utf-8-sig'))
        before = sum(map(len, found.values()))
        for key, text in re.findall(r'\bLH\.add\(\s*(' + STRING + r')\s*,\s*(' + STRING + ')', raw):
            put(json.loads(key), json.loads(text))
        category = {'MultiItemRandomTools':'randomtools','MultiItemFood':'food','MultiItemBottles':'bottles',
                    'MultiItemCans':'cans','MultiItemTechnological':'technological','MultiItemBooks':'books'}.get(path.stem)
        if category:
            for _, args in calls(raw, 'addItem'):
                if len(args)<3 or not args[0].isdigit(): continue
                for suffix, expr in [('',args[1]),('.tooltip',args[2])]:
                    value=name(expr)
                    if value is not None: put(f'gt.multiitem.{category}.{args[0]}{suffix}',value)
        if path.name == 'Loader_MultiTileEntities.java':
            rows = list(calls(raw, 'aRegistry.add'))
            for pos, args in rows:
                if len(args)<3 or not args[2].isdigit(): continue
                prior = list(re.finditer(r'aMat\s*=\s*([^;]+);',raw[:pos]))
                value=name(args[0],material(prior[-1][1]) if prior else None)
                if value is not None: put('gt.multitileentity.'+args[2],value)
            body=raw.split('private static void metalset(',1)[1].split('private static void storages(',1)[0]
            for _, args in calls(raw,'metalset'):
                if len(args)<7 or not args[6].isdigit(): continue
                mat=material(args[5])
                for _, row in calls(body,'aRegistry.add'):
                    offset=re.fullmatch(r'(?:(\d+)\s*\+\s*)?aID',row[2])
                    value=name(row[0],mat)
                    if offset and value is not None:
                        put('gt.multitileentity.'+str(int(args[6])+int(offset[1] or 0)),value)
        if path.name == 'OP.java':
            for key,text in re.findall(r'\bcreate\(\s*(' + STRING + r')\s*,\s*(' + STRING + ')',raw):
                put('oredict.prefix.'+json.loads(key),json.loads(text))
        if sum(map(len, found.values())) != before and path not in files: files.append(path)
    return {k:next(iter(v)) for k,v in found.items() if len(v)==1}, files


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source',type=Path,required=True)
    ap.add_argument('--identities',type=Path,required=True)
    ap.add_argument('--audit',type=Path,required=True)
    ap.add_argument('--write',action='store_true')
    ns=ap.parse_args()
    source,meta=load_source()
    aliases=read_json(ROOT/CONFIG_PATH/'aliases.json')
    english=read_json(ROOT/LANG_PATH/'en_us.json')
    source_en,files=original_english(ns.source)
    candidates=defaultdict(set)
    fallbacks=defaultdict(set)
    for line in ns.identities.read_text(encoding='utf-8-sig').splitlines():
        key,original,fallback=line.split('\t')
        candidates[key].add(original)
        if fallback: fallbacks[key].add(fallback)
    added,conflicts,missing,ambiguous={},{},{},{}
    for key, originals in sorted(candidates.items()):
        if len(originals)!=1:
            ambiguous[key]=sorted(originals);continue
        original=next(iter(originals))
        if key not in english:
            if len(fallbacks[key]) == 1 and key.startswith(('material.gregtech.','item.gregtech.tab_icon_')):
                english[key]=source_en.get(original,next(iter(fallbacks[key])))
            # Modern fluid paths are sanitized; reuse the existing English declaration.
            elif key.startswith('fluid_type.gregtech.'):
                legacy='fluid_type.gregtech.'+original.removeprefix('fluid.')
                if legacy not in english:continue
                english[key]=english[legacy]
            else:continue
        if original not in source:
            missing[key]=original;continue
        if key in aliases and aliases[key]!=original:
            # Accepted special original internal spellings must not be guessed from modern material names.
            if key=='block.gregtech.mortar_block':
                conflicts[key]={'before':aliases[key],'after':original,'reason':'Original ceramic mortar:32735; sapphire tool variant:32075'}
            else:
                conflicts[key]={'accepted':aliases[key],'candidate':original,'action':'retained for source identity review'};continue
        if aliases.get(key)!=original:
            added[key]=original;aliases[key]=original
    english_changes={}
    # Only existing verified identity bindings; no English-name reverse lookup.
    for key, original in sorted(aliases.items()):
        if key in english and original in source_en and english[key]!=source_en[original]:
            english_changes[key]={'before':english[key],'after':source_en[original],'source_key':original}
            english[key]=source_en[original]
    report={'source_language_sha256':meta['sha256'],'new_bindings':added,'conflicts':conflicts,
            'missing_original':missing,'ambiguous_symbols':ambiguous,'english_changes':english_changes,
            'source_files':[{'path':str(p.resolve()),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files],
            'identity_export_sha256':hashlib.sha256(ns.identities.read_bytes()).hexdigest(),
            'authors':'GregTech-6 Team / Gregorius Techneticies; original Java LGPL-3.0-or-later',
            'policy':'Chinese copied verbatim from pinned user file; local work only; conflicting modern symbol spellings are not inferred'}
    translated=expected_chinese(english,source,aliases)
    if ns.write:
        (ROOT/CONFIG_PATH/'aliases.json').write_text(json_text(aliases),encoding='utf-8')
        (ROOT/LANG_PATH/'en_us.json').write_text(json_text(english),encoding='utf-8')
        (ROOT/LANG_PATH/'zh_cn.json').write_text(json_text(translated),encoding='utf-8')
        pinned={key:{'source_key':original,'value':source_en[original]}
                for key,original in aliases.items() if key in english and original in source_en}
        (ROOT/CONFIG_PATH/'english_source.json').write_text(json_text({
            'policy':'Exact original English for source declarations resolved by adopted identity; remaining port text checked separately',
            'values':pinned,'source_files':report['source_files']}),encoding='utf-8')
    ns.audit.write_text(json_text(report),encoding='utf-8')
    print(json.dumps({k:len(report[k]) for k in ['new_bindings','conflicts','missing_original','ambiguous_symbols','english_changes']}))


if __name__=='__main__':main()
