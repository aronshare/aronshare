"""Offline integration tests: fixtures exercise the real review/cache/format path.
Only network and AI process seams are mocked; no live publishing imports run.
"""
import ast
import io
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
FRONT=Path('/home/ubuntu/ahhhhfs-astro')
sys.path.insert(0,str(ROOT/'scripts'))
import image_cleanup as gate
import image_ingestion as ingest
import cover_crawler as covers

class IngestionTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.public=self.root/'public'
        self.source=self.root/'source.png'
        image=Image.new('RGB',(800,400),'white')
        ImageDraw.Draw(image).rectangle((40,40,760,360),fill='navy')
        image.save(self.source)
        self.data=self.source.read_bytes()
        env=patch.dict(os.environ,{'ARONSHARE_IMAGE_REVIEW_DIR':str(self.root/'cache'), 'TMPDIR':str(self.root)})
        env.start(); self.addCleanup(env.stop)
        self.store=gate.CleanupStore()

    def clean(self):
        self.store.inspect(self.source,'clean',reviewer='test',note='Synthetic fixture only')

    def test_real_cover_gate_blocks_uninspected_and_preserves_old(self):
        destination=self.root/'cover.webp'; destination.write_bytes(b'old')
        with patch('cover_sources.fetch_bytes',return_value=(self.data,'https://example.com/ui.png','image/png')), patch.object(covers,'apply_letterbox') as render:
            self.assertFalse(covers.generate_cover_for_post('t','c',str(destination),content='![UI](https://example.com/ui.png)'))
            render.assert_not_called()
        self.assertEqual(destination.read_bytes(),b'old')

    def test_reviewed_cover_is_formatted_without_ai(self):
        self.clean()
        destination=self.root/'cover.webp'
        with patch('cover_sources.fetch_bytes',return_value=(self.data,'https://example.com/ui.png','image/png')), patch.object(gate,'run_baoyu') as ai:
            self.assertTrue(covers.generate_cover_for_post('t','c',str(destination),content='![UI](https://example.com/ui.png)'))
            ai.assert_not_called()
        with Image.open(destination) as im: self.assertEqual(im.size,(1200,675))

    def test_body_unreviewed_blocks_all_assets_without_remote_fallback(self):
        with patch.object(ingest,'fetch_bytes',return_value=(self.data,'https://example.com/ui.png','image/png')):
            with self.assertRaises(gate.ReviewRequired):
                ingest.localize_images('Credit: Alice ![UI](/ui.png)',base_url='https://example.com/',public_dir=self.public)
        self.assertFalse(self.public.exists())

    def test_body_html_markdown_and_media_use_reviewed_assets(self):
        self.clean()
        body='Credit: Alice ![UI](https://example.com/ui.png) <img alt="UI" src="https://example.com/ui.png">'
        with patch.object(ingest,'fetch_bytes',return_value=(self.data,'https://example.com/ui.png','image/png')) as fetch, patch.object(gate,'run_baoyu') as ai:
            text,media=ingest.localize_images(body,base_url='https://example.com',public_dir=self.public,media=[{'type':'image','src':'https://example.com/ui.png'}])
            fetch.assert_called_once()
            ai.assert_not_called()
        self.assertIn('Credit: Alice',text)
        self.assertNotIn('https://example.com/ui.png',text)
        self.assertIn(media[0]['src'],text)
        with Image.open(self.public/media[0]['src'].lstrip('/')) as im:
            self.assertEqual(im.size,(800,400))
            self.assertEqual(im.format,'WEBP')

    def test_unsupported_images_fail_closed(self):
        for text in ('![UI][ref]', '<img srcset="a.png 1x">','<picture><source srcset="x"></picture>','![UI](https://e.com/a(b).png)'):
            with self.subTest(text=text), self.assertRaises(gate.CleanupError):
                ingest.localize_images(text,base_url='https://example.com',public_dir=self.public)

    def test_partial_body_approval_never_installs_any_assets(self):
        self.clean()
        second=io.BytesIO(); Image.new('RGB',(800,400),'red').save(second,'PNG')
        with patch.object(ingest,'fetch_bytes',side_effect=[(self.data,'https://e.com/a.png','image/png'),(second.getvalue(),'https://e.com/b.png','image/png')]):
            with self.assertRaises(gate.ReviewRequired):
                ingest.localize_images('![A](https://e.com/a.png) ![B](https://e.com/b.png)',base_url='https://e.com/',public_dir=self.public)
        self.assertFalse(self.public.exists())

    def test_daily_body_failure_skips_post(self):
        text=(ROOT/'scripts/daily_20_pipeline.py').read_text()
        start=text.index('        # Body images and attachments')
        end=text.index('        # 纯文本清理',start)
        snippet='for item in items:\n'+text[start:end]+'        accepted.append(item)\n'
        scope={'items':[dict(id=1,content='![UI](https://example.com/ui.png)',url='https://example.com')], 'ASTRO_DIR':self.root,'log':lambda *a:None,'accepted':[]}
        with patch.object(ingest,'localize_images',side_effect=gate.ReviewRequired('review required')):
            exec(snippet,scope)
        self.assertEqual(scope['accepted'],[])
        self.assertFalse(self.public.exists())

    def test_daily_summary_cannot_bypass_body_gate(self):
        text=(ROOT/'scripts/daily_20_pipeline.py').read_text()
        start=text.index('        # Body images and attachments')
        end=text.index('        # 纯文本清理',start)
        snippet='for item in items:\n'+text[start:end]+'        accepted.append(item)\n'
        scope={'items':[dict(id=1,content='Plain body',summary='![UI](https://example.com/ui.png)',url='https://example.com')], 'ASTRO_DIR':self.root,'log':lambda *a:None,'accepted':[]}
        with patch.object(ingest,'fetch_bytes',return_value=(self.data,'https://example.com/ui.png','image/png')):
            exec(snippet,scope)
        self.assertEqual(scope['accepted'],[])
        self.assertFalse(self.public.exists())

    def helper(self,path,name,scope):
        tree=ast.parse(path.read_text())
        node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name)
        exec(compile(ast.Module(body=[node],type_ignores=[]),str(path),'exec'),scope)
        return scope[name]

    def test_frontend_covers_call_same_gate_and_propagate_failure(self):
        # Extract just function, avoiding DB/env side-effect imports from frontend.
        sys.path.insert(0,str(FRONT)); self.addCleanup(lambda:sys.path.remove(str(FRONT)))
        fn=self.helper(FRONT/'pipeline/covers.py','download',{'__package__':'pipeline','Image':Image})
        with patch.object(ingest,'fetch_bytes',return_value=(self.data,'https://example.com/ui.png','image/png')):
            with self.assertRaises(gate.ReviewRequired): fn('https://example.com/ui.png')
            self.clean()
            self.assertEqual(fn('https://example.com/ui.png').size,(800,400))

    def test_frontend_write_and_enrich_gate_before_post_write(self):
        sys.path.insert(0,str(FRONT)); self.addCleanup(lambda:sys.path.remove(str(FRONT)))
        posts=self.root/'src/content/posts'; posts.mkdir(parents=True)
        scope={'__package__':'pipeline','POSTS_DIR':posts,'category_name':lambda x:x,'template_body':lambda d:'Body','to_frontmatter':lambda d:'title: Test\n'}
        fn=self.helper(FRONT/'pipeline/build.py','write_post',scope)
        data={'category_slug':'apps','media':[{'type':'image','src':'https://example.com/ui.png'}]}
        with self.assertRaises(gate.CleanupError):
            fn('remote', dict(data, cover='https://example.com/dirty.png'))
        self.assertFalse((posts/'remote.md').exists())
        with patch.object(ingest,'fetch_bytes',return_value=(self.data,'https://example.com/ui.png','image/png')):
            with self.assertRaises(gate.ReviewRequired): fn('1',data)
            self.assertFalse((posts/'1.md').exists())
            self.clean(); fn('1',data)
            self.assertTrue((posts/'1.md').exists())
            self.assertEqual(len(list((self.public/'assets/post-images').glob('*.webp'))),1)
        tree=ast.parse((FRONT/'pipeline/enrich.py').read_text())
        self.assertTrue(any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='write_post' for n in ast.walk(tree)))

if __name__ == '__main__': unittest.main()
