"""Validate the production artifact, iPhone metadata, icon dimensions, and scope-safe paths."""
from pathlib import Path
from html.parser import HTMLParser
import json
import struct
import unittest

ROOT = Path(__file__).resolve().parents[1]

class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.nodes = []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        self.nodes.append((tag, dict(attrs)))

class ProductionBuild(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT / '_site/index.html').read_text(encoding='utf-8')
        cls.doc = Document(cls.html)
        cls.manifest = json.loads((ROOT / '_site/manifest.webmanifest').read_text())

    def test_no_unbundled_scripts_or_styles(self):
        self.assertFalse(any(tag == 'script' and 'src' in a for tag, a in self.doc.nodes))
        self.assertFalse(any(tag == 'link' and a.get('rel') == 'stylesheet' for tag, a in self.doc.nodes))
        self.assertNotIn('<!-- PWA_HEAD -->', self.html)
        self.assertNotIn('__BUILD_VERSION__', (ROOT / '_site/sw.js').read_text())

    def test_iphone_metadata(self):
        meta = {a.get('name'): a.get('content') for tag, a in self.doc.nodes if tag == 'meta'}
        self.assertEqual(meta['apple-mobile-web-app-capable'], 'yes')
        self.assertEqual(meta['apple-mobile-web-app-title'], 'Night Run')
        self.assertIn('viewport-fit=cover', meta['viewport'])
        self.assertNotIn('user-scalable=no', meta['viewport'])
        icons = [a for tag, a in self.doc.nodes if tag == 'link' and a.get('rel') == 'apple-touch-icon']
        self.assertEqual(icons[0]['href'], 'apple-touch-icon.png')

    def test_manifest_works_below_repository_path(self):
        for field in ['id', 'scope', 'start_url']:
            self.assertEqual(self.manifest[field], './')
        self.assertEqual(self.manifest['display'], 'standalone')
        self.assertTrue(any(i['purpose'] == 'maskable' for i in self.manifest['icons']))

    def test_png_dimensions_and_no_missing_icons(self):
        for name, size in [('apple-touch-icon.png', 180), ('icons/icon-192.png', 192), ('icons/icon-512.png', 512), ('icons/icon-maskable-512.png', 512)]:
            blob = (ROOT / '_site' / name).read_bytes()
            self.assertEqual(blob[:8], b'\x89PNG\r\n\x1a\n')
            self.assertEqual(struct.unpack('>II', blob[16:24]), (size, size))

    def test_all_local_head_links_exist(self):
        for tag, attrs in self.doc.nodes:
            if tag == 'link' and 'href' in attrs:
                href = attrs['href']
                self.assertFalse(href.startswith('/'), href)
                self.assertTrue((ROOT / '_site' / href).is_file(), href)

    def test_mobile_controls_have_all_directions_and_combat(self):
        buttons = [a for tag, a in self.doc.nodes if tag == 'button']
        self.assertEqual(len([b for b in buttons if 'data-move' in b]), 8)
        for action in ['target', 'fire', 'dashmode', 'interact', 'inventory', 'talents', 'journal', 'city', 'craft', 'install']:
            self.assertTrue(any(b.get('data-act') == action for b in buttons), action)

    def test_deployment_does_not_include_source_or_user_data(self):
        files = {str(p.relative_to(ROOT / '_site')).replace('\\', '/') for p in (ROOT / '_site').rglob('*') if p.is_file()}
        self.assertIn('index.html', files)
        self.assertNotIn('src/engine.js', files)
        self.assertFalse(any(p.endswith('.json') for p in files))
        self.assertFalse(any('.git/' in p for p in files))

if __name__ == '__main__':
    unittest.main(verbosity=2)
