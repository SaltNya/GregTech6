"""Import language bindings by adopted registry identity. Dry run unless --write.

Input is LanguageIdentities.java's export from the current compiled core. The
original checkout is read-only; unsupported English expressions remain reported.
"""
import argparse
import ast
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


def material_key(name):
    internal=re.sub(r"[ \-'/]",'',name)
    return 'gt.material.'+internal[:1].upper()+internal[1:]


def any_material_names(original):
    """ANY.init overrides display names before multi-tile machine registration."""
    path=original/'src/main/java/gregapi/data/ANY.java'
    if not path.exists():return {},{},[]
    raw=masked(path.read_text(encoding='utf-8'))
    names={symbol:json.loads(value) for symbol,value in re.findall(
        r'\b(\w+)\s*=\s*any\(\s*('+STRING+r')',raw)}
    displays=dict(names)
    for line in raw.splitlines():
        symbol=re.match(r'\s*(\w+)\s*\.',line)
        if not symbol or symbol[1] not in names:continue
        local=re.findall(r'\.setLocal\s*\(\s*('+STRING+r')\s*\)',line)
        if len(local)>1 or len(local)!=len(re.findall(r'\.setLocal\s*\(',line)):
            raise ValueError('Unsupported original ANY display name: '+symbol[1])
        if len(local)==1:displays[symbol[1]]=json.loads(local[0])
    return names,displays,[path]


def tool_ids(original):
    cs = original / 'src/main/java/gregapi/data/CS.java'
    if not cs.exists(): return {}
    text = masked(cs.read_text(encoding='utf-8'))
    if 'class ToolsGT' not in text: return {}
    text = text.split('class ToolsGT',1)[1].split('public static final MultiItem',1)[0]
    return dict(re.findall(r'\b([A-Z][A-Z_0-9]*)\s*=\s*(\d+)\b',text))


def material_identities(original):
    """Positive original IDs prove material identity, including old field-name aliases.

    Names use OreDictMaterial's sanitizer; getLocal uses the separate setLocal
    override. ID zero is a validation/compatibility placeholder, never proof.
    """
    path=original/'src/main/java/gregapi/data/MT.java'
    material=original/'src/main/java/gregapi/oredict/OreDictMaterial.java'
    if not path.exists() or not material.exists():return {},{},[],{}
    by_id,english=defaultdict(set),defaultdict(set)
    for line in masked(path.read_text(encoding='utf-8')).splitlines():
        # Element declarations use zero-argument factories; a few symbols are
        # chained assignments (Ma, Magic = Ma = create(...)). Both still expose
        # a literal positive ID and original name at the actual constructor.
        row=re.search(r'(?:=|\breturn\b)\s*(\w+)\s*\(\s*(\d+)\s*,\s*('+STRING+')',line)
        if not row or int(row[2])==0:continue
        factory,ident=row[1],int(row[2])
        name=json.loads(row[3]);key=material_key(name)
        if key=='gt.material.':continue
        by_id[ident].add(key)
        local=re.findall(r'\.setLocal\s*\(\s*('+STRING+r')\s*\)',line)
        if len(local)>1 or len(local)!=len(re.findall(r'\.setLocal\s*\(',line)):continue
        if factory=='woodnormal' and not local:
            args=next(calls(line,factory))[1]
            if len(args)<3 or not re.fullmatch(STRING,args[2]):continue
            local=[args[2]]
        english[key].add(json.loads(local[0]) if local else name)
    ambiguous={str(k):sorted(v) for k,v in by_id.items() if len(v)!=1}
    return ({k:next(iter(v)) for k,v in by_id.items() if len(v)==1},
            {k:next(iter(v)) for k,v in english.items() if len(v)==1},[path,material],ambiguous)


def verified_material_proofs(identity_rows, material_ids):
    """Only the combination of positive numeric ID and exact internal name proves identity."""
    proofs=defaultdict(set)
    for key,original,ident in identity_rows:
        if key.startswith('@material-proof.') and ident.isdigit() and int(ident)>0:
            if material_ids.get(int(ident))==original:
                proofs[key.removeprefix('@material-proof.')].add((int(ident),original))
    return proofs


