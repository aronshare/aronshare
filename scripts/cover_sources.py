"""Real source images only. Bounded, public-IP-pinned HTTP; no browser fallback."""
import html
import http.client
import ipaddress
import json
import re
import socket
import ssl
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit
from PIL import Image, ImageStat

USER_AGENT = 'AronShare-Cover/1.0'
MAX_BYTES = 20 * 1024 * 1024


def public_addresses(url):
    p = urlsplit(url)
    if p.scheme not in ('http', 'https') or not p.hostname or p.username or p.password or p.port not in (None, 80, 443):
        raise ValueError('Only public HTTP(S) URLs on standard ports are allowed')
    addresses = socket.getaddrinfo(p.hostname, p.port or (443 if p.scheme == 'https' else 80), type=socket.SOCK_STREAM)
    if not addresses or any(not ipaddress.ip_address(a[4][0]).is_global for a in addresses):
        raise ValueError('Non-public destination refused')
    return p, addresses


def fetch_bytes(url, limit=MAX_BYTES):
    """Resolve once per hop, connect to that exact IP, retain TLS hostname checks."""
    for _ in range(6):
        p, addresses = public_addresses(url)
        conn = http.client.HTTPConnection(p.hostname, p.port or (443 if p.scheme == 'https' else 80), timeout=12)
        try:
            address = addresses[0]
            sock = socket.socket(address[0], address[1], address[2])
            conn.sock = sock
            sock.settimeout(12)
            sock.connect(address[4])
            if p.scheme == 'https':
                conn.sock = ssl.create_default_context().wrap_socket(sock, server_hostname=p.hostname)
            conn.request('GET', urlunsplit(('', '', p.path or '/', p.query, '')), headers={'User-Agent': USER_AGENT, 'Accept-Encoding': 'identity'})
            response = conn.getresponse()
            if response.status in (301, 302, 303, 307, 308):
                location = response.getheader('Location')
                if not location:
                    raise ValueError('Redirect without location')
                url = urljoin(url, location)
                continue
            if response.status != 200:
                raise ValueError(f'HTTP {response.status}')
            data = response.read(limit + 1)
            if len(data) > limit:
                raise ValueError('Response too large')
            return data, url, response.getheader('Content-Type', '')
        finally:
            conn.close()
    raise ValueError('Too many redirects')


def is_blocked_or_forum(url, html_text=''):
    host = (urlsplit(url).hostname or '').lower()
    if not host or any(host == h or host.endswith('.'+h) for h in ('v2ex.com','hostloc.com','nodeseek.com','linux.do')):
        return True
    text = html_text.lower()
    if any(k in text for k in ('performing security verification','challenges.cloudflare.com','cf-turnstile','just a moment','attention required!','enable javascript and cookies','verify you are human','checking your browser')):
        return True
    title = re.search(r'<title[^>]*>(.*?)</title>', text, re.S)
    return bool(title and any(k in title[1] for k in ('404','403','500','502','503','not found','access denied','forbidden','error','unavailable')))


def usable_image_url(url):
    p = urlsplit(url)
    name = (p.path + ' ' + p.netloc).lower()
    if p.scheme not in ('https', 'http'):
        return False
    if p.hostname in ('aronshare.com', 'www.aronshare.com'):
        return False
    return not any(k in name for k in ('opengraph.githubassets.com','github.githubassets.com','avatars.githubusercontent.com','shields.io','badge','avatar','favicon','logo','/icon','/social','/og','/cover_','star-history','openomy.com','/widgets/','sponsor'))


