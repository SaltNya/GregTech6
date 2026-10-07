"""Console encoding must not corrupt a successful language self-check receipt."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'integration'))
from launch_production_smoke import parse_receipt


class DeliveryLanguageTests(unittest.TestCase):
    def test_native_messages_do_not_determine_structured_receipt_encoding(self):
        raw = b'Native message \x85\xff\nPRODUCTION_SMOKE_SUCCESS ' + '{"text":"中文 / 1538°C"}'.encode('utf-8')
        self.assertEqual(parse_receipt(raw, 0, 'sample.log')['text'], '中文 / 1538°C')

    def test_legacy_codepage_receipt_must_not_silently_replace_characters(self):
        raw = b'PRODUCTION_SMOKE_SUCCESS ' + '{"text":"1538°C"}'.encode('cp936')
        with self.assertRaises(UnicodeDecodeError):
            parse_receipt(raw, 0, 'sample.log')

    def test_failure_marker_is_not_hidden_by_native_encoding(self):
        raw = b'\xff PRODUCTION_SMOKE_FAILED\nPRODUCTION_SMOKE_SUCCESS {}'
        with self.assertRaisesRegex(ValueError, 'Production client failure'):
            parse_receipt(raw, 0, 'sample.log')

    def test_duplicate_receipts_and_failed_exit_are_rejected(self):
        for raw, code in [(b'PRODUCTION_SMOKE_SUCCESS {}\nPRODUCTION_SMOKE_SUCCESS {}', 0),
                          (b'PRODUCTION_SMOKE_SUCCESS {}', 1)]:
            with self.subTest(raw=raw, code=code), self.assertRaises(ValueError):
                parse_receipt(raw, code, 'sample.log')
