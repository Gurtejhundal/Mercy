"""Plugin discovery paths and execution from an unrelated learner checkout."""
from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest

from mercy import __version__

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

    def test_release_version_has_notes_and_matching_plugin_manifests(self):
        import re
        metadata=(ROOT/'pyproject.toml').read_text()
        version=re.search(r'^version = "([^"]+)"',metadata,re.M).group(1)
        self.assertEqual(version,__version__)
        for path in ['.codex-plugin/plugin.json','.claude-plugin/plugin.json']:
            self.assertEqual(json.loads((ROOT/path).read_text())['version'],version)
        tag='v'+(version[:-2] if version.endswith('.0') else version)
        self.assertTrue((ROOT/'docs/releases'/f'{tag}.md').is_file())

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


    def test_bundled_notebook_can_render_human_edited_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / 'app.py').write_text('def hello():\n    return "hi"\n')
            command = [sys.executable, '-I', str(ROOT / 'scripts/mercy.py')]
            subprocess.run(command + ['prepare', '--project', '.', '--limit', '1'],
                           cwd=project, capture_output=True, text=True, check=True)
            evidence = project / 'mercy-output/mercy-evidence.json'
            data = json.loads(evidence.read_text())
            data['questions'][0]['answer'] = 'Reviewed explanation retained after regeneration.'
            evidence.write_text(json.dumps(data))
            subprocess.run(command + ['render', '--input', str(evidence)],
                           cwd=project, capture_output=True, text=True, check=True)
            notebook = project / 'mercy-output/mercy-studio.html'
            self.assertIn(data['questions'][0]['answer'], notebook.read_text())
            self.assertTrue((project / 'mercy-output/mercy-viva.md').is_file())

    def test_bundled_guided_prepare_and_next_work_from_a_learner_checkout(self):
        with tempfile.TemporaryDirectory() as tmp:
            project=Path(tmp);(project/'app.py').write_text('def hello(): return "hi"\n')
            command=[sys.executable,'-I',str(ROOT/'scripts/mercy.py')]
            version=subprocess.run(command+['--version'],cwd=project,check=True,capture_output=True,text=True)
            self.assertEqual(version.stdout.strip(),'Mercy '+__version__)
            subprocess.run(command+['prepare','--guided','--project','.'],cwd=project,capture_output=True,text=True,check=True)
            evidence=project/'mercy-output/mercy-evidence.json'
            result=subprocess.run(command+['next','--project','.','--input',str(evidence)],cwd=project,capture_output=True,text=True,check=True)
            task=json.loads(result.stdout)
            self.assertEqual(task['progress']['total'],10)
            self.assertFalse(task['ready_to_render'])
            self.assertTrue(task['source_excerpts'])


class GeneratedReportTests(unittest.TestCase):
    def test_fresh_scan_and_legacy_render_use_current_report_system(self):
        import re
        with tempfile.TemporaryDirectory() as tmp:
            project=Path(tmp);(project/'app.py').write_text('def hello(): return "hi"\n')
            command=[sys.executable,'-I',str(ROOT/'scripts/mercy.py')]
            version=subprocess.run(command+['--version'],cwd=project,check=True,capture_output=True,text=True)
            self.assertEqual(version.stdout.strip(),'Mercy '+__version__)
            subprocess.run(command+['prepare','--guided','--project','.'],cwd=project,check=True,capture_output=True,text=True)
            evidence=project/'mercy-output/mercy-evidence.json'
            data=json.loads(evidence.read_text())
            self.assertTrue(any(q.get('overview') for q in data['questions']))
            data.pop('workflow');data['questions'][0]['answer']='An existing detailed explanation survives.'
            for q in data['questions']:q.pop('overview',None)
            evidence.write_text(json.dumps(data))
            for operation in ('prepare','render'):
                html=(evidence.parent/'mercy-studio.html').read_text()
                atlas=json.loads(re.search(r'id="atlas-data">(.*?)</script>',html,re.S).group(1))
                self.assertEqual(atlas['generator_version'],__version__)
                self.assertEqual(set(re.findall(r'data-section="([^"]+)"',html)),{'overview','questions','flow','architecture','tree'})
                if operation=='render':self.assertIn('An existing detailed explanation survives.',html)
                else:subprocess.run(command+['render','--input',str(evidence)],cwd=project,check=True,capture_output=True,text=True)


if __name__ == '__main__':
    unittest.main()
