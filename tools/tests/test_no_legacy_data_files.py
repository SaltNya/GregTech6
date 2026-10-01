import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class LegacyDataCleanupTests(unittest.TestCase):
    def test_old_facade_files_are_removed(self):
        data = ROOT / 'src/main/java/com/gregtech/gregtech/data'
        for name in 'AM ANY BI CS FL FM IL LH MD MT OD OP RM TC TD'.split():
            self.assertFalse((data / f'{name}.java').exists(), name)
        self.assertTrue((data / 'ImportedMaterialData.java').exists())
