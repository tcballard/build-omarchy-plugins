"""Behavioral regression checks for generated code and the current host contract."""
from __future__ import annotations
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
GENERATOR = REPO / 'skills/omarchy-plugin-scaffold/scripts/new_plugin.py'
VALIDATOR = REPO / 'skills/omarchy-plugin-test/scripts/validate_plugin.py'
SECTIONS = ('left', 'centerBegin', 'center', 'centerEnd', 'right', 'tray')

class QuattroAlignmentTests(unittest.TestCase):
    def generate(self, output: Path, *options: str) -> None:
        result = subprocess.run([sys.executable, str(GENERATOR), '--id', 'io.github.example.alignment', '--name', 'Alignment', '--author', 'Example', '--output', str(output), '--no-git', *options], capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_every_host_section_round_trips_generation_and_strict_validation(self):
        with tempfile.TemporaryDirectory() as temporary:
            for section in SECTIONS:
                with self.subTest(section=section):
                    output = Path(temporary) / section
                    self.generate(output, '--kind', 'bar-widget', '--default-section', section)
                    manifest = json.loads((output / 'manifest.json').read_text(encoding="utf-8"))
                    self.assertEqual(section, manifest['barWidget']['defaultSection'])
                    result = subprocess.run([sys.executable, str(VALIDATOR), '--strict', '--json', str(output)], capture_output=True, text=True)
                    self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                    manifest['barWidget']['defaultSection'] = 'drawer-typo'
                    (output / 'manifest.json').write_text(json.dumps(manifest), encoding="utf-8")
                    rejected = subprocess.run([sys.executable, str(VALIDATOR), '--json', str(output)], capture_output=True, text=True)
                    self.assertNotEqual(0, rejected.returncode)
                    self.assertIn('default-section', {e['code'] for e in json.loads(rejected.stdout)['errors']})

    def test_generated_visual_kinds_use_unambiguous_palette_imports(self):
        with tempfile.TemporaryDirectory() as temporary:
            for kind in ('bar-widget', 'panel', 'overlay', 'menu', 'bar'):
                with self.subTest(kind=kind):
                    output = Path(temporary) / kind
                    self.generate(output, '--kind', kind)
                    sources = list(output.glob('*.qml'))
                    self.assertTrue(sources)
                    for source in sources:
                        text = source.read_text(encoding="utf-8")
                        self.assertNotRegex(text, r'(?<![\w.])Color\.')
                        if 'Commons.Color.' in text:
                            self.assertIn('import qs.Commons as Commons', text)
                    if kind != 'bar-widget':
                        self.assertTrue(any('Commons.Color.' in source.read_text(encoding="utf-8") for source in sources))

if __name__ == '__main__':
    unittest.main()