def resolve_material_collision(key, originals, proofs):
    # getTranslationKey() belongs to the actual material's internal name. A
    # same-named field in another category (e.g. Woods.Gold) must not replace it.
    canonical={original for _,original in proofs.get(key,set())
               if original in originals and key=='material.gregtech.'+original.removeprefix('gt.material.').lower()}
    return canonical if len(canonical)==1 else originals


def numbered_item_identities(original):
    """Use the same IL-to-recipe-ID conversion as the adopted recipe importer."""
    # That historical script executes its CLI at import time; only read its literal
    # naming tables. Never import/run a generator with obsolete output paths.
    recipe_importer=ROOT/'tools/transpile_gt6_chem.py'
    tables={}
    for node in ast.parse(recipe_importer.read_text(encoding='utf-8')).body:
        if isinstance(node,ast.Assign) and isinstance(node.targets[0],ast.Name):
            key=node.targets[0].id
            if key in ('IL_ITEM_PREFIXES','IL_SHAPE_PREFIXES','SHAPE_WORDS'): tables[key]=ast.literal_eval(node.value)
    def item_id(field):
        if any(field.startswith(prefix) for prefix in tables['IL_ITEM_PREFIXES']): return None
        for prefix,native in tables['IL_SHAPE_PREFIXES'].items():
            if not field.startswith(prefix): continue
            words=field[len(prefix):].lower().replace('_','')
            # Native shape IDs retained these spellings; the old recipe importer
            # does not normalize their original IL field word order completely.
            if prefix in ('Shape_Extruder_','Shape_SimpleEx_'):
                forms={'pipetiny':'tinypipe','pipesmall':'smallpipe','pipemedium':'mediumpipe',
                       'pipelarge':'largepipe','pipehuge':'hugepipe','ccc':'capsulecellcontainer',
                       'platetiny':'tinyplate','wirefine':'finewire'}
                if words in forms:return native+forms[words]
            for source,target in tables['SHAPE_WORDS'].items():
                if words==source.replace('_',''): return native+target
            return native+words
        return field.lower()
    file = ROOT/'core/src/main/java/com/gregtech/gregtech/content/recipe/TechnologicalItemDefinitions.java'
    aliases = dict(re.findall(r'Map.entry\("([^"]+)",\s*"([^"]+)"\)',masked(file.read_text(encoding='utf-8'))))
    result, files = {}, [file, ROOT/'tools/transpile_gt6_chem.py']
    categories={'MultiItemRandomTools':'randomtools','MultiItemFood':'food','MultiItemBottles':'bottles',
                'MultiItemCans':'cans','MultiItemTechnological':'technological','MultiItemBooks':'books'}
    for stem,category in categories.items():
        path=original/f'src/main/java/gregtech/items/{stem}.java'
        if not path.exists(): continue
        files.append(path)
        for line in masked(path.read_text(encoding='utf-8')).splitlines():
            field=re.search(r'IL\.(\w+)\s*\.set\(\s*addItem\(',line)
            if field is None: continue
            args=next(calls(line,'addItem'))[1]
            if not args[0].isdigit(): continue
            native=item_id(field[1])
            if native is None: continue
            native=aliases.get(native,native)
            if ':' in native: continue
            key='item.gregtech.'+native
            value=f'gt.multiitem.{category}.{args[0]}'
            if key in result and result[key]!=value: raise ValueError('Ambiguous original item: '+key)
            result[key]=value
    return result, files


