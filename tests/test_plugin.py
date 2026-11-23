"""Plugin discovery paths and execution from an unrelated learner checkout."""
from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PluginTests(unittest.TestCase):
    def test_host_manifests_resolve_the_same_skill_and_icon(self):
        codex = json.loads((ROOT / '.codex-plugin/plugin.json').read_text())
        claude = json.loads((ROOT / '.claude-plugin/plugin.json').read_text())
        for manifest in (codex, claude):
            skill = ROOT / manifest['skills'] / 'mercy/SKILL.md'
            self.assertTrue(skill.is_file())
            self.assertTrue(skill.resolve().is_relative_to(ROOT))
        self.assertEqual(codex['skills'], claude['skills'])
        self.assertEqual(codex['interface']['shortDescription'], 'that one teacher we all know')
        self.assertTrue((ROOT / codex['interface']['composerIcon']).is_file())
        for path in ('.agents/plugins/marketplace.json', '.claude-plugin/marketplace.json'):
            catalog = json.loads((ROOT / path).read_text())
            self.assertEqual(catalog['plugins'][0]['name'], codex['name'])
            source = catalog['plugins'][0]['source']
            self.assertEqual((ROOT / (source['path'] if isinstance(source, dict) else source)).resolve(), ROOT)

    def test_bundled_toolkit_runs_without_install_or_target_imports(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / 'app.py').write_text('def hello():\n    return "hi"\n')
            shadow = project / 'mercy'
            shadow.mkdir()
            (shadow / '__init__.py').write_text('raise RuntimeError("target code executed")\n')
            result = subprocess.run(
                [sys.executable, '-I', str(ROOT / 'scripts/mercy.py'), 'inspect', '--project', '.'],
                cwd=project, capture_output=True, text=True, check=True)
            evidence = json.loads(result.stdout)
            self.assertIn('app.py', result.stdout)
            self.assertIsInstance(evidence, dict)
            self.assertFalse((project / 'mercy-output').exists())


if __name__ == '__main__':
    unittest.main()
