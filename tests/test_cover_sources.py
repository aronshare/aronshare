"""Offline cover regression suite; never imports publishing modules."""
import ast
import importlib.machinery
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import cover_crawler as c

class CoverTests(unittest.TestCase):
    def test_template_module_and_compiled_files_are_absent(self):
        scripts = ROOT / 'scripts'
        self.assertEqual(list(scripts.rglob('generate_ai_cover*')), [])
        self.assertIsNone(importlib.machinery.PathFinder.find_spec(
            'generate_ai_cover', [str(scripts)]))

    def test_no_template_callable_or_reference_in_active_scripts(self):
        import cover_sources as sources
        for module in (c, sources):
            self.assertFalse(hasattr(module, 'create_card_cover'))
        for path in (ROOT / 'scripts').rglob('*.py'):
            with self.subTest(path=path.relative_to(ROOT)):
                source = path.read_text(encoding='utf-8')
                self.assertNotIn('generate_ai_cover', source)
                self.assertNotIn('create_card_cover', source)

    def test_entrypoints_import_and_call_real_crawler(self):
        for filename in ('daily_20_pipeline.py', 'aronshare_master_pipeline.py'):
            with self.subTest(entrypoint=filename):
                tree = ast.parse((ROOT / 'scripts' / filename).read_text())
                imports = [node for node in ast.walk(tree)
                           if isinstance(node, ast.ImportFrom)
                           and node.module == 'cover_crawler']
                self.assertTrue(any(alias.name == 'generate_cover_for_post'
                                    for node in imports for alias in node.names))
                self.assertTrue(any(isinstance(node, ast.Call)
                                    and isinstance(node.func, ast.Name)
                                    and node.func.id == 'generate_cover_for_post'
                                    for node in ast.walk(tree)))

    def test_without_source_never_renders_a_template(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / 'cover.webp'
            with patch.object(c, 'apply_letterbox') as render:
                self.assertFalse(c.generate_cover_for_post('Title', 'Tool', str(out)))
                render.assert_not_called()
            self.assertFalse(out.exists())

    def test_relative_html_and_query(self):
        text = '![UI](./screens/ui.png?raw=1&size=2) <img src="../demo.webp?token=x&amp;y=z">'
        self.assertEqual(c.image_candidates(text, 'https://raw.githubusercontent.com/o/r/dev/docs/README.md'), [
            'https://raw.githubusercontent.com/o/r/dev/docs/screens/ui.png?raw=1&size=2',
            'https://raw.githubusercontent.com/o/r/dev/demo.webp?token=x&y=z'])

    def test_no_github_social_fallback(self):
        with tempfile.TemporaryDirectory() as d, patch.object(c, 'download_image', return_value=True) as download, patch('urllib.request.urlopen', side_effect=OSError('offline')):
            # The hardened fetch seam is patched as well when available.
            with patch('cover_sources.fetch_bytes', side_effect=OSError('offline')):
                self.assertFalse(c.extract_github_preview('https://github.com/o/r', str(Path(d)/'x')))
            download.assert_not_called()

    def test_failure_preserves_existing(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d)/'old.webp'
            out.write_bytes(b'original')
            self.assertFalse(c.generate_cover_for_post('t','c',str(out)))
            self.assertEqual(out.read_bytes(), b'original')

    def test_daily_passes_stored_content(self):
        tree = ast.parse((ROOT/'scripts/daily_20_pipeline.py').read_text())
        call = next(n for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id=='generate_cover_for_post')
        value = next(k.value for k in call.keywords if k.arg=='content')
        self.assertEqual(eval(compile(ast.Expression(value), '<test>', 'eval'), {'item': {'content':'actual image'}}), 'actual image')

    def test_challenge_and_error(self):
        for html in ['<title>Just a moment...</title>', '<title>404 Not Found</title>', '<title>Access denied</title>']:
            self.assertTrue(c.is_blocked_or_forum('https://example.com', html))

    def test_private_network_refused(self):
        import cover_sources as s
        for url in ('http://127.0.0.1/x', 'http://[::1]/', 'http://169.254.169.254/', 'file:///etc/passwd', 'https://example.com:9443/', 'http://user:pass@example.com/'):
            with self.assertRaises((ValueError, OSError)):
                s.public_addresses(url)
        with patch('socket.getaddrinfo', return_value=[(2,1,6,'',('10.1.2.3',80))]):
            with self.assertRaises(ValueError):
                s.public_addresses('http://rebind.example/')

    def test_social_and_logo_urls_refused(self):
        import cover_sources as s
        for url in ('https://opengraph.githubassets.com/hash/o/r', 'https://github.githubassets.com/assets/github-logo.png', 'https://aronshare.com/covers/x.webp', 'https://api.star-history.com/chart'):
            self.assertFalse(s.usable_image_url(url))
        self.assertEqual(s.image_candidates('<img width="100" height="100" src="/opaque.png"><img alt="logo" src="/opaque2.png">', 'https://example.com/'), [])

    def test_official_images_before_social(self):
        import cover_sources as s
        body = b'<meta content="/og.png" property="og:image"><img src="/screenshots/app.webp?key=a&amp;b=c">'
        with patch.object(s, 'fetch_bytes', return_value=(body,'https://example.com/','text/html')), patch.object(s, 'download_image', return_value=True) as download:
            self.assertTrue(s.extract_page_preview('https://example.com/', 'unused'))
            self.assertEqual(download.call_args.args[0], 'https://example.com/screenshots/app.webp?key=a&b=c')

    def test_challenge_never_downloads(self):
        import cover_sources as s
        with patch.object(s,'fetch_bytes',return_value=(b'<title>Just a moment...</title><img src="/app.png">','https://example.com/','text/html')), patch.object(s,'download_image') as download:
            self.assertFalse(s.extract_page_preview('https://example.com/', 'unused'))
            download.assert_not_called()

    def test_github_default_branch_relative(self):
        import cover_sources as s
        replies = [(b'{"download_url":"https://raw.githubusercontent.com/o/r/develop/docs/README.md"}', 'https://api.github.com/repos/o/r/readme', 'application/json'), (b'<img src="../screens/app.png?raw=1">','https://raw.githubusercontent.com/o/r/develop/docs/README.md','text/plain')]
        with patch.object(s,'fetch_bytes',side_effect=replies), patch.object(s,'download_image',return_value=True) as download:
            self.assertTrue(s.extract_github_preview('https://github.com/o/r', 'unused'))
            self.assertEqual(download.call_args.args[0], 'https://raw.githubusercontent.com/o/r/develop/screens/app.png?raw=1')

    def test_stale_screenshot_not_accepted(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'old.png'; p.write_bytes(b'stale')
            self.assertFalse(c.capture_with_chrome('https://example.com', str(p)))

    def test_real_pixels_letterbox_and_atomic_failure(self):
        import cover_sources as s
        im = Image.new('RGB',(800,400),'white')
        from PIL import ImageDraw
        ImageDraw.Draw(im).rectangle((100,50,700,350),fill='navy')
        stream=io.BytesIO(); im.save(stream,'PNG')
        with tempfile.TemporaryDirectory() as d, patch.object(s,'fetch_bytes',return_value=(stream.getvalue(),'https://example.com/app.png','image/png')), patch('image_cleanup.prepare_image', side_effect=lambda p: Path(p)):
            p=Path(d)/'new.webp'; provenance={}
            self.assertTrue(c.generate_cover_for_post('t','c',str(p),content='![UI](https://example.com/app.png)',provenance=provenance))
            with Image.open(p) as result:
                self.assertEqual(result.size,(1200,675))
                self.assertEqual(result.format,'WEBP')
            self.assertEqual(provenance['image_url'],'https://example.com/app.png')
            before=p.read_bytes()
            with patch.object(c,'apply_letterbox',return_value=False):
                self.assertFalse(c.generate_cover_for_post('t','c',str(p),content='![UI](https://example.com/app.png)'))
            self.assertEqual(p.read_bytes(),before)

    def test_download_invalid_and_tiny_images(self):
        import cover_sources as s
        stream=io.BytesIO(); Image.new('RGB',(10,10)).save(stream,'PNG')
        for data in (b'<html>error</html>',stream.getvalue()):
            with patch.object(s,'fetch_bytes',return_value=(data,'https://example.com/a.png','image/png')):
                self.assertFalse(s.download_image('https://example.com/a.png','unused'))

    def master_helper(self):
        tree=ast.parse((ROOT/'scripts/aronshare_master_pipeline.py').read_text())
        helper=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='ensure_real_cover')
        import re
        scope={'re':re,'Path':Path,'log':lambda *a:None}
        exec(compile(ast.Module(body=[helper],type_ignores=[]),'<master-helper>','exec'),scope)
        return scope['ensure_real_cover']

    def test_master_cover_failure_does_not_write(self):
        helper=self.master_helper()
        with tempfile.TemporaryDirectory() as d, patch.object(c,'generate_cover_for_post',return_value=False):
            p=Path(d)/'post.md'; text='---\ntitle: "Test"\ncover: ""\nrepo_url: https://github.com/o/r\n---\nBody'
            p.write_text(text)
            self.assertFalse(helper(p,Path(d)/'covers'))
            self.assertEqual(p.read_text(),text)

    def test_master_success_inserts_cover_and_existing_untouched(self):
        helper=self.master_helper()
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'post.md'; p.write_text('---\ntitle: Test\nsource_url: https://example.com\n---\nBody')
            covers=Path(d)/'covers'; covers.mkdir()
            def generate(*args,**kwargs):
                Path(args[2]).write_bytes(b'fixture-image'); return True
            with patch.object(c,'generate_cover_for_post',side_effect=generate) as generate_mock:
                self.assertTrue(helper(p,covers))
                self.assertIn('cover: "/covers/cover_post.webp"',p.read_text())
                self.assertTrue(helper(p,covers))
                self.assertEqual(generate_mock.call_count,1)

    def test_master_existing_cover_with_cache_query(self):
        helper = self.master_helper()
        with tempfile.TemporaryDirectory() as d, patch.object(c, 'generate_cover_for_post') as generate:
            covers = Path(d) / 'covers'; covers.mkdir()
            (covers / 'cover_11685.webp').write_bytes(b'existing-real-image')
            post = Path(d) / '11685.md'
            text = '---\ntitle: PicPick\ncover: /covers/cover_11685.webp?v=ui_letterbox_v2\n---\nBody'
            post.write_text(text)
            self.assertTrue(helper(post, covers))
            self.assertEqual(post.read_text(), text)
            generate.assert_not_called()

    def test_daily_failed_cover_gate(self):
        text=(ROOT/'scripts/daily_20_pipeline.py').read_text()
        start=text.index('        cover_filename =')
        end=text.index('        # 纯文本清理',start)
        snippet='for item in items:\n'+text[start:end]+'        accepted.append(item)\n'
        with tempfile.TemporaryDirectory() as d, patch.object(c,'generate_cover_for_post',return_value=False):
            scope={'items':[dict(id=1,title='t',category='c',url='https://example.com',content='actual')], 'astro_covers_dir':Path(d),'log':lambda *a:None,'accepted':[]}
            # An existing stale file cannot override an explicit False result.
            (Path(d)/'cover_1.webp').write_bytes(b'stale')
            exec(snippet,scope)
            self.assertEqual(scope['accepted'],[])

    def test_redirect_to_private_is_blocked_before_connect(self):
        import cover_sources as s
        from unittest.mock import MagicMock
        response=MagicMock(status=302)
        response.getheader.return_value='http://127.0.0.1/secret'
        connection=MagicMock(); connection.getresponse.return_value=response
        with patch.object(s.socket,'getaddrinfo',side_effect=[[(2,1,6,'',('93.184.216.34',80))],[(2,1,6,'',('127.0.0.1',80))]]), patch.object(s.socket,'socket') as sock, patch.object(s.http.client,'HTTPConnection',return_value=connection):
            with self.assertRaises(ValueError):
                s.fetch_bytes('http://example.com/start')
            self.assertEqual(sock.call_count,1)
            sock.return_value.connect.assert_called_once_with(('93.184.216.34',80))

    def test_unique_temp_paths_follow_tmpdir(self):
        import os
        seen=[]
        def fail_download(url,path,details):
            seen.append(path); return False
        with tempfile.TemporaryDirectory() as d, patch.dict(os.environ,{'TMPDIR':d}), patch.object(c,'download_image',side_effect=fail_download):
            for _ in range(2):
                self.assertFalse(c.generate_cover_for_post('t','c',str(Path(d)/'x.webp'),content='![UI](https://example.com/app.png)'))
            self.assertEqual(len(set(seen)),2)
            self.assertTrue(all(Path(p).is_relative_to(d) for p in seen))
            self.assertTrue(all(not Path(p).parent.exists() for p in seen))


if __name__ == '__main__':
    unittest.main()
