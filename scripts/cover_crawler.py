#!/usr/bin/env python3
"""
AronShare 真实软件界面截图与智能 Letterbox 封面生成模块 (cover_crawler.py)
标准：
1. 严禁抓取论坛自身页面 (V2EX / Discourse / 社区)，检测到防爬盾 (Cloudflare 等) 绝不使用
2. 优先提取真实软件界面截屏、官方 UI 或 GitHub 真实截图
3. GitHub 仅取 README 产品图片；官网提取实际图片，不回退社交卡片或浏览器截图
4. 使用 Pillow 智能 Letterbox：原图完整置中 + 背景高斯模糊弥散光晕 + 安全边距 + aronshare.com 胶囊水印
"""

import os
import tempfile
from pathlib import Path
from PIL import Image, ImageFilter, ImageDraw, ImageFont
from cover_sources import (download_image, extract_github_preview, extract_page_preview,
                           image_candidates, capture_with_chrome, is_blocked_or_forum)

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

def generate_cover_for_post(title: str, category: str, output_path: str, url: str = "", content: str = "", official_url: str = "", repo_url: str = "", provenance=None) -> bool:
    """Only source-derived images; failure never changes the existing destination.

    Optional provenance dict receives the exact selected image and referring page.
    All scratch files are unique and follow TMPDIR. Installation is atomic.
    """
    details = {}
    try:
        scratch = Path(os.environ.get('TMPDIR') or Path.home() / '.hermes/cache/scratch')
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="aronshare-cover-", dir=scratch) as work:
            raw = str(Path(work) / "source.img")
            rendered = str(Path(work) / "cover.webp")
            found = False
            for candidate in image_candidates(content or "", url or official_url):
                if download_image(candidate, raw, details):
                    details.update(kind="article-image", page_url=url)
                    found = True
                    break
            if not found:
                for target in dict.fromkeys(filter(None, (repo_url, url, official_url))):
                    if extract_github_preview(target, raw, details):
                        found = True
                        break
            if not found:
                for target in dict.fromkeys(filter(None, (official_url, url))):
                    if extract_page_preview(target, raw, details):
                        found = True
                        break
            if not found:
                print(f"[!] No usable real source image; skipped: {title}")
                return False
            # Mandatory review/edit gate BEFORE branding/formatting; no dirty fallback.
            from image_cleanup import prepare_image
            reviewed = prepare_image(raw)
            details['cleanup_reviewed_image'] = str(reviewed)
            if not apply_letterbox(str(reviewed), rendered):
                return False
            destination = Path(output_path)
            destination.parent.mkdir(parents=True, exist_ok=True)
            # Stage beside destination for atomic replace, including cross-device TMPDIR.
            fd, staged = tempfile.mkstemp(prefix=".cover-", suffix=".webp", dir=destination.parent)
            try:
                with os.fdopen(fd, 'wb') as stream:
                    stream.write(Path(rendered).read_bytes())
                os.replace(staged, destination)
            finally:
                Path(staged).unlink(missing_ok=True)
            if provenance is not None:
                provenance.update(details)
            print(f"[√] Real cover: {output_path}; source={details.get('resolved_image_url')}")
            return True
    except Exception as exc:
        print(f"[!] Cover failed: {exc}")
        return False
