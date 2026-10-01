"""Read-only original-resource and recipe checks; safe during the Java gate."""
import json
import re
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ASSETS=ROOT/'src/main/resources/assets/gregtech'
ORIGINAL=ROOT.parent/'gregtech6-master/gregtech6-master/src/main/resources/assets/gregtech'
TIERS=['ulv','lv','mv','hv','ev','iv','luv','zpm','uv','xv']
class LargeBatteryAssets(unittest.TestCase):
    def test_original_large_and_small_textures_and_gui_bytes(self):
        for folder in ['battery_electric','battery_electric_large']:
            source=ORIGINAL/'textures/blocks/machines/energystorages'/folder
            target=ASSETS/'textures/block/machines/energystorages'/folder
            for p in source.rglob('*'):
                if p.is_file():self.assertEqual(p.read_bytes(),(target/p.relative_to(source)).read_bytes())
        self.assertEqual((ORIGINAL/'textures/gui/chests/16.png').read_bytes(),(ASSETS/'textures/gui/chests/16.png').read_bytes())
    def test_all_twenty_nine_standard_names(self):
        cn=(ROOT.parent/'GregTech.lang').read_text(encoding='utf-8')
        lang=json.loads((ASSETS/'lang/zh_cn.json').read_text(encoding='utf-8'))
        devices=[(10080+i,'battery_box_'+t) for i,t in enumerate(TIERS)]+[(10090+i,'energy_storage_'+t) for i,t in enumerate(TIERS)]+[(10040+i,'transformer_'+TIERS[i]+'_'+TIERS[i+1]) for i in range(9)]
        for number,ident in devices:
            expected=re.search(r'^\s*S:gt\.multitileentity\.'+str(number)+r'=(.*)$',cn,re.M).group(1).strip()
            self.assertEqual(lang['block.gregtech.'+ident],expected)
            self.assertTrue((ASSETS/f'blockstates/{ident}.json').is_file())
    def test_twenty_three_patterns_and_transformer_dependency(self):
        recipes=list((ROOT/'src/main/resources/data/gregtech/recipes/energy_nodes').glob('*.json'))
        self.assertEqual(len(recipes),23)
        for p in recipes:
            r=json.loads(p.read_text(encoding='utf-8'))
            self.assertEqual(r['pattern'],['WIW','XMx','WIW'] if p.stem.startswith('transformer_') else ['WCW','WCW','XMX'])
            if p.stem.startswith('energy_storage_'):self.assertTrue(r['key']['M']['item'].startswith('gregtech:transformer_'))
if __name__=='__main__':unittest.main()
