import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check_material_coverage import declarations


class MaterialCoverageTests(unittest.TestCase):
    def test_chained_particle_alias_is_not_silently_skipped(self):
        rows = declarations('Photon = y = create(1, "Photon"); // Gone = create(9, "Gone");')
        self.assertEqual([('Photon', 1)], [(r['name'], r['id']) for r in rows])

    def test_dynamic_names_remain_explicitly_unresolved(self):
        rows = declarations('HexoriumBlack = hexorium(9224, 32, 32, 32, DYE_INDEX_Black);')
        self.assertEqual(9224, rows[0]['id'])
        self.assertFalse(rows[0]['name'])

    def test_aligned_antimatter_declarations(self):
        rows = declarations('D, Deuterium = D = diatomic      ( 4011, "Anti-Deuterium", 1, 1);')
        self.assertEqual([('Anti-Deuterium', 4011)], [(r['name'], r['id']) for r in rows])
