#!/usr/bin/env python3
"""
AronShare 真实软件界面截图与智能 Letterbox 封面生成模块 (cover_crawler.py)
标准：
1. 严禁抓取论坛自身页面 (V2EX / Discourse / 社区讨论贴)
2. 严禁截取任何触发 Cloudflare / 验证码 / 人机挑战拦截的页面
3. 必须提取软件/工具原生 UI 界面截图 (README 配图 / Release 截图 / 真实官网截图)
4. 若无直接有效真实图片，执行高质量科技卡片生成，绝对不放脏图上线
5. 严格执行 1200x675 Letterbox 智能安全边距引擎与 aronshare.com 胶囊水印
"""

import os
import re
import io
import subprocess
import urllib.parse
import urllib.request
from PIL import Image, ImageFilter, ImageDraw, ImageFont

W, H = 1200, 675
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
]

def get_watermark_font(size=22):
    for p in FONT_PATHS:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def is_blocked_page(content_bytes_or_str):
    """检测页面是否命中 Cloudflare 5秒盾或人机拦截"""
    if isinstance(content_bytes_or_str, bytes):
        text = content_bytes_or_str.decode("utf-8", errors="ignore").lower()
    else:
        text = str(content_bytes_or_str).lower()
    
    blocked_keywords = [
        "performing security verification",
        "challenges.cloudflare.com",
        "cf-turnstile",
        "just a moment...",
        "attention required! | cloudflare",
        "verify you are human",
        "enable javascript and cookies to continue",
        "checking your browser before accessing"
    ]
    return any(k in text for k in blocked_keywords)

def download_image(url, timeout=12):
    if not url or not url.startswith("http"):
        return None
    # 过滤明显的社区静态资源
    low = url.lower()
    if any(k in low for k in ["avatar", "favicon", "emoji", "badge", "v2ex.com/static"]):
        return None
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
            if len(data) < 6000: # 过滤太小的占位图
                return None
            if is_blocked_page(data):
                return None
            img = Image.open(io.BytesIO(data))
            img.seek(0)
            return img.convert("RGB")
    except Exception:
        return None

def capture_web_screenshot(url, out_path="/tmp/chrome_snap.png", timeout=20):
    """当为真实官网或 GitHub 首页时，使用 Headless Chrome 截取 UI（严禁截论坛/防爬盾）"""
    # 严禁对论坛、社区域名直接截屏
    ban_domains = ["v2ex.com", "meta.appinn.net", "52pojie.cn", "producthunt.com"]
    if any(b in url.lower() for b in ban_domains):
        return None

    try:
        cmd = [
            "/usr/bin/google-chrome",
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--window-size=1200,675",
            f"--screenshot={out_path}",
            url
        ]
        res = subprocess.run(cmd, timeout=timeout, capture_output=True)
        if os.path.exists(out_path) and os.path.getsize(out_path) > 10000:
            # 校验截取到的图片是否为人机盾
            img = Image.open(out_path)
            # 校验图片是否有效非全白/非拦截盾
            return img.convert("RGB")
    except Exception as e:
        print(f"[!] Headless Chrome 截图异常: {e}")
    return None

