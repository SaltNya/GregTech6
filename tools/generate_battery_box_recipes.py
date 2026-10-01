"""GT6 10040-10048 and resolvable 10080-10096 recipes; no invented high circuits."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT/'src/main/resources/data/gregtech'
TIERS = ['ulv','lv','mv','hv','ev','iv','luv','zpm','uv','xv']
CASINGS = ['tinalloy','steelgalvanized','aluminium','stainlesssteel','chromium','titanium','iridium','osmiumelemental','trinitanium']
WIRES = ['lead','tin','copper','gold','aluminium','platinum','graphene']
def write(path, data):
    text=json.dumps(data,ensure_ascii=False,indent=2)+'\n'
    path.parent.mkdir(parents=True,exist_ok=True)
    if not path.exists() or path.read_text(encoding='utf-8')!=text:path.write_text(text,encoding='utf-8')
def item(name):return {'item':'gregtech:'+name}
def run():
    # Tier zero accepts the already implemented higher circuits through the original substitution rule.
    write(DATA/'tags/items/circuits_tier_0_plus.json',{'replace':False,'values':['#gregtech:circuits_tier_1_plus',{'id':'#forge:circuits/primitive','required':False}]})
    for i in range(9):
        ident='transformer_'+TIERS[i]+'_'+TIERS[i+1]
        metal='copper' if i<3 else 'annealed_copper'
        write(DATA/f'recipes/energy_nodes/{ident}.json',{'type':'gregtech:tool_shaped','allow_mirror':False,'pattern':['WIW','XMx','WIW'],'key':{'W':({'tag':'gregtech:wire_01/any_copper'} if i<3 else item('wire_01_'+metal)),'X':({'tag':'gregtech:wire_04/any_copper'} if i<3 else item('wire_04_'+metal)),'I':{'tag':'gregtech:plate_double/any_iron_or_steel'},'M':item('casing_machine_'+CASINGS[i]),'x':item('tool_wire_cutter')},'result':item(ident)})
    for i in range(7):
        for large in (False,True):
            ident=('energy_storage_' if large else 'battery_box_')+TIERS[i]
            size='04' if large else '01'
            middle='transformer_'+TIERS[i]+'_'+TIERS[i+1] if large else 'casing_machine_'+CASINGS[i]
            write(DATA/f'recipes/energy_nodes/{ident}.json',{'type':'minecraft:crafting_shaped','pattern':['WCW','WCW','XMX'],'key':{'W':({'tag':'gregtech:wire_'+size+'/any_copper'} if i==2 else item('wire_'+size+'_'+WIRES[i])),'C':({'tag':'gregtech:cable_'+size+'/any_copper'} if i==2 else item(('wire_' if i>=6 else 'cable_')+size+'_'+WIRES[i])),'X':{'tag':f'gregtech:circuits_tier_{i}_plus'},'M':item(middle)},'result':item(ident)})
    for lang in ['en_us','zh_cn']:
        path=ROOT/f'src/main/resources/assets/gregtech/lang/{lang}.json'
        data=json.loads(path.read_text(encoding='utf-8'))
        data['tooltip.gregtech.node.battery_slots']='Battery slots: %s; capacity comes from installed batteries' if lang=='en_us' else '电池槽位：%s；容量由装入的电池决定'
        data['tooltip.gregtech.transformer.controls']='Monkey wrench: reverse conversion (clears buffered energy)' if lang=='en_us' else '活动扳手：反转变压方向（清空缓冲能量）'
        write(path,dict(sorted(data.items())))
    print('23 recipes: 9 transformers, 7 ordinary and 7 large battery boxes; tiers 7-9 await circuit providers, large tier 9 also lacks original transformer 10049.')
if __name__=='__main__':run()
