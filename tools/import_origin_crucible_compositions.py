"""Keep chemical composition distinct from actual GT6 crucible recipes."""
from pathlib import Path
import re,json,hashlib
root=Path(__file__).resolve().parents[1]
source=root.parent/'gregtech6-master/gregtech6-master/src/main/java/gregapi/data/MT.java'
raw=source.read_text(encoding='utf-8')
entries=[]
for line in raw.splitlines():
    match=re.match(r'\s*(?:\w+\s*=\s*)+\w+\s*\(\s*(\d+),',line)
    if not match:continue
    if re.search(r'\.(?:setAloy|uumAloy)\(',line) or re.search(r'\.alloy(?:Simple|Centrifuge|Electrolyzer)\(\s*(?:\d+[Ll]?\s*(?:,\s*\d+[Ll]?)?)?\s*\)',line):
        entries.append(int(match[1]))
assert len(entries)>70,len(entries)
dest=root/'core/src/main/java/com/gregtech/gregtech/api/machine/crucible/OriginalCrucibleCompositions.java'
dest.write_text(raw.split('package ')[0]+'''package com.gregtech.gregtech.api.machine.crucible;
/** MT.setAloy/uumAloy/alloySimple recipe declarations, not all ALLOY chemistry. */
public final class OriginalCrucibleCompositions {
    private OriginalCrucibleCompositions() {}
    private static final java.util.Set<Integer> IDS=java.util.Set.of('''+','.join(map(str,sorted(set(entries))))+''');
    public static boolean hasRecipe(int materialId){return IDS.contains(materialId);}
}
''',encoding='utf-8')
(root/'docs/integration/verification/origin-crucible-compositions-20261004.json').write_text(json.dumps({'source':str(source),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'default_crucible_recipe_material_ids':sorted(set(entries)),'steel_airless_recipe':False,'scope':'Source declarations; actual runtime assertions recorded separately'},indent=2)+'\n',encoding='utf-8')
print('Imported',len(set(entries)),'original default creation recipes')
