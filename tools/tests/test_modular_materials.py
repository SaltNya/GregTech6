"""Lossless material generation and Java identifier migration contracts."""
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
from modular_materials import JAVA, GROUPS, parse_catalog, write_catalog
from readable_data_names import readable_java


class MaterialGenerationTests(unittest.TestCase):
    def test_regeneration_matches_checked_in_catalogs(self):
        source = (TOOLS / 'generated/materials-source.java.txt').read_text(encoding='utf-8')
        groups = parse_catalog(source)
        self.assertEqual(1056, sum(map(len, groups.values())))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'data/generated').mkdir(parents=True)
            shutil.copyfile(JAVA / 'data/ImportedMaterialData.java', root / 'data/ImportedMaterialData.java')
            write_catalog(source, root, save_intermediate=False)
            paths = ['content/material/Materials.java', 'data/generated/GT6Materials.java']
            paths += [f'content/material/generated/{name}.java' for name in GROUPS.values()]
            for path in paths:
                with self.subTest(path=path):
                    self.assertEqual((JAVA / path).read_text(encoding='utf-8'),
                                     (root / path).read_text(encoding='utf-8'))

    def test_rename_preserves_registry_strings_and_comments(self):
        source = 'RM.Mixer; String id = "RM.FL"; // RM stays\n/* FL stays */ FL.Water;'
        self.assertEqual('MachineRecipeMaps.Mixer; String id = "RM.FL"; // RM stays\n'
                         '/* FL stays */ RegisteredFluids.Water;', readable_java(source))

    def test_worldgen_references_resolve_after_material_rename(self):
        from generate_ore_block_assets import parse_definitions, worldgen_fields
        materials, _ = parse_definitions()
        references = worldgen_fields()
        self.assertGreater(len(references), 20)
        self.assertEqual(set(), references - materials.keys())


if __name__ == '__main__':
    unittest.main()
