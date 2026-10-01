"""Import only unambiguous, source-backed GT6 names; never translate by word guessing."""
from pathlib import Path
import json,re,collections
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT.parent/'gregtech6-master/gregtech6-master/src/main/java'
def norm(s): return re.sub(r'[^a-z0-9]','',s.lower())
def sync():
 legacy={m[1].strip():m[2] for line in (ROOT.parent/'GregTech.lang').read_text(encoding='utf-8').splitlines() if (m:=re.match(r'\s*S:([^=]+)=(.*)',line))}
 folder=ROOT/'src/main/resources/assets/gregtech/lang'
 en=json.loads((folder/'en_us.json').read_text(encoding='utf-8'));zh=json.loads((folder/'zh_cn.json').read_text(encoding='utf-8'))
 names=collections.defaultdict(set)
 for p in (SOURCE/'gregtech/items').glob('MultiItem*.java'):
  category=p.stem.removeprefix('MultiItem').lower()
  for m in re.finditer(r'addItem\(\s*(\d+)\s*,\s*"([^"\n]+)"\s*,',p.read_text(encoding='utf-8')):
   key=f'gt.multiitem.{category}.{m[1]}'
   if legacy.get(key):names[norm(m[2])].add(key)
 mte=(SOURCE/'gregtech/loaders/b/Loader_MultiTileEntities.java').read_text(encoding='utf-8')
 for m in re.finditer(r'aRegistry.add\(\s*"([^"\n]+)"\s*,\s*"[^"\n]+"\s*,\s*(\d+)',mte):
  key='gt.multitileentity.'+m[2]
  if legacy.get(key):names[norm(m[1])].add(key)
 # Source loop has ten tiers. Resolve dynamic English names using its numeric base ID.
 tech=(SOURCE/'gregtech/items/MultiItemTechnological.java').read_text(encoding='utf-8')
 tier_names=['ULV','LV','MV','HV','EV','IV','LuV','ZPM','UV','PUV1']
 for m in re.finditer(r'addItem\(\s*(\d+)\+i\s*,\s*"([^"\n]+)"\+VN\[i\]\+"([^"\n]+)"',tech):
  for i,tier in enumerate(tier_names):
   key='gt.multiitem.technological.'+str(int(m[1])+i)
   if legacy.get(key):names[norm(m[2]+tier+m[3])].add(key)
 explicit={}
 tiers=['ulv','lv','mv','hv','ev','iv','luv','zpm','uv','puv1','xv']
 for i,tier in enumerate(tiers):explicit['item.gregtech.compact_electric_conveyor_'+tier]='gt.multiitem.technological.'+str(12040+i)
 for name,num in {'sifting_table':32702,'grindstone':32703,'dust_funnel':32704,'mixing_bowl':32706,'bathing_pot':32708,'coin_mold':32701,'wood_barrel':32714,'plant_pot':32065}.items():explicit['block.gregtech.'+name]='gt.multitileentity.'+str(num)
 origins={};changes={};ambiguous={}
 for key,value in en.items():
  source=explicit.get(key)
  if source is None and key.startswith('fluid.gregtech.'):
   candidate='fluid.'+key.removeprefix('fluid.gregtech.')
   if candidate in legacy:source=candidate
  if source is None and key.startswith(('item.gregtech.','block.gregtech.')):
   candidates=names[norm(value)]
   if len({legacy[c] for c in candidates})==1:source=sorted(candidates)[0]
   elif candidates:ambiguous[key]=sorted(candidates)
  if source is None and key in legacy:source=key
  if source and legacy.get(source) and not re.search(r'%(?:\d+\$)?[sd]',value):
   translated=legacy[source]
   # A display name must not accidentally import an incompatible format string.
   if '%' in translated:continue
   origins[key]=source
   if zh.get(key)!=translated:changes[key]={'old':zh.get(key),'new':translated,'source':source}
   zh[key]=translated
 # XV is a pre-existing port-only extra tier. Derive only its tier suffix from the standard family name.
 derived={}
 for key in en:
  if key.startswith('item.gregtech.compact_') and key.endswith('_xv'):
   base=key[:-3]+'_ulv'
   if base in origins:
    zh[key]=re.sub(r'\(ULV\)', '(XV)', zh[base])
    derived[key]={'source':origins[base],'rule':'ULV tier suffix replaced by port-only XV'}
 (ROOT/'docs/standard-chinese-derived.json').write_text(json.dumps(derived,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (folder/'zh_cn.json').write_text(json.dumps(dict(sorted(zh.items())),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (ROOT/'docs/standard-chinese-origins.json').write_text(json.dumps(origins,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 previous=ROOT/'docs/standard-chinese-changes.json'
 if previous.exists():
  old=json.loads(previous.read_text(encoding='utf-8')).get('changes',{})
  for key,value in changes.items():
   if key in old:value['old']=old[key]['old']
  changes={**old,**changes}
 (ROOT/'docs/standard-chinese-changes.json').write_text(json.dumps({'changes':changes,'ambiguous':ambiguous},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('Source-backed names:',len(origins),'corrected:',len(changes),'ambiguous:',len(ambiguous))
if __name__=='__main__':sync()
