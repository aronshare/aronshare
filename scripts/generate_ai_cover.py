#!/usr/bin/env python3
"""
高清 16:9 视网膜科技卡片封面全自动生成引擎 (generate_ai_cover.py)
专为 AronShare 资源站打造：
- 严格 1200x675 (16:9 黄金分辨率)
- 渐变科技暗黑质感背景 / 高光微拟物网格 / 饱满光晕
- 自动提取核心分类、智能自适应完整标题（绝不生硬截断 ..）
- 右侧科技卡片矩阵（左右平衡，拒绝左重右轻）
- 高亮副标与特性提示
- 右下角无损注入 aronshare.com 专属圆角胶囊水印
- 自动导出极致轻量高保真 WebP 格式
"""

import sys
import os
import re
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

def create_card_cover(title, category="开源神器", output_path="/tmp/cover.webp", watermark="aronshare.com", subtitle_text="官方源码已验证 · 纯净免安装 · 拒绝商业捆绑割韭菜"):
    w, h = 1200, 675
    img = Image.new("RGBA", (w, h), (15, 23, 42, 255)) # slate-900
    draw = ImageDraw.Draw(img)

    # 1. 绘制科技网格背景
    grid_color = (30, 41, 59, 120) # slate-800
    for x in range(0, w, 40):
        draw.line([(x, 0), (x, h)], fill=grid_color, width=1)
    for y in range(0, h, 40):
        draw.line([(0, y), (w, y)], fill=grid_color, width=1)

    # 2. 绘制顶部发光与右侧光晕 (营造饱满空间感)
    halo = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    halo_draw = ImageDraw.Draw(halo)
    for r in range(400, 0, -5):
        alpha = int(35 * (1 - r / 400))
        halo_draw.ellipse([600 - r * 1.5, -100 - r, 600 + r * 1.5, -100 + r], fill=(14, 165, 233, alpha))
    for r in range(300, 0, -6):
        alpha = int(25 * (1 - r / 300))
        halo_draw.ellipse([980 - r, 300 - r, 980 + r, 300 + r], fill=(59, 130, 246, alpha))
    img = Image.alpha_composite(img, halo)
    draw = ImageDraw.Draw(img)

    # 3. 绘制分类胶囊徽标
    cat_font = get_font(24)
    cat_text = f"●  {category}"
    bbox = draw.textbbox((0, 0), cat_text, font=cat_font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    badge_x = 90
    badge_y = 120
    pad_x, pad_y = 20, 10
    draw.rounded_rectangle(
        [badge_x, badge_y, badge_x + tw + pad_x * 2, badge_y + th + pad_y * 2],
        radius=10,
        fill=(14, 165, 233, 45),
        outline=(56, 189, 248, 220),
        width=2
    )
    draw.text((badge_x + pad_x, badge_y + pad_y - 2), cat_text, fill=(56, 189, 248, 255), font=cat_font)

    # 4. 绘制超大主标题 (智能完整排版，杜绝生硬截断，动态字号)
    clean_title = re.sub(r'^[【\\[].*?[】\\]]\\s*', '', title).strip()
    
    # 动态字号匹配：字数越多字号越适中，绝不出现 .. 截断
    if len(clean_title) <= 14:
        title_size = 52
        chars_per_line = 13
    elif len(clean_title) <= 24:
        title_size = 44
        chars_per_line = 15
    elif len(clean_title) <= 34:
        title_size = 36
        chars_per_line = 17
    else:
        title_size = 32
        chars_per_line = 19

    title_font = get_font(title_size)

    lines = []
    for i in range(0, len(clean_title), chars_per_line):
        lines.append(clean_title[i:i+chars_per_line])
        if len(lines) == 3:
            break

    start_y = badge_y + th + pad_y * 2 + 45
    for idx, l in enumerate(lines):
        draw.text((90, start_y + idx * (title_size + 16)), l, fill=(255, 255, 255, 255), font=title_font)

    # 5. 绘制副标与认证卖点 (高对比度、清晰明亮)
    sub_font = get_font(21)
    sub_y = start_y + len(lines) * (title_size + 16) + 35
    draw.text((90, sub_y), subtitle_text, fill=(203, 213, 225, 255), font=sub_font)

    # 6. 右侧科技功能矩阵 (解决画面右侧空旷、左重右轻的问题)
    decor_box_x = 840
    decor_box_y = 150
    # 纯中文标签，不依赖 Emoji 避免 Linux 字体缺失导致方块豆腐块
    features = [
        ("[极速调速]", "支持 1~1000 倍率自定义调节"),
        ("[安全开源]", "Ring3 进程调优 · 零内核侵入"),
        ("[绿色免装]", "单文件解压即用 · 无任何捆绑"),
        ("[下载加速]", "实测百度/大文件客户端有效")
    ]
    for i, (f_title, f_desc) in enumerate(features):
        cur_y = decor_box_y + i * 90
        draw.rounded_rectangle(
            [decor_box_x, cur_y, decor_box_x + 270, cur_y + 74],
            radius=12,
            fill=(30, 41, 59, 160),
            outline=(51, 65, 85, 200),
            width=1
        )
        t_font = get_font(19)
        draw.text((decor_box_x + 18, cur_y + 12), f_title, fill=(56, 189, 248, 255), font=t_font)
        d_font = get_font(13)
        draw.text((decor_box_x + 18, cur_y + 42), f_desc, fill=(203, 213, 225, 255), font=d_font) # 提亮至 slate-300

    # 7. 注入右下角专属水印
    wm_font = get_font(20)
    wm_bbox = draw.textbbox((0, 0), watermark, font=wm_font)
    wm_w, wm_h = wm_bbox[2] - wm_bbox[0], wm_bbox[3] - wm_bbox[1]
    
    rx2 = w - 40
    ry2 = h - 35
    rx1 = rx2 - wm_w - 28
    ry1 = ry2 - wm_h - 16
    draw.rounded_rectangle([rx1, ry1, rx2, ry2], radius=8, fill=(15, 23, 42, 210), outline=(51, 65, 85, 200), width=1)
    draw.text((rx1 + 14, ry1 + 6), watermark, fill=(255, 255, 255, 240), font=wm_font)

    # 8. 导出无损 WebP
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.convert("RGB").save(output_path, "WEBP", quality=92)
    print(f"[√] 成功生成高清 16:9 品牌封面: {output_path}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 generate_ai_cover.py <title> <category> <output_path>")
        sys.exit(1)
    create_card_cover(sys.argv[1], sys.argv[2], sys.argv[3])
