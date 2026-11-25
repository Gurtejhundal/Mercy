"""Evidence persistence must survive a failed regeneration."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from mercy.renderer import export_json


class EvidenceExportTests(unittest.TestCase):
    def test_failed_write_preserves_original_and_cleans_staging_file(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);output=root/'mercy-evidence.json'
            output.write_text('{"existing":"reviewed answers"}')
            original=output.read_bytes()
            for operation in ['fsync','replace']:
                with self.subTest(operation=operation):
                    with patch('mercy.renderer.os.'+operation,side_effect=OSError('disk failure')):
                        with self.assertRaises(OSError):export_json({},[],output)
                    self.assertEqual(output.read_bytes(),original)
                    self.assertEqual(list(root.glob('.mercy-evidence-*')),[])

    def test_export_preserves_permissions_and_rejects_symlink_outputs(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);output=root/'evidence.json';output.write_text('{}');output.chmod(0o640)
            export_json({'project':'example'},[],output)
            self.assertEqual(json.loads(output.read_text())['report']['project'],'example')
            self.assertEqual(output.stat().st_mode & 0o777,0o640)
            link=root/'linked.json';link.symlink_to(output);original=output.read_bytes()
            with self.assertRaises(ValueError):export_json({},[],link)
            self.assertEqual(output.read_bytes(),original)
