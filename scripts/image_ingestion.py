"""Localize body/attachment images only after mandatory visual-review gate.

Conservative Markdown/HTML subset; unsupported image markup blocks the post
rather than leaving an unreviewed remote image in publishable article content.
Source credit and ordinary links/text are never removed.
"""
import html
import io
from pathlib import Path
import re
import tempfile
from urllib.parse import urljoin, urlsplit, unquote
from PIL import Image
from cover_sources import fetch_bytes
from image_cleanup import CleanupError, prepare_image, atomic_write, digest, scratch_root

MD_IMAGE = re.compile(r'!\[([^\]\n]*)\]\(\s*(<[^>\n]+>|[^\s()]+)(\s+["\'][^\n]*?["\'])?\s*\)')
HTML_IMAGE = re.compile(r'<img\b[^>]*>', re.I)
SRC = re.compile(r'(?<![\w-])src\s*=\s*(["\'])(.*?)\1', re.I|re.S)


def acquire_image(url, base_url, public_dir, work):
    """Preserve exact acquired bytes for content-keyed inspection/cache."""
    public_dir = Path(public_dir).resolve()
    parsed = urlsplit(url)
    if not parsed.netloc and parsed.path.startswith(('/assets/', '/covers/')):
        source = (public_dir/unquote(parsed.path).lstrip('/')).resolve()
        if not source.is_relative_to(public_dir) or not source.is_file():
            raise CleanupError(f'Missing/unsafe local image: {url}')
        data = source.read_bytes()
    else:
        data, _, _ = fetch_bytes(urljoin(base_url, html.unescape(url)))
    original = Path(work)/f'{digest(data)}.img'
    original.write_bytes(data)
    return original


def localize_images(content, *, base_url, public_dir, media=None):
    """Return (body, media); failure raises before writing ANY image/post.

    Attachments with type=image, inline Markdown and quoted-src HTML img are
    supported. Responsive/embedded image syntax fails closed for manual review.
    """
    public_dir = Path(public_dir)
    staged = {}
    mapping = {}
    attachments = [dict(item) for item in (media or [])]
    if re.search(r'<(?:picture|source|svg|object|embed|iframe|input)\b|\b(?:srcset|data-src|poster)\s*=|url\s*\(', content, re.I):
        raise CleanupError('Unsupported embedded/responsive image markup; manual localization required')
    with tempfile.TemporaryDirectory(prefix='aronshare-body-', dir=scratch_root()) as work:
        def localize(url):
            url = html.unescape(url.strip('<>'))
            if url in mapping: return mapping[url]
            original = acquire_image(url, base_url, public_dir, work)
            reviewed = prepare_image(original)
            # Body aspect/layout is retained: no cover crop, no new branding.
            stream = io.BytesIO()
            with Image.open(reviewed) as image:
                image.convert('RGBA' if 'A' in image.getbands() else 'RGB').save(stream, 'WEBP', quality=95)
            data = stream.getvalue()
            name = f'/assets/post-images/reviewed_{digest(data)}.webp'
            staged[name] = data
            mapping[url] = name
            return name
        # Fail closed for reference/shortcut images rather than a partial regex rewrite.
        stripped = MD_IMAGE.sub('', content)
        if '![' in stripped:
            raise CleanupError('Unsupported Markdown image syntax; use inline ![alt](URL) before ingestion')
        def markdown(match):
            return f'![{match[1]}]({localize(match[2])}{match[3] or ""})'
        result = MD_IMAGE.sub(markdown, content)
        def image_tag(match):
            tag = match[0]
            sources = list(SRC.finditer(tag))
            if len(sources) != 1:
                raise CleanupError('HTML img requires exactly one quoted src')
            source = sources[0]
            return tag[:source.start(2)]+localize(source[2])+tag[source.end(2):]
        result = HTML_IMAGE.sub(image_tag, result)
        for item in attachments:
            if item.get('type') == 'image':
                if not item.get('src'): raise CleanupError('Image attachment missing src')
                if item.get('srcset'): raise CleanupError('Attachment srcset requires explicit review')
                item['src'] = localize(item['src'])
        # Only reviewed images can reach public/. Post writers are called afterward.
        for name, data in staged.items():
            atomic_write(public_dir/name.lstrip('/'), data)
    return result, attachments