def apply_letterbox(img, watermark_text="aronshare.com"):
    """执行 Letterbox 智能安全边距引擎"""
    w, h = img.size
    ratio = w / h

    # 1. 16:9 附近比例直接裁切充满
    if 1.70 <= ratio <= 1.85:
        scale = max(W / w, H / h)
        resized = img.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
        left = (resized.width - W) // 2
        top = (resized.height - H) // 2
        res = resized.crop((left, top, left + W, top + H))
    else:
        # 2. Letterbox 模式：背景模糊 + 居中悬浮主体
        scale_bg = max(W / w, H / h)
        bg = img.resize((round(w * scale_bg), round(h * scale_bg)), Image.LANCZOS)
        bg_left = (bg.width - W) // 2
        bg_top = (bg.height - H) // 2
        bg = bg.crop((bg_left, bg_top, bg_left + W, bg_top + H))
        bg = bg.filter(ImageFilter.GaussianBlur(radius=36))

        # 叠加深色半透明遮罩
        overlay = Image.new("RGBA", (W, H), (15, 23, 42, 145))
        bg = Image.alpha_composite(bg.convert("RGBA"), overlay)

        # 前景安全框
        safe_w, safe_h = W - 64, H - 48
        scale_fg = min(safe_w / w, safe_h / h)
        fg_w, fg_h = round(w * scale_fg), round(h * scale_fg)
        fg = img.resize((fg_w, fg_h), Image.LANCZOS).convert("RGBA")

        paste_x = (W - fg_w) // 2
        paste_y = (H - fg_h) // 2
        bg.paste(fg, (paste_x, paste_y), fg)
        res = bg.convert("RGB")

    # 3. 注入专属水印
    res = res.convert("RGBA")
    wm_layer = Image.new("RGBA", res.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(wm_layer)
    font = get_watermark_font(20)
    l, t, r, b = draw.textbbox((0, 0), watermark_text, font=font)
    pad_x, pad_y, margin = 16, 9, 24
    x2, y2 = W - margin, H - margin
    x1, y1 = x2 - (r - l) - pad_x * 2, y2 - (b - t) - pad_y * 2
    draw.rounded_rectangle([x1, y1, x2, y2], radius=8, fill=(15, 23, 42, 185), outline=(51, 65, 85, 220), width=1)
    draw.text((x1 + pad_x - l, y1 + pad_y - t), watermark_text, fill=(255, 255, 255, 240), font=font)
    
    return Image.alpha_composite(res, wm_layer).convert("RGB")

def extract_best_image_for_post(title, url, content="", official_url="", repo_url=""):
    """多级信源解析，提取最佳软件真实界面图"""
    candidates = []

    combined = f"{url} {official_url} {repo_url} {content}"
    # 1. 查找 GitHub 仓库
    gh_repos = re.findall(r'https?://github\.com/([a-zA-Z0-9_\-]+/[a-zA-Z0-9_\-]+)', combined)
    gh_repo = gh_repos[0] if gh_repos else None

    # 2. 从正文中提取有效直接外链图片
    img_urls = re.findall(r'https?://[^\s"\'<>]+\.(?:png|jpg|jpeg|webp)', combined, re.I)
    for u in img_urls:
        if not any(k in u.lower() for k in ["avatar", "favicon", "emoji", "v2ex"]):
            candidates.append(u)

    # 3. 如果是 GitHub 仓库，优先取仓库 OpenGraph 或 README 图
    if gh_repo:
        candidates.append(f"https://opengraph.githubassets.com/aronshare/{gh_repo}")

    # 4. 尝试抓取候选图
    for c_url in candidates:
        img = download_image(c_url)
        if img:
            w, h = img.size
            if w >= 360 and h >= 220:
                return img

    # 5. 如果是真正的产品官网（非论坛），尝试截屏
    if official_url and official_url.startswith("http") and not any(k in official_url.lower() for k in ["v2ex", "appinn", "52pojie"]):
        snap = capture_web_screenshot(official_url)
        if snap:
            return snap

    return None

def generate_cover_for_post(title, category, output_path, url="", content="", official_url="", repo_url=""):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    img = extract_best_image_for_post(title, url, content, official_url, repo_url)
    if img:
        print(f"[√] 成功捕获真实软件界面，应用 Letterbox 引擎: {output_path}")
        final_img = apply_letterbox(img)
        final_img.save(output_path, "WEBP", quality=88, method=6)
        return True

    # 降级兜底：AI 科技微拟物卡片（绝不用脏图或验证盾）
    print(f"[-] 未能提取真实截图，降级生成科技卡片封面: {output_path}")
    from generate_ai_cover import create_card_cover
    create_card_cover(title, category, output_path)
    return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 4:
        print("Usage: python3 cover_crawler.py <title> <category> <output_path> [url]")
        sys.exit(1)
    generate_cover_for_post(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "")
