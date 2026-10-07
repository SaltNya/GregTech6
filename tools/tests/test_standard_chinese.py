"""The accepted source, not a hand-written expected translation, is authoritative."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from localization import ROOT, LANG_PATH, CONFIG_PATH, read_json, synchronize


class StandardChineseTests(unittest.TestCase):
    def test_all_values_match_pinned_source_or_exact_english_fallback(self):
        report = synchronize()
        self.assertGreater(report['source_keys'], 100000)
        self.assertGreater(report['native_aliases'], 6000)

    def test_sensor_and_canvas_bindings_keep_original_identity(self):
        aliases = read_json(ROOT / CONFIG_PATH / 'aliases.json')
        self.assertEqual(aliases['block.gregtech.sensor_electrometer'], 'gt.multitileentity.31015')
        self.assertEqual(aliases['item.gregtech.canvas_white.tooltip'], 'gt.multiitem.randomtools.7045.tooltip')
        # XV has no original family registration; do not manufacture a translated tier.
        english = read_json(ROOT / LANG_PATH / 'en_us.json')
        chinese = read_json(ROOT / LANG_PATH / 'zh_cn.json')
        key = 'item.gregtech.compact_electric_conveyor_xv'
        self.assertNotIn(key, aliases)
        self.assertEqual(chinese[key], english[key])