def pipe_identities(original, symbols):
    """Resolve original helper offsets using adopted material identities, not names."""
    root = original / 'src/main/java'
    loader = root / 'gregtech/loaders/b/Loader_MultiTileEntities.java'
    if not loader.exists(): return {}, []
    files = [loader]
    result = {}
    for line in masked(loader.read_text(encoding='utf-8')).splitlines():
        assigned = re.search(r'aMat\s*=\s*(MT\.\w+)\s*;', line)
        for _, args in calls(line, 'aRegistry.add'):
            if len(args)>4 and args[4]=='MultiTileEntityCell.class' and args[2].isdigit() and assigned:
                if assigned[1] in symbols:
                    key='@cell.'+symbols[assigned[1]]
                    value='gt.multitileentity.'+args[2]
                    if key in result and result[key]!=value: raise ValueError('Ambiguous original capsule: '+key)
                    result[key]=value
    sizes = {'pipeTiny':'TINY','pipeSmall':'SMALL','pipeMedium':'MEDIUM',
             'pipeLarge':'LARGE','pipeHuge':'HUGE','pipeQuadruple':'QUADRUPLE',
             'pipeNonuple':'NONUPLE','pipeRestrictiveMedium':'RESTRICTIVE_MEDIUM',
             'pipeRestrictiveLarge':'RESTRICTIVE_LARGE','pipeRestrictiveHuge':'RESTRICTIVE_HUGE'}
    for kind, helper in [('item','Item'),('fluid','Fluid')]:
        path = root / f'gregapi/tileentity/connectors/MultiTileEntityPipe{helper}.java'
        files.append(path)
        offsets = {}
        for line in masked(path.read_text(encoding='utf-8')).splitlines():
            prefix = re.search(r'setTarget_\(OP\.(\w+)', line)
            rows = list(calls(line, 'aRegistry.add'))
            if prefix is None or not rows: continue
            offset = re.fullmatch(r'aID\s*(?:\+\s*(\d+))?', rows[0][1][2])
            if offset is None or prefix[1] not in sizes: continue
            size = sizes[prefix[1]]
            if size in offsets: raise ValueError('Duplicate original pipe size: ' + size)
            offsets[size] = int(offset[1] or 0)
        if len(offsets) != (6 if kind == 'item' else 7):
            raise ValueError('Incomplete original pipe helper: ' + kind)
        for _, args in calls(masked(loader.read_text(encoding='utf-8')), f'MultiTileEntityPipe{helper}.add{helper}Pipes'):
            if not args[0].isdigit() or args[-1] not in symbols: continue
            for size, offset in offsets.items():
                key = f'@pipe.{kind}.{symbols[args[-1]]}.{size}'
                value = 'gt.multitileentity.' + str(int(args[0]) + offset)
                if key in result and result[key] != value:
                    raise ValueError('Ambiguous original pipe material: ' + key)
                result[key] = value
    return result, files


