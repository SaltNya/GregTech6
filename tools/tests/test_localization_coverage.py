import json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
class LocalizationCoverageTests(unittest.TestCase):
    def test_languages_have_identical_keys_and_argument_counts(self):
        root=ROOT/'src/main/resources/assets/gregtech/lang'
        en=json.loads((root/'en_us.json').read_text(encoding='utf-8'))
        zh=json.loads((root/'zh_cn.json').read_text(encoding='utf-8'))
        self.assertEqual(en.keys(),zh.keys())
        token=re.compile(r'(?<!%)%(?:\d+\$)?[sd]')
        for key in en:
            self.assertEqual(len(token.findall(en[key])),len(token.findall(zh[key])),key)
            self.assertNotIn('\ufffd',zh[key],key)
    def test_static_tooltip_and_jade_keys_exist(self):
        en=json.loads((ROOT/'src/main/resources/assets/gregtech/lang/en_us.json').read_text(encoding='utf-8'))
        missing=set()
        for path in (ROOT/'src/main/java').rglob('*.java'):
            for key in re.findall(r'"((?:tooltip|jade|message|gui|config)\.gregtech\.[a-zA-Z0-9_.]+)"',path.read_text(encoding='utf-8')):
                if not key.endswith('.') and key not in en:missing.add(key)
        self.assertFalse(missing,sorted(missing))