class Images(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
        self.meta = []
    def handle_starttag(self, tag, attrs):
        a = {key: value or '' for key, value in attrs}
        if tag == 'img':
            if any(a.get(key, '').isdigit() and int(a[key]) < minimum for key, minimum in (('width', 320), ('height', 180))):
                return
            label = ' '.join(a.get(k, '') for k in ('alt','class','id')).lower()
            if not any(k in label for k in ('logo','badge','avatar','icon')):
                value = a.get('data-src') or a.get('src')
                if value:
                    self.images.append(value)
                elif a.get('srcset'):
                    self.images.append(a['srcset'].split(',')[-1].strip().split()[0])
        if tag == 'meta' and (a.get('property') or a.get('name')) in ('og:image','twitter:image') and a.get('content'):
            self.meta.append(a['content'])


def image_candidates(text, base_url, include_meta=False):
    # Descriptive labels can identify opaque logo/CDN URLs with no useful filename.
    text = re.sub(r'!\[[^\]]*(?:logo|badge|avatar|icon|sponsor)[^\]]*\]\([^\n]*?\)', '', text or '', flags=re.I)
    parser = Images()
    parser.feed(text or '')
    markdown = re.findall(r'!\[[^\]]*\]\(\s*(<[^>]+>|[^\s)]+)(?:\s+["\'][^\n]*?["\'])?\s*\)', text or '')
    refs = dict(re.findall(r'^\s*\[([^\]]+)\]:\s*(\S+)', text or '', re.M))
    markdown += [refs[k] for k in re.findall(r'!\[[^\]]*\]\[([^\]]+)\]', text or '') if k in refs]
    # Preserve signed/query URLs; absolute image URLs in plain-text feeds are valid too.
    plain_text = re.sub(r'<[^>]*>', '', text or '')
    plain = re.findall(r'https?://[^\s"\'<>]+', plain_text)
    plain = [u.rstrip(').,') for u in plain if re.search(r'\.(png|jpe?g|webp|gif)(?:\?|$)', u, re.I)]
    result = []
    for value in markdown + parser.images + (parser.meta if include_meta else []) + plain:
        url = urljoin(base_url, html.unescape(value.strip('<>')))
        p = urlsplit(url)
        if p.hostname == 'github.com' and '/blob/' in p.path:
            url = urlunsplit(('https','raw.githubusercontent.com',p.path.replace('/blob/', '/', 1),p.query,''))
        if usable_image_url(url) and url not in result:
            result.append(url)
    return result


def download_image(img_url, temp_path, provenance=None):
    try:
        if not usable_image_url(img_url):
            return False
        data, final_url, _ = fetch_bytes(img_url)
        if not usable_image_url(final_url):
            return False
        import io
        with Image.open(io.BytesIO(data)) as im:
            if im.width < 320 or im.height < 180 or im.width * im.height > 40_000_000:
                return False
            im.load()
            if max(ImageStat.Stat(im.convert('RGB')).stddev) < 5:
                return False
        Path(temp_path).write_bytes(data)
        if provenance is not None:
            provenance.update(image_url=img_url, resolved_image_url=final_url)
        return True
    except Exception:
        return False


def extract_github_preview(github_url, temp_path, provenance=None):
    p = urlsplit(github_url)
    if p.hostname != 'github.com':
        return False
    parts = p.path.strip('/').split('/')
    if len(parts) < 2:
        return False
    owner, repo = parts[:2]
    repo = repo.removesuffix('.git')
    urls = []
    try:
        raw, _, _ = fetch_bytes(f'https://api.github.com/repos/{owner}/{repo}/readme', 2_000_000)
        info = json.loads(raw)
        if info.get('download_url'):
            urls.append(info['download_url'])
    except Exception:
        pass
    urls += [f'https://raw.githubusercontent.com/{owner}/{repo}/{branch}/README.md' for branch in ('main','master')]
    for readme_url in dict.fromkeys(urls):
        try:
            data, final_url, _ = fetch_bytes(readme_url, 2_000_000)
            text = data.decode('utf-8', errors='replace')
            if is_blocked_or_forum(final_url, text):
                continue
            for candidate in image_candidates(text, final_url):
                if download_image(candidate, temp_path, provenance):
                    if provenance is not None:
                        provenance.update(kind='github-readme', page_url=final_url)
                    return True
        except Exception:
            continue
    return False


def extract_page_preview(url, temp_path, provenance=None):
    # Never screenshot/extract GitHub's generic site cards as a product image.
    if is_blocked_or_forum(url) or urlsplit(url).hostname == 'github.com':
        return False
    try:
        data, final_url, mime = fetch_bytes(url, 4_000_000)
        if mime.startswith('image/'):
            return download_image(final_url, temp_path, provenance)
        text = data.decode('utf-8', errors='replace')
        if is_blocked_or_forum(final_url, text) or urlsplit(final_url).hostname == 'github.com':
            return False
        for candidate in image_candidates(text, final_url, include_meta=True):
            if download_image(candidate, temp_path, provenance):
                if provenance is not None:
                    provenance.update(kind='page-image', page_url=final_url)
                return True
    except Exception:
        pass
    return False


def capture_with_chrome(url, temp_path):
    """Fail closed: unsandboxed Chrome cannot safely constrain all network hops.

    No stale file is inspected/reused. Use extracted product screenshots instead.
    """
    return False
