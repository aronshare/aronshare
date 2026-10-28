#!/usr/bin/env python3
"""
AronShare 资源库专版 Telegram 自动分发程序 (sync_aronshare_to_telegram.py)
自动将 aronshare.com 精选工具/资源推送到 @aronhouyu1024 频道
"""

import sys
import os
import re
import html
import json
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path

SECRETS_PATH = "/home/ubuntu/.secrets/telegram-aronhy-bot.json"

def send_aronshare_post(post_id, title, category, summary, cover_url=None):
    if not os.path.exists(SECRETS_PATH):
        print(f"[!] 未找到 Telegram 凭证文件: {SECRETS_PATH}")
        return False

    with open(SECRETS_PATH, "r", encoding="utf-8") as f:
        creds = json.load(f)

    bot_token = creds.get("bot_token")
    chat_id = creds.get("chat_id")  # @aronhouyu1024

    detail_url = f"https://aronshare.com/posts/{post_id}/"
    if not cover_url:
        cover_url = f"https://aronshare.com/covers/cover_{post_id}.webp"

    # 纯文本清理，剔除 HTML 标签，避免 Telegram HTML 解析器报错
    clean_summary = re.sub(r'<[^>]+>', '', summary or '').strip()
    clean_summary = re.sub(r'\s+', ' ', clean_summary)[:280]

    caption_lines = [
        f"🌟 <b>{html.escape(title)}</b>\n",
        f"🏷️ <b>资源分类</b>：#{html.escape(category.replace(' ', '_'))}",
        f"💡 <b>核心亮点与痛点拆解</b>：\n{html.escape(clean_summary)}\n",
        f"🔗 <b>查看完整深度评测与官方/网盘下载</b>：\n{detail_url}",
        f"\n⚡ <i>AronShare 自动化精选资源系统同步推送</i>"
    ]
    caption = "\n".join(caption_lines)

    # 尝试发送带图消息，若图片外链不可达则降级为文本发送
    url_photo = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    payload_photo = {
        "chat_id": chat_id,
        "photo": cover_url,
        "caption": caption,
        "parse_mode": "HTML"
    }

    req = urllib.request.Request(
        url_photo,
        data=json.dumps(payload_photo).encode("utf-8"),
        headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            if res.get("ok"):
                print(f"[√] 成功推送图文资源 [{post_id}] {title} 到 Telegram 频道 {chat_id}！")
                return True
    except Exception as e:
        # 平滑降级为 sendMessage
        try:
            url_msg = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload_msg = {
                "chat_id": chat_id,
                "text": caption,
                "parse_mode": "HTML"
            }
            req_msg = urllib.request.Request(
                url_msg,
                data=json.dumps(payload_msg).encode("utf-8"),
                headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
            )
            with urllib.request.urlopen(req_msg, timeout=15) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                if res.get("ok"):
                    print(f"[√] 成功推送文本资源 [{post_id}] {title} 到 Telegram 频道！")
                    return True
        except Exception as err:
            print(f"[x] 降级发送异常: {str(err)}")
            return False

if __name__ == '__main__':
    # 测试推送最新第 11652 篇资源
    test_id = "11652"
    test_title = "Pinkbin 开源 Windows 磁盘清理工具，让 AI 帮你看懂文件夹能不能删"
    test_cat = "开源自托管"
    test_summary = "C 盘经常爆红？传统磁盘工具只告诉你哪里占空间，很少告诉你能不能删。Pinkbin 借助本地 AI 智能分析陌生文件夹用途与删除风险，告别误删困扰！"
    
    print("[*] 正在向 @aronhouyu1024 发送实测卡片...")
    send_aronshare_post(test_id, test_title, test_cat, test_summary)
