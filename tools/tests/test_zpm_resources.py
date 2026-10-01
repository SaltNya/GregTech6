import json
import unittest
from tools.restore_laser_models import ASSETS
from tools.check_render_resources import check


class ZpmResources(unittest.TestCase):
    def test_all_discharger_states_and_module_models_resolve(self):
        paths = [ASSETS / 'blockstates/zpm.json']
        for name in ['basic', 'advanced', 'elite']:
            path = ASSETS / f'blockstates/zpm_discharger_{name}.json'
            paths.append(path)
            model = json.loads(path.read_text(encoding='utf8'))
            self.assertEqual(24, len(model['variants']))
        issues, _ = check(paths)
        self.assertEqual([], issues)
