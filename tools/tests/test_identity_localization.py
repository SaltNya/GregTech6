"""Source identity parser must preserve English literals and refuse ambiguous IDs."""
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'integration'))
from import_identity_localization import original_english


class IdentityLanguageTests(unittest.TestCase):
    def setUp(self):
        (Path(__file__).resolve().parents[2]/'work').mkdir(exist_ok=True)

    def test_original_literals_material_names_and_numeric_offsets(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[2]/'work') as folder:
            root=Path(folder); java=root/'src/main/java'
            (java/'gregapi/data').mkdir(parents=True)
            (java/'gregapi/data/MT.java').write_text('Steel = metal(26, "Source Steel", 0);',encoding='utf-8')
            (java/'Loader_MultiTileEntities.java').write_text('''
private static void metalset(Object aRegistry, Object aMat, int aID) {
 aRegistry.add("Bookshelf ("+aMat.getLocal()+")", "Storage", 7100+aID, 0);
}
private static void storages() {
 metalset(aRegistry, aMetal, aUtilMetal, aMachine, aWooden, MT.Steel, 10, 1);
 aMat = MT.Steel; aRegistry.add("Machine ("+aMat.getLocal()+")", "Machines", 20000, 0);
 // aRegistry.add("wrong", "Machines", 20000, 0);
 aRegistry.add("Unsupported "+VN[1], "Machines", 20001, 0);
 LH.add("gt.tooltip.sample", " Exact source! ");
}
''',encoding='utf-8')
            result,_=original_english(root)
            self.assertEqual(result['gt.multitileentity.7110'],'Bookshelf (Source Steel)')
            self.assertEqual(result['gt.multitileentity.20000'],'Machine (Source Steel)')
            self.assertEqual(result['gt.tooltip.sample'],' Exact source! ')
            self.assertNotIn('gt.multitileentity.20001',result)

    def test_conflicting_declarations_are_not_silently_overwritten(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[2]/'work') as folder:
            root=Path(folder);java=root/'src/main/java'
            (java/'gregapi/data').mkdir(parents=True)
            (java/'gregapi/data/MT.java').write_text('',encoding='utf-8')
            (java/'MultiItemBooks.java').write_text('''
addItem(1, "Book", "");
addItem(2, "First", "Original description");
addItem(2, "Conflicting", "Original description");
''',encoding='utf-8')
            result,_=original_english(root)
            self.assertEqual(result['gt.multiitem.books.1'],'Book')
            self.assertEqual(result['gt.multiitem.books.1.tooltip'],'')
            self.assertNotIn('gt.multiitem.books.2',result)
            self.assertEqual(result['gt.multiitem.books.2.tooltip'],'Original description')
