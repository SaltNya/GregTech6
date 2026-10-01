import unittest,re,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ORIGINAL=ROOT.parent/'gregtech6-master/gregtech6-master/src/main'
class AxleAssets(unittest.TestCase):
 def test_all_original_animation_files_are_exact(self):
  files=list((ORIGINAL/'resources/assets/gregtech/textures/blocks/iconsets').glob('AXLE*'))
  self.assertEqual(15,len(files))
  for source in files:
   self.assertEqual(source.read_bytes(),(ROOT/'src/main/resources/assets/gregtech/textures/block/iconsets'/source.name.lower()).read_bytes())
 def test_axis_face_rotation_matrix_is_original(self):
  source=(ORIGINAL/'java/gregapi/old/Textures.java').read_text(encoding='utf-8').split('AXLES[][] =',1)[1].split('GLASSES_CLEAR',1)[0]
  expected=[]
  for row in re.findall(r'\{(AXLE[^{}]+)\}',source):
   expected.append([x.strip().removeprefix('AXLE').removeprefix('_').lower() for x in row.split(',')])
  port=(ROOT/'src/main/java/com/gregtech/gregtech/client/AxleBakedModel.java').read_text(encoding='utf-8').split('private final',1)[0]
  actual=[re.findall(r'"([a-z]*)"',row) for row in re.findall(r'\{([^{}]+)\}',port) if len(re.findall(r'"([a-z]*)"',row))==3]
  self.assertEqual(18,len(expected));self.assertEqual(expected,actual)
if __name__=='__main__':unittest.main()
