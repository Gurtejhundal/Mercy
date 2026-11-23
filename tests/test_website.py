"""Static deployment integrity; no server or external requests required."""
from html.parser import HTMLParser
from pathlib import Path
import unittest
from urllib.parse import urlsplit, unquote

PUBLIC=Path(__file__).resolve().parents[1]/'public'
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__();self.links=[];self.ids=set();self.feed(text)
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if attrs.get('id'):self.ids.add(attrs['id'])
        for key in ['src','href']:
            if attrs.get(key):self.links.append(attrs[key])

class WebsiteTests(unittest.TestCase):
    def test_local_assets_and_page_anchors_resolve(self):
        for file in ['index.html','demo.html']:
            page=Page((PUBLIC/file).read_text())
            for ref in page.links:
                parsed=urlsplit(ref)
                if parsed.scheme or parsed.netloc:continue
                if parsed.path:
                    target=(PUBLIC/unquote(parsed.path)).resolve()
                    self.assertTrue(target.is_relative_to(PUBLIC.resolve()))
                    self.assertTrue(target.is_file(),ref)
                elif parsed.fragment:self.assertIn(parsed.fragment,page.ids)

    def test_teacher_and_font_are_packaged_for_the_offline_report(self):
        assets=PUBLIC.parent/'mercy/assets'
        for file in ['teacher.webp','notebook.ttf','OFL.txt']:
            self.assertEqual((PUBLIC/'assets'/file).read_bytes(),(assets/file).read_bytes())
        self.assertIn('that one teacher we all know',(PUBLIC/'index.html').read_text())
        self.assertIn('that one teacher we all know',(PUBLIC/'demo.html').read_text())

if __name__=='__main__':unittest.main()
