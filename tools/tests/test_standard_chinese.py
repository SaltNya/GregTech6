import json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
class StandardChineseTests(unittest.TestCase):
 def test_every_imported_name_matches_supplied_source(self):
  legacy={m[1].strip():m[2] for line in (ROOT.parent/'GregTech.lang').read_text(encoding='utf-8').splitlines() if (m:=re.match(r'\s*S:([^=]+)=(.*)',line))}
  origins=json.loads((ROOT/'docs/standard-chinese-origins.json').read_text(encoding='utf-8'))
  zh=json.loads((ROOT/'src/main/resources/assets/gregtech/lang/zh_cn.json').read_text(encoding='utf-8'))
  self.assertGreater(len(origins),1000)
  for key,source in origins.items():self.assertEqual(zh[key],legacy[source],key)
 def test_conveyor_resources_and_standard_name(self):
  zh=json.loads((ROOT/'src/main/resources/assets/gregtech/lang/zh_cn.json').read_text(encoding='utf-8'))
  for tier in ['ulv','lv','mv','hv','ev','iv','luv','zpm','uv','puv1','xv']:
   name='compact_electric_conveyor_'+tier
   self.assertTrue((ROOT/f'src/main/resources/assets/gregtech/models/item/{name}.json').is_file())
   self.assertIn('输送机模块',zh['item.gregtech.'+name])
