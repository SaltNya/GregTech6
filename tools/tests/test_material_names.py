"""Small source-parser contracts; runtime naming is checked separately in shared Java."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'integration'))
from generate_material_names import block_end, material_symbols, prefix_rows


class MaterialNameGeneratorTests(unittest.TestCase):
    def test_braces_inside_java_strings_do_not_close_method(self):
        sample = '{ if (true) { return "} escaped \\\" {"; } } trailing'
        self.assertEqual(sample[block_end(sample, 0):], ' trailing')
        with self.assertRaises(ValueError):
            block_end('{return "}";', 0)

    def test_material_identity_uses_scopes_factories_and_aliases(self):
        symbols, groups = material_symbols('''
static OreDictMaterial gold() {return metal(790, "Gold", 0);}
Au = gold();
Alias = Au;
public static class WOODS {
Gold = wood(9500, "Golden Wood", 0);
Again = Gold;
}
Clay = clay(8215, "Clay", 0);
''')
        self.assertEqual(symbols['Alias'], (790, 'Gold'))
        self.assertEqual(symbols['WOODS.Again'], (9500, 'GoldenWood'))
        self.assertEqual(groups['clay'], {(8215, 'Clay')})

    def test_only_naming_tags_and_implicit_ore_tag_are_carried_over(self):
        helper = 'add(MATERIAL_BASED, UNIFICATABLE, ORE, TOOLTIP_ENCHANTS);'
        source = '''ore = create("ore", "Category", "Small ", " Ore").setOreStats(U).add(UNIFICATABLE);
dust = create("dust", "Dusts", "", " Dust").add(DUST_BASED, TD.Prefix.IS_CONTAINER, TOOLTIP_MATERIAL);'''
        self.assertEqual(prefix_rows(source, helper), {
            'ore': ('Small ', ' Ore', ['ORE']), 'dust': ('', ' Dust', ['DUST_BASED', 'IS_CONTAINER'])})
        with self.assertRaisesRegex(ValueError, 'setOreStats'):
            prefix_rows(source, '')
        with self.assertRaisesRegex(ValueError, 'display override'):
            prefix_rows(source + '\ndust.setLocalItemName("changed", "name");', helper)
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            prefix_rows(source + '\n' + source, helper)


if __name__ == '__main__':
    unittest.main()
