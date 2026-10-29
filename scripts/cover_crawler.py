#!/usr/bin/env python3
"""
AronShare 真实软件界面截图与智能 Letterbox 封面生成模块 (cover_crawler.py)
标准：
1. 严禁抓取论坛自身页面 (V2EX / Discourse / 社区)，检测到防爬盾 (Cloudflare 等) 绝不使用
2. 优先提取真实软件界面截屏、官方 UI 或 GitHub 真实截图
3. 若为 GitHub 仓库，提取其 Releases/README 中的真实操作 UI 图，或官方 OpenGraph
4. 使用 Pillow 智能 Letterbox：原图完整置中 + 背景高斯模糊弥散光晕 + 安全边距 + aronshare.com 胶囊水印
"""

import os
import sys
import re
import urllib.request
import subprocess
from pathlib import Path
from PIL import Image, ImageFilter, ImageDraw, ImageFont

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
BOT_CHALLENGE_KEYWORDS = [
    "performing security verification",
    "challenges.cloudflare.com",
    "cf-turnstile",
    "just a moment...",
    "attention required! | cloudflare",
    "enable javascript and cookies"
]

def is_blocked_or_forum(url: str, html_text: str = "") -> bool:
    if not url:
        return True
    url_lower = url.lower()
    # 绝对禁止针对论坛自身进行截屏
    if any(k in url_lower for k in ["v2ex.com", "hostloc.com", "nodeseek.com", "linux.do"]):
        return True
    if html_text:
        text_lower = html_text.lower()
        if any(k in text_lower for k in BOT_CHALLENGE_KEYWORDS):
            return True
    return False