def original_english(original):
    found, files = defaultdict(set), [original / 'src/main/java/gregapi/data/MT.java']
    tools = tool_ids(original)
    wood_classes = {}
    woods_file = original/'src/main/java/gregtech/loaders/a/Loader_Woods.java'
    if woods_file.exists():
        wood_classes=dict(re.findall(r'new (BlockTree\w+)\s*\(\s*"([^"]+)"',masked(woods_file.read_text(encoding='utf-8'))))
        files.append(woods_file)
    blocks_file = original/'src/main/java/gregtech/loaders/a/Loader_Blocks.java'
    if blocks_file.exists():
        wood_classes.update(re.findall(r'new (BlockFlowers[AB]|BlockBaleGrass|BlockBaleCrop|BlockSands|BlockGrass|BlockDiggable|'
                                      r'BlockAsphalt|BlockConcrete(?:Reinforced)?|BlockCFoam(?:Fresh)?|BlockGlass(?:Clear|Glow)|'
                                      r'BlockBars(?:Brass|Steel|TungstenSteel)|BlockSpike(?:Sharp|Steel|Super|Metal|Fancy))\s*\(\s*"([^"]+)"',
                                      masked(blocks_file.read_text(encoding='utf-8'))))
        files.append(blocks_file)
    def put(key, text):
        found[key].add(text)
    _,material_english,material_files,_=material_identities(original)
    files.extend(p for p in material_files if p not in files)
    for key,value in material_english.items():put(key,value)
    material_text = masked((original / 'src/main/java/gregapi/data/MT.java').read_text(encoding='utf-8'))
    material_names = defaultdict(set)
    for m in re.finditer(r'\bwoodnormal\(\s*\d+\s*,\s*(' + STRING + r')\s*,\s*(' + STRING + ')', material_text):
        put('gt.material.'+json.loads(m[1]),json.loads(m[2]))
    for m in re.finditer(r'(\w+)\s*=\s*\w+\s*\(\s*\d+\s*,\s*(' + STRING + ')', material_text):
        material_names[m[1]].add(json.loads(m[2]))
    factories = {m[1]: json.loads(m[2]) for m in re.finditer(
        r'static\s+OreDictMaterial\s+(\w+)\s*\(\)\s*\{return\s+\w+\s*\(\s*\d+\s*,\s*(' + STRING + ')', material_text)}
    for line in material_text.splitlines():
        assignment = re.match(r'\s*(\w+)\s*=\s*(\w+)\s*\(', line)
        if assignment is None: continue
        symbol, factory = assignment.groups()
        if factory in factories: material_names[symbol].add(factories[factory])
        # setLocal is the original registration-time getLocal value, not an alias.
        local = re.findall(r'\.setLocal\(\s*(' + STRING + r')\s*\)', line)
        if factory == 'woodnormal':
            args = next(calls(line, factory))[1]
            if len(args)>2 and re.fullmatch(STRING,args[2]): local=[args[2]]
        if len(local)==1: material_names[symbol]={json.loads(local[0])}
    arrays = {key: [s.strip() for s in values.split(',')] for key,values in
              re.findall(r'\b(\w+_T)\s*=\s*\{([^}]+)\}', material_text)}
    any_internal,any_names,any_files=any_material_names(original)
    files.extend(any_files)
    for symbol,internal in any_internal.items():put(material_key(internal),any_names[symbol])
    voltages, dyes = [], []
    cs = original / 'src/main/java/gregapi/data/CS.java'
    if cs.exists():
        match = re.search(r'\bVN\s*=\s*\{([^}]+)\}', masked(cs.read_text(encoding='utf-8')))
        if match: voltages = [json.loads(v.strip()) for v in match[1].split(',')]
        match = re.search(r'\bDYE_NAMES\s*=\s*\{([^}]+)\}', masked(cs.read_text(encoding='utf-8')))
        if match: dyes = [json.loads(v.strip()) for v in match[1].split(',')]
        files.append(cs)
    def material(expr):
        any_match = re.fullmatch(r'ANY\.(\w+)', re.sub(r'\s+', '', expr))
        if any_match: return any_names.get(any_match[1])
        array = re.fullmatch(r'MT\.DATA\.(\w+)\[(\d+)\]', re.sub(r'\s+', '', expr))
        if array:
            rows=arrays.get(array[1], [])
            if int(array[2])>=len(rows): return None
            symbol=rows[int(array[2])]
            if symbol.startswith('ANY.'): return any_names.get(symbol[4:])
            expr='MT.'+symbol
        match = re.fullmatch(r'MT\.(\w+)', re.sub(r'\s+', '', expr))
        names = material_names.get(match[1], set()) if match else set()
        return next(iter(names)) if len(names) == 1 else None
    def name(expr, mat=None):
        # Preserve all literal whitespace/case. No word matching or translated-name inference.
        parts = re.findall(STRING + r'|aMat\.getLocal\(\)|VN\[\d+\]|\+', expr)
        if re.sub(r'\s+', '', ''.join(parts)) != re.sub(r'\s+', '', expr):
            return None
        values = []
        for part in parts:
            if part == '+': continue
            if part == 'aMat.getLocal()':
                if mat is None: return None
                values.append(mat)
            elif part.startswith('VN['):
                index=int(part[3:-1])
                if index>=len(voltages): return None
                values.append(voltages[index])
            else: values.append(json.loads(part))
        return ''.join(values)
    for path in sorted((original / 'src/main/java').rglob('*.java')):
        raw = masked(path.read_text(encoding='utf-8-sig'))
        before = sum(map(len, found.values()))
        for key, text in re.findall(r'\bLH\.add\(\s*(' + STRING + r')\s*,\s*(' + STRING + ')', raw):
            put(json.loads(key), json.loads(text))
        if path.name == 'LH.java':
            constants = {key:json.loads(value) for key,value in re.findall(
                r'\b(\w+)\s*=\s*(' + STRING + ')',raw)}
            for _,args in calls(raw,'add'):
                if len(args)>1 and args[0] in constants and re.fullmatch(STRING,args[1]):
                    put(constants[args[0]],json.loads(args[1]))
        category = {'MultiItemRandomTools':'randomtools','MultiItemFood':'food','MultiItemBottles':'bottles',
                    'MultiItemCans':'cans','MultiItemTechnological':'technological','MultiItemBooks':'books'}.get(path.stem)
        if category:
            for _, args in calls(raw, 'addItem'):
                if len(args)<3 or not args[0].isdigit(): continue
                for suffix, expr in [('',args[1]),('.tooltip',args[2])]:
                    value=name(expr)
                    if value is not None: put(f'gt.multiitem.{category}.{args[0]}{suffix}',value)
            if category=='technological':
                # Original compact components: one explicit 0..9 voltage loop.
                loop=re.search(r'for\s*\(int i = 0; i < 10; i\+\+\)\s*\{([^}]+)\}',raw)
                if loop:
                    for _,args in calls(loop[1],'addItem'):
                        base=re.fullmatch(r'(\d+)\s*\+\s*i',args[0])
                        if not base: continue
                        for i in range(10):
                            for suffix,expr in [('',args[1]),('.tooltip',args[2])]:
                                value=name(expr.replace('VN[i]',f'VN[{i}]'))
                                if value is not None:put(f'gt.multiitem.technological.{int(base[1])+i}{suffix}',value)
        if path.name == 'Loader_MultiTileEntities.java':
            rows = list(calls(raw, 'aRegistry.add'))
            for pos, args in rows:
                if len(args)<3 or not args[2].isdigit(): continue
                prior = list(re.finditer(r'aMat\s*=\s*([^;]+);',raw[:pos]))
                value=name(args[0],material(prior[-1][1]) if prior else None)
                if value is not None: put('gt.multitileentity.'+args[2],value)
            for line in raw.splitlines():
                loop=re.search(r'for\s*\(int i = 0; i < (\d+); i\+\+\)',line)
                if not loop or int(loop[1])>300:continue
                for _,args in calls(line,'aRegistry.add'):
                    base=re.fullmatch(r'i\s*\+\s*(\d+)',args[2]);value=name(args[0])
                    if base and value is not None:
                        for i in range(int(loop[1])):put('gt.multitileentity.'+str(int(base[1])+i),value)
            body=raw.split('private static void metalset(',1)[1].split('private static void storages(',1)[0]
            for _, args in calls(raw,'metalset'):
                if len(args)<7 or not args[6].isdigit(): continue
                mat=material(args[5])
                for _, row in calls(body,'aRegistry.add'):
                    offset=re.fullmatch(r'(?:(\d+)\s*\+\s*)?aID',row[2])
                    value=name(row[0],mat)
                    if offset and value is not None:
                        put('gt.multitileentity.'+str(int(args[6])+int(offset[1] or 0)),value)
            for helper in ('Item','Fluid'):
                helper_file = original / f'src/main/java/gregapi/tileentity/connectors/MultiTileEntityPipe{helper}.java'
                if not helper_file.exists(): continue
                files.append(helper_file)
                helper_rows=list(calls(masked(helper_file.read_text(encoding='utf-8')), 'aRegistry.add'))
                for _, args in calls(raw, f'MultiTileEntityPipe{helper}.add{helper}Pipes'):
                    if not args[0].isdigit(): continue
                    mat=material(args[-1])
                    for _, row in helper_rows:
                        offset=re.fullmatch(r'aID\s*(?:\+\s*(\d+))?',row[2])
                        value=name(row[0],mat)
                        if offset and value is not None:
                            put('gt.multitileentity.'+str(int(args[0])+int(offset[1] or 0)),value)
        if path.name == 'OP.java':
            for key,text in re.findall(r'\bcreate\(\s*(' + STRING + r')\s*,\s*(' + STRING + ')',raw):
                put('oredict.prefix.'+json.loads(key),json.loads(text))
        if path.name == 'Loader_Rails.java':
            for helper in ('new BlockBaseRail','new BlockRailRoad'):
                for _, args in calls(raw, helper):
                    if len(args)>2 and re.fullmatch(STRING,args[1]) and re.fullmatch(STRING,args[2]):
                        put(json.loads(args[1]),json.loads(args[2]))
        if path.name == 'Loader_Tools.java':
            for _, args in calls(raw, 'ToolsGT.sMetaTool.addTool'):
                if len(args)<3: continue
                ident=tools.get(args[0].removeprefix('ToolsGT.'))
                if ident is None: continue
                for suffix,expr in [('',args[1]),('.tooltip',args[2])]:
                    value=name(expr)
                    if value is not None: put('gt.metatool.01.'+ident+suffix,value)
        if path.name == 'BlockGlowtus.java' and len(dyes)==16:
            suffix = re.search(r'LH\.add\(getUnlocalizedName\(\)\+"\."\+i,\s*DYE_NAMES\[i\]\s*\+\s*(' + STRING + ')',raw)
            if suffix:
                for i,dye in enumerate(dyes): put('gt.block.lilypad.glowtus.'+str(i),dye+json.loads(suffix[1]))
        if path.stem in wood_classes:
            if re.search(r'extends\s+BlockColored\b',raw) and len(dyes)==16:
                # Only evaluate the literal constructor and the verified common BlockColored formula.
                colored = original/'src/main/java/gregapi/block/metatype/BlockColored.java'
                formula = ''.join(re.findall(STRING+r'|\S',masked(colored.read_text(encoding='utf-8'))))
                for suffix in ('', '+" Slab"'):
                    expected='for(inti=0;i<16;i++)LH.add(getUnlocalizedName()+"."+i,DYE_NAMES[i]+" "+aDefaultLocalised'+suffix+');'
                    if expected not in formula:
                        raise ValueError('Unsupported original BlockColored name formula')
                if colored not in files:files.append(colored)
                defaults = {json.loads(args[4]) for _,args in calls(raw,'super')
                            if len(args)>4 and re.fullmatch(STRING,args[4])}
                if len(defaults)!=1:raise ValueError('Ambiguous colored block constructor: '+str(path))
                base=wood_classes[path.stem];default=next(iter(defaults))
                for i,dye in enumerate(dyes):
                    put(f'{base}.{i}',dye+' '+default)
                    for side in range(6):put(f'{base}.slab.{side}.{i}',dye+' '+default+' Slab')
            constructors=re.split(r'\b(?:public|protected)\s+'+re.escape(path.stem)+r'\s*\(',raw)[1:]
            for index,body in enumerate(constructors):
                base=wood_classes[path.stem]
                if index>0:
                    # The second planks constructor creates all six oriented slabs.
                    if 'Planks' not in path.stem:continue
                    bases=[base+'.slab.'+str(side) for side in range(6)]
                else:bases=[base]
                for suffix,text in re.findall(r'LH\.add\(getUnlocalizedName\(\)\s*\+\s*(' + STRING + r')\s*,\s*(' + STRING + ')',body):
                    for base in bases:put(base+json.loads(suffix),json.loads(text))
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
    # Shared LH instructions/labels can reuse an identical unique source phrase.
    # Deliberately excludes item/block names: wording is never an item identity.
    shared_phrases=defaultdict(set)
    for key,value in source_en.items():
        if key.startswith('gt.lang.') and key in source and value:
            shared_phrases[value].add(key)
    for key,value in english.items():
        if key.startswith('tooltip.gregtech.') and key not in aliases and len(shared_phrases[value])==1:
            candidates[key].update(shared_phrases[value])
    shelves = ROOT/'core/src/main/resources/data/gregtech/bookshelf_variants.json'
    for shelf in read_json(shelves)['variants']:
        key = 'block.gregtech.'+shelf['path']
        original = 'gt.multitileentity.'+str(shelf['gt6_id'])
        if original in source_en:
            candidates[key].add(original)
            fallbacks[key].add(source_en[original])
    item_candidates,item_files=numbered_item_identities(ns.source)
    for key,original in item_candidates.items():
        if key in english: candidates[key].add(original)
    files.extend(item_files)
    identity_rows = [line.split('\t') for line in ns.identities.read_text(encoding='utf-8-sig').splitlines()]
    material_ids,_,_,ambiguous_material_ids=material_identities(ns.source)
    material_proofs=verified_material_proofs(identity_rows,material_ids)
    symbols = {key.removeprefix('@symbol.'):original for key, original, _ in identity_rows
               if key.startswith('@symbol.')}
    pipes, pipe_files = pipe_identities(ns.source, symbols)
    pipes.update({'@tool.'+key:'gt.metatool.01.'+value for key,value in tool_ids(ns.source).items()})
    files = sorted(set(files + pipe_files))
    for key,original,fallback in identity_rows:
        if key.startswith(('@symbol.','@material-proof.')): continue
        if key.startswith('material.gregtech.') and original.startswith('gt.material.'):
            original=material_key(original.removeprefix('gt.material.'))
        original = pipes.get(original, original)
        candidates[key].add(original)
        if fallback: fallbacks[key].add(fallback)
    # A name already bound by numeric identity also owns that ID's description.
    for key in english:
        if key.endswith('.tooltip') and key[:-8] in aliases:
            original = aliases[key[:-8]] + '.tooltip'
            if original in source: candidates[key].add(original)
    added,conflicts,missing,ambiguous,resolved_collisions={},{},{},{},{}
    for key, originals in sorted(candidates.items()):
        if len(originals)>1:
            resolved=resolve_material_collision(key,originals,material_proofs)
            if len(resolved)==1:
                resolved_collisions[key]={'candidates':sorted(originals),'actual_material':next(iter(resolved))}
                originals=resolved
        if len(originals)!=1:
            ambiguous[key]=sorted(originals);continue
        original=next(iter(originals))
        if key not in english:
            if original in source_en:
                english[key]=source_en[original]
            elif len(fallbacks[key]) == 1 and key.startswith(('material.gregtech.','item.gregtech.tab_icon_', 'block.gregtech.bookshelf')):
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
            if len(material_proofs[key])==1 and next(iter(material_proofs[key]))[1]==original:
                ident=next(iter(material_proofs[key]))[0]
                conflicts[key]={'before':aliases[key],'after':original,'source_material_id':ident,
                                'reason':'Actual shared material ID matches original MT declaration; old field alias is not the material internal name'}
            elif key=='block.gregtech.mortar_block':
                conflicts[key]={'before':aliases[key],'after':original,'reason':'Original ceramic mortar:32735; sapphire tool variant:32075'}
            elif key=='block.gregtech.wood_barrel' and original=='gt.multitileentity.32733':
                conflicts[key]={'before':aliases[key],'after':original,'reason':'CheapWoodBarrelCatalog retains the original lead-rod cheap barrel, not the normal barrel 32714'}
            elif key.endswith('.tooltip') and aliases.get(key[:-8], '') + '.tooltip' == original:
                conflicts[key]={'before':aliases[key],'after':original,'reason':'Description belongs to the accepted original item number, even when multiple items share its text'}
            else:
                conflicts[key]={'accepted':aliases[key],'candidate':original,'action':'retained for source identity review'};continue
        if aliases.get(key)!=original:
            added[key]=original;aliases[key]=original
    added_tooltips={}
    for key,original in list(aliases.items()):
        if not key.startswith('item.gregtech.') or key.endswith('.tooltip') or not original.startswith('gt.multiitem.'):continue
        native,legacy=key+'.tooltip',original+'.tooltip'
        if key in english and native not in english and legacy in source and legacy in source_en:
            english[native]=source_en[legacy];aliases[native]=legacy;added_tooltips[native]=legacy
    english_changes={}
    # Only existing verified identity bindings; no English-name reverse lookup.
    for key, original in sorted(aliases.items()):
        if key in english and original in source_en and english[key]!=source_en[original]:
            english_changes[key]={'before':english[key],'after':source_en[original],'source_key':original}
            english[key]=source_en[original]
    report={'source_language_sha256':meta['sha256'],'new_bindings':added,'conflicts':conflicts,
            'ambiguous_original_material_ids':ambiguous_material_ids,
            'resolved_material_collisions':resolved_collisions,
            'missing_original':missing,'ambiguous_symbols':ambiguous,'english_changes':english_changes,'added_tooltips':added_tooltips,
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
    print(json.dumps({k:len(report[k]) for k in ['new_bindings','conflicts','missing_original','ambiguous_symbols','english_changes','added_tooltips']}))


if __name__=='__main__':main()
