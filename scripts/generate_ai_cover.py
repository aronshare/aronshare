#!/usr/bin/env python3
"""
高清 16:9 视网膜科技卡片封面全自动生成引擎 (generate_ai_cover.py)
专为 AronShare 资源站打造：
- 严格 1200x675 (16:9 黄金分辨率)
- 渐变科技暗黑质感背景 / 高光微拟物网格
- 自动提取核心分类、超大主标题、痛点副标
- 右下角无损注入 aronshare.com 专属圆角胶囊水印
- 自动导出极致轻量高保真 WebP 格式
"""

import sys
import os
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FONTS_DIR = "/usr/share/fonts"
FONT_TITLE_PATHS = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
]

def get_font(size):
    for p in FONT_TITLE_PATHS:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def create_card_cover(title, category="开源神器", output_path="/tmp/cover.webp", watermark="aronshare.com"):
    w, h = 1200, 675
    img = Image.new("RGBA", (w, h), (15, 23, 42, 255)) # slate-900
    draw = ImageDraw.Draw(img)

    # 1. 绘制科技网格背景
    grid_color = (30, 41, 59, 120) # slate-800
    for x in range(0, w, 40):
        draw.line([(x, 0), (x, h)], fill=grid_color, width=1)
    for y in range(0, h, 40):
        draw.line([(0, y), (w, y)], fill=grid_color, width=1)

    # 2. 绘制顶部发光光晕 (Radial/Gradient 模拟)
    halo = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    halo_draw = ImageDraw.Draw(halo)
    # 顶部中央天蓝色高光
    for r in range(350, 0, -5):
        alpha = int(35 * (1 - r / 350))
        halo_draw.ellipse([600 - r * 1.5, -100 - r, 600 + r * 1.5, -100 + r], fill=(14, 165, 233, alpha))
    img = Image.alpha_composite(img, halo)
    draw = ImageDraw.Draw(img)

    # 3. 绘制分类胶囊徽标
    cat_font = get_font(22)
    cat_text = f"● {category}"
    bbox = draw.textbbox((0, 0), cat_text, font=cat_font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    badge_x = 100
    badge_y = 140
    pad_x, pad_y = 18, 10
    draw.rounded_rectangle(
        [badge_x, badge_y, badge_x + tw + pad_x * 2, badge_y + th + pad_y * 2],
        radius=8,
        fill=(14, 165, 233, 40),
        outline=(56, 189, 248, 180),
        width=1
    )
    draw.text((badge_x + pad_x, badge_y + pad_y - 2), cat_text, fill=(56, 189, 248, 255), font=cat_font)

    # 4. 绘制超大主标题 (智能换行与自适应字号)
    clean_title = title.split('：')[0].split(' - ')[0].strip()
    if len(clean_title) > 28:
        clean_title = clean_title[:28] + "..."

    title_size = 52 if len(clean_title) <= 16 else 44
    title_font = get_font(title_size)

    # 自动折行 (每行最多 14-16 个汉字)
    lines = []
    line_limit = 15 if title_size == 44 else 13
    for i in range(0, len(clean_title), line_limit):
        lines.append(clean_title[i:i+line_limit])

    start_y = badge_y + th + pad_y * 2 + 50
    for idx, l in enumerate(lines[:2]):
        draw.text((100, start_y + idx * (title_size + 18)), l, fill=(248, 250, 252, 255), font=title_font)

    # 5. 绘制副标与认证标识
    sub_font = get_font(20)
    sub_y = start_y + len(lines[:2]) * (title_size + 18) + 40
    sub_text = "官方源码已验证 · 纯净免安装 · 拒绝商业捆绑割韭菜"
    draw.text((100, sub_y), sub_text, fill=(148, 163, 184, 220), font=sub_font)

    # 6. 注入右下角专属水印
    wm_font = get_font(22)
    wm_bbox = draw.textbbox((0, 0), watermark, font=wm_font)
    wm_w, wm_h = wm_bbox[2] - wm_bbox[0], wm_bbox[3] - wm_bbox[1]
    
    rx2 = w - 40
    ry2 = h - 40
    rx1 = rx2 - wm_w - 32
    ry1 = ry2 - wm_h - 18
    draw.rounded_rectangle([rx1, ry1, rx2, ry2], radius=8, fill=(15, 23, 42, 210), outline=(51, 65, 85, 200), width=1)
    draw.text((rx1 + 16, ry1 + 7), watermark, fill=(255, 255, 255, 240), font=wm_font)

    # 7. 导出无损 WebP
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.convert("RGB").save(output_path, "WEBP", quality=92)
    print(f"[√] 成功生成高清 16:9 品牌封面: {output_path}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 generate_ai_cover.py <title> <category> <output_path>")
        sys.exit(1)
    create_card_cover(sys.argv[1], sys.argv[2], sys.argv[3])