def download_image(img_url: str, temp_path: str) -> bool:
    if not img_url or not img_url.startswith("http"):
        return False
    try:
        req = urllib.request.Request(img_url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = resp.read()
            if len(data) < 5000:  # 过滤小图标、追踪像素
                return False
            with open(temp_path, "wb") as f:
                f.write(data)
        with Image.open(temp_path) as im:
            w, h = im.size
            if w < 200 or h < 150:
                return False
        return True
    except Exception:
        return False

def extract_github_preview(github_url: str, temp_path: str) -> bool:
    """从 GitHub 仓库提取 README UI 截图或 OpenGraph 卡片"""
    match = re.search(r"github\.com/([^/]+)/([^/#\?]+)", github_url)
    if not match:
        return False
    owner, repo = match.group(1), match.group(2)
    repo = repo.replace(".git", "")

    # 1. 尝试从 raw README 中提取 UI 截图
    for branch in ["main", "master"]:
        readme_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/README.md"
        try:
            req = urllib.request.Request(readme_url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=8) as resp:
                text = resp.read().decode("utf-8", errors="ignore")
                imgs = re.findall(r'https?://[^\s"\'<>]+\.(?:png|jpg|jpeg|webp)', text, re.I)
                clean = [
                    i for i in imgs 
                    if not any(k in i.lower() for k in ["badge", "shields.io", "travis", "workflow", "avatar", "icon", "license"])
                ]
                for candidate in clean:
                    if download_image(candidate, temp_path):
                        return True
        except Exception:
            continue

    # 2. 尝试从网页抓取 og:image
    try:
        repo_page = f"https://github.com/{owner}/{repo}"
        req = urllib.request.Request(repo_page, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
            ogs = re.findall(r'property=[\'"]og:image[\'"]\s+content=[\'"]([^\'"]+)[\'"]', html)
            if ogs and download_image(ogs[0], temp_path):
                return True
    except Exception:
        pass

    # 3. 兜底尝试 OpenGraph CDN 链接
    og_fallback = f"https://opengraph.githubassets.com/aronshare/{owner}/{repo}"
    if download_image(og_fallback, temp_path):
        return True

    return False

def capture_with_chrome(url: str, temp_path: str) -> bool:
    if is_blocked_or_forum(url):
        return False
    cmd = [
        "/usr/bin/google-chrome",
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--window-size=1200,675",
        f"--screenshot={temp_path}",
        url
    ]
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20)
        if res.returncode == 0 and os.path.exists(temp_path) and os.path.getsize(temp_path) > 10000:
            return True
    except Exception:
        pass
    return False

def apply_letterbox(src_img_path: str, output_path: str, target_size=(1200, 675)) -> bool:
    try:
        with Image.open(src_img_path) as im:
            im = im.convert("RGBA")
            orig_w, orig_h = im.size

            # 1. 生成弥散光晕背景
            bg = im.copy()
            bg_scale = max(target_size[0] / orig_w, target_size[1] / orig_h)
            bg_w, bg_h = int(orig_w * bg_scale), int(orig_h * bg_scale)
            bg = bg.resize((bg_w, bg_h), Image.Resampling.LANCZOS)
            
            # 居中裁剪到 1200x675
            left = (bg_w - target_size[0]) // 2
            top = (bg_h - target_size[1]) // 2
            bg = bg.crop((left, top, left + target_size[0], top + target_size[1]))
            # 施加高斯模糊和微暗压底
            bg = bg.filter(ImageFilter.GaussianBlur(radius=30))
            
            overlay = Image.new("RGBA", target_size, (15, 23, 42, 140))
            bg = Image.alpha_composite(bg, overlay)

            # 2. 计算中心主体等比缩放
            margin_x, margin_y = 60, 45
            avail_w = target_size[0] - margin_x * 2
            avail_h = target_size[1] - margin_y * 2

            fit_scale = min(avail_w / orig_w, avail_h / orig_h)
            new_w, new_h = int(orig_w * fit_scale), int(orig_h * fit_scale)
            fg = im.resize((new_w, new_h), Image.Resampling.LANCZOS)

            # 3. 悬浮主体阴影绘制
            paste_x = (target_size[0] - new_w) // 2
            paste_y = (target_size[1] - new_h) // 2

            # 阴影层
            shadow = Image.new("RGBA", target_size, (0, 0, 0, 0))
            shadow_draw = ImageDraw.Draw(shadow)
            shadow_draw.rectangle(
                [paste_x - 10, paste_y - 8, paste_x + new_w + 10, paste_y + new_h + 12],
                fill=(0, 0, 0, 160)
            )
            shadow = shadow.filter(ImageFilter.GaussianBlur(radius=15))
            bg = Image.alpha_composite(bg, shadow)

            # 贴上主体
            bg.paste(fg, (paste_x, paste_y), fg)

            # 4. 品牌胶囊水印 aronshare.com (右下角)
            draw = ImageDraw.Draw(bg)
            tag_text = "aronshare.com"
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
            except Exception:
                font = ImageFont.load_default()

            bbox = draw.textbbox((0, 0), tag_text, font=font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]

            px = target_size[0] - tw - 45
            py = target_size[1] - th - 35
            pad = 12

            # 绘制品牌半透明胶囊底
            draw.rounded_rectangle(
                [px - pad, py - pad, px + tw + pad, py + th + pad],
                radius=8,
                fill=(10, 15, 30, 200),
                outline=(56, 189, 248, 180),
                width=1
            )
            draw.text((px, py), tag_text, font=font, fill=(255, 255, 255, 240))

            # 转换为 RGB 并保存为高质量 WebP
            final = bg.convert("RGB")
            final.save(output_path, "WEBP", quality=92)
            return True
    except Exception as e:
        print(f"[!] Letterbox 处理失败: {e}")
        return False

def generate_cover_for_post(title: str, category: str, output_path: str, url: str = "", content: str = "", official_url: str = "", repo_url: str = "") -> bool:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    temp_raw = f"/tmp/raw_cover_{os.path.basename(output_path)}.png"

    try:
        # 1. 尝试从 content 中提取外链真实图片
        imgs = re.findall(r'https?://[^\s"\'<>]+\.(?:png|jpg|jpeg|webp)', content or "", re.I)
        clean_imgs = [i for i in imgs if not any(k in i.lower() for k in ["avatar", "icon", "badge", "shields.io"])]
        for img_url in clean_imgs:
            if download_image(img_url, temp_raw):
                if apply_letterbox(temp_raw, output_path):
                    print(f"[√] 从正文提取界面图成功: {output_path}")
                    return True

        # 2. 尝试从 GitHub 仓库提取
        target_repo = repo_url or (url if "github.com" in (url or "") else "") or (official_url if "github.com" in (official_url or "") else "")
        if target_repo and "github.com" in target_repo:
            if extract_github_preview(target_repo, temp_raw):
                if apply_letterbox(temp_raw, output_path):
                    print(f"[√] 提取 GitHub 仓库官方预览成功: {output_path}")
                    return True

        # 3. 尝试无头 Chrome 官网实拍截屏
        target_site = official_url or url
        if target_site and not is_blocked_or_forum(target_site):
            if capture_with_chrome(target_site, temp_raw):
                if apply_letterbox(temp_raw, output_path):
                    print(f"[√] 成功捕获官网真实界面: {output_path}")
                    return True

    finally:
        if os.path.exists(temp_raw):
            try:
                os.remove(temp_raw)
            except Exception:
                pass

    return False
