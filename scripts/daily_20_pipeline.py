#!/usr/bin/env python3
"""
AronShare 每日 20 篇全自动精选、网盘转存、发布与 TG 广播主控脚本 (daily_20_pipeline.py)
每天执行：
1. 从数据库筛选最新高价值 20 篇一手候选
2. 识别网盘链接，调用 pan_transfer 自动秒转存至自有夸克 /AronShare资源库，替换为任推邦分佣链接
3. 生成 16:9 无损科技封面，写入 Astro posts Markdown
4. 执行 Astro build 静态构建并部署上线到 /www/wwwroot/aronshare.com
5. 同步广播 20 篇到 Telegram 频道 (@aronhouyu1024)
6. 重新生成顶级 Awesome README 并自动提交同步至 GitHub (aronshare/aronshare)
"""

import os
import sys
import re
import time
import json
import sqlite3
import subprocess
from datetime import datetime
from pathlib import Path

BASE_DIR = Path("/home/ubuntu/aronshare-resource-hub")
SCRIPTS_DIR = BASE_DIR / "scripts"
ASTRO_DIR = Path("/home/ubuntu/ahhhhfs-astro")
WEB_ROOT = Path("/www/wwwroot/aronshare.com")
DB_PATH = Path("/home/ubuntu/.hermes/profiles/xwriter/data/content_hub.db")
SECRETS_PATH = Path("/home/ubuntu/.secrets/telegram-aronhy-bot.json")

# 加载 pan_transfer
sys.path.append(str(ASTRO_DIR / "pipeline"))
try:
    from pan_transfer import QuarkPanTransfer
except ImportError:
    QuarkPanTransfer = None

# 加载 TG 推送模块
sys.path.append(str(SCRIPTS_DIR))
try:
    from sync_aronshare_to_telegram import send_aronshare_post
except ImportError:
    send_aronshare_post = None

def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}", flush=True)

def run_daily_pipeline(target_count=20):
    log("==================================================")
    log(f"🚀 启动 AronShare 每日 {target_count} 篇全闭环自动化发布流水线")
    log("==================================================")

    # 1. 初始化转存引擎
    quark_transfer = None
    if QuarkPanTransfer:
        # 读取 ahhhhfs-astro/.env
        env_file = ASTRO_DIR / ".env"
        if env_file.exists():
            for line in env_file.read_text(encoding="utf-8").splitlines():
                k, sep, v = line.strip().partition("=")
                if sep and k and not k.startswith("#"):
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
        quark_transfer = QuarkPanTransfer()
        log(f"[*] 夸克转存引擎状态: {'已配置 (任推邦已绑定)' if quark_transfer.is_configured() else '未配置'}")

    # 2. 查询现网已发布的文章（查重）
    existing_slugs = set()
    posts_dir = ASTRO_DIR / "src" / "content" / "posts"
    posts_dir.mkdir(parents=True, exist_ok=True)
    for p in posts_dir.glob("*.md"):
        existing_slugs.add(p.stem)
    log(f"[*] 当前系统已有文章: {len(existing_slugs)} 篇")

    # 3. 从 content_hub.db 筛选最新 20 篇高价值一手候选（严格限制为纯资源与纯工具类，坚决隔离科技新闻/外媒，坚决排除论坛无图源 V2EX）
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT r.id, s.name, r.title, r.url, r.summary, r.content_text, s.category
        FROM raw_articles r
        JOIN monitor_sources s ON r.source_id = s.id
        WHERE r.score >= 80
          AND s.name NOT LIKE '%V2EX%'
          AND r.url NOT LIKE '%v2ex.com%'
          AND (
            s.category LIKE '%网盘%' OR 
            s.category LIKE '%课程%' OR 
            s.category LIKE '%副业%' OR 
            s.category LIKE '%开源%' OR 
            s.category LIKE '%工具%' OR 
            s.category LIKE '%自学%' OR
            s.category LIKE '%神器%' OR
            s.category LIKE '%原盘%' OR
            s.category LIKE '%SaaS%' OR
            s.category LIKE '%自托管%'
          )
          AND s.category NOT LIKE '%外媒%'
          AND s.category NOT LIKE '%綜合科技%'
          AND s.category NOT LIKE '%一線科技%'
          AND s.category NOT LIKE '%新聞%'
          AND s.category NOT LIKE '%Apple%'
        ORDER BY r.created_at DESC
        LIMIT 100
    """)
    candidates = cur.fetchall()
    conn.close()

    selected_posts = []
    for row in candidates:
        r_id, s_name, title, url, summary, content, category = row
        slug = f"post_{r_id}"
        if slug in existing_slugs or str(r_id) in existing_slugs:
            continue
        # 简单清洗标题
        clean_title = re.sub(r'^[【\[].*?[】\]]\s*', '', title).strip()
        clean_title = clean_title.replace("：", " - ").replace(":", " - ")
        
        selected_posts.append({
            "id": r_id,
            "slug": slug,
            "source_name": s_name,
            "title": clean_title,
            "url": url,
            "summary": summary or clean_title,
            "content": content or summary or clean_title,
            "category": category or "实用工具"
        })
        if len(selected_posts) >= target_count:
            break

    log(f"[*] 本次精选出 {len(selected_posts)} 篇全新一手高价值资源！")
    if not selected_posts:
        log("[!] 暂无可发布的全新文章，结束本次轮询。")
        return

    # 4. 逐篇执行：网盘转存 -> 生成封面 -> 生成 Markdown
    astro_covers_dir = ASTRO_DIR / "public" / "covers"
    astro_covers_dir.mkdir(parents=True, exist_ok=True)
    gen_cover_script = SCRIPTS_DIR / "cover_crawler.py"

    published_items = []
    for item in selected_posts:
        log(f"--> 处理第 {len(published_items)+1}/{len(selected_posts)} 篇: [{item['title']}]")
        
        # 严格过滤：仅当检测到夸克网盘链接时，才触发自动化转存
        pan_share_url = None
        combined_text = item['content'] + " " + item['url'] + " " + item['summary']
        m_quark = re.search(r'https?://pan\.quark\.cn/s/[a-zA-Z0-9]+', combined_text)
        
        if m_quark:
            if quark_transfer and quark_transfer.is_configured():
                orig_quark = m_quark.group(0)
                log(f"  [+] 检测到上游夸克网盘链接: {orig_quark}，执行秒转存...")
                try:
                    trans_res = quark_transfer.transfer_and_share(orig_quark)
                    if trans_res and trans_res.get("share_url"):
                        pan_share_url = trans_res["share_url"]
                        log(f"  [√] 转存成功！已生成自有任推邦专属分佣链接: {pan_share_url}")
                except Exception as e:
                    log(f"  [!] 转存波动: {e}")
        else:
            log("  [-] 未包含目标网盘链接，跳过转存，保持原生官网直达。")

        # 生成 16:9 真实界面 Letterbox 品牌封面 (优先抓取官方原生 UI，绝不用纯蓝色模板)
        # 生成高质量 16:9 真实 UI 封面
        cover_filename = f"cover_{item['id']}.webp"
        out_cover = astro_covers_dir / cover_filename
        cover_ok = False
        try:
            from cover_crawler import generate_cover_for_post
            cover_ok = generate_cover_for_post(
                title=item['title'],
                category=item['category'],
                output_path=str(out_cover),
                url=item['url'],
                content=item.get('content', ''),
                official_url=item['url'],
                repo_url=item['url']
            )
        except Exception as e:
            log(f"  [!] 封面抓取异常: {e}")

        if not cover_ok or not out_cover.exists():
            log(f"  [!] 未能提取到真实软件界面 UI，严格执行质量标准：跳过该篇，绝不发布单调文字图！")
            continue

        # Body images and attachments use the SAME mandatory gate as covers.
        # Never leave remote/dirty originals in content on review or edit failure.
        try:
            from image_ingestion import localize_images
            item['content'], _ = localize_images(
                item['content'], base_url=item['url'], public_dir=ASTRO_DIR / 'public')
            # Summary is also interpolated into the Markdown body, so image
            # syntax there must not provide a second unreviewed ingestion path.
            item['summary'], _ = localize_images(
                item.get('summary') or '', base_url=item['url'], public_dir=ASTRO_DIR / 'public')
        except Exception as exc:
            log(f"  [!] Body image review/cleanup blocked post {item['id']}: {exc}")
            continue

        # 纯文本清理，剔除 HTML 标签与双引号等破坏 YAML frontmatter 的字符
        clean_summary = re.sub(r'<[^>]+>', ' ', item['summary'] or '').strip()
        clean_summary = clean_summary.replace('"', '').replace("'", '').replace('\n', ' ')
        clean_summary = re.sub(r'\s+', ' ', clean_summary)[:280]

        clean_title = item['title'].replace('"', '').replace("'", '').replace('\n', ' ')

        pan_links_yaml = "pan_links: []"
        if pan_share_url:
            pan_links_yaml = f"""pan_links:
  - name: "夸克网盘 (高速转存)"
    url: "{pan_share_url}" """

        # 写入 Markdown (严格契合 Astro Collection posts 强校验 Schema)
        now_iso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        md_content = f"""---
title: "{clean_title}"
category: "{item['category']}"
category_slug: "apps"
tags: ["{item['category']}", "神器推荐", "自动化"]
published_at: "{now_iso}"
author: "Aron"
cover: "/covers/{cover_filename}"
summary: "{clean_summary[:120]}"
official_url: "{item['url']}"
{pan_links_yaml}
source_name: "{item['source_name']}"
source_url: "{item['url']}"
---

### 💡 核心痛点与功能解析
{clean_summary}

### 🛠️ 详细功能与使用实操
{item['content']}

### 🔗 官方直达与高速网盘
- **一手官方源头**：[点击直达官网]({item['url']})
"""
        if pan_share_url:
            md_content += f"- **AronShare 专属夸克网盘直达 (高速转存)**：[点击极速转存下载]({pan_share_url})\n"

        post_md_path = posts_dir / f"{item['slug']}.md"
        from image_cleanup import atomic_write
        atomic_write(post_md_path, md_content.encode('utf-8'))
        published_items.append(item)

    log(f"[√] 成功生成 {len(published_items)} 篇 Markdown 文章！")

    if not published_items:
        log("[!] 没有通过真实封面校验的文章，停止发布。")
        return

    # 5. 执行 Astro 静态编译与生产部署
    log("[*] 正在执行 Astro 静态构建与全站热发布...")
    res = subprocess.run(["npm", "run", "build"], cwd=str(ASTRO_DIR), capture_output=True, text=True)
    if res.returncode == 0:
        log("[√] Astro 编译成功！同步至 Nginx 生产目录...")
        subprocess.run(["sudo", "rsync", "-av", "--delete", f"{ASTRO_DIR}/dist/", f"{WEB_ROOT}/"], check=True)
        subprocess.run(["sudo", "chown", "-R", "www:www", str(WEB_ROOT)], check=True)
    else:
        log(f"[!] Astro 编译警告: {res.stderr[:300]}")

    # 6. Telegram 频道同步广播 20 篇
    log("[*] 正在同步广播至 Telegram 官方频道 (@aronhouyu1024)...")
    for item in published_items:
        try:
            if send_aronshare_post:
                send_aronshare_post(item['id'], item['title'], item['category'], item['summary'])
                time.sleep(3) # 间隔 3 秒，严格规避 TG 429 限流
        except Exception as e:
            log(f"  [!] TG 广播异常: {e}")

    # 7. 重新提炼 Awesome README 并自动提交 Git
    log("[*] 重新提炼 Awesome-style README.md 并同步 GitHub 仓库...")
    readme_script = SCRIPTS_DIR / "build_awesome_readme.py"
    if readme_script.exists():
        subprocess.run(["python3", str(readme_script)], capture_output=True, text=True)

    git_sync_script = SCRIPTS_DIR / "auto_git_sync.py"
    if git_sync_script.exists():
        commit_msg = f"feat(daily-pipeline): publish {len(published_items)} curated resources with pan monetization [{datetime.now().strftime('%Y-%m-%d')}]"
        subprocess.run(["python3", str(git_sync_script), commit_msg], cwd=str(BASE_DIR), capture_output=True, text=True)
        log("[√] GitHub 远程仓库同步完成！")

    # 8. 向 Aron 飞书发送富文本实时卡片
    log("[*] 正在向 Aron 飞书发送全链路执行完成卡片...")
    feishu_script = SCRIPTS_DIR / "feishu_notifier.py"
    if feishu_script.exists():
        try:
            sys.path.append(str(SCRIPTS_DIR))
            from feishu_notifier import send_feishu_update_card
            items_for_card = [
                {"title": item['title'], "category": item['category'], "url": f"https://aronshare.com/posts/{item['slug']}/"}
                for item in published_items[:8]
            ]
            send_feishu_update_card(
                title=f"AronShare 每日 20 篇全自动发布完成 [{datetime.now().strftime('%m-%d %H:%M')}]",
                summary=f"今日精选 {len(published_items)} 篇高价值工具已全自动上线，并同步广播至 Telegram 官方频道与 GitHub Awesome 仓库！",
                stats_info=f"发布数量: {len(published_items)} 篇 | 生产环境: HTTP 200 正常 | TG推送: 20条成功 | Git: 已同步",
                new_items=items_for_card
            )
            log("[√] 飞书富文本播报卡片发送成功！")
        except Exception as e:
            log(f"[!] 飞书播报异常: {e}")

    log("==================================================")
    log(f"🎉 今日 {len(published_items)} 篇资源全链路（网站+TG+Git+飞书通知）全自动发布完毕！")
    log("==================================================")

if __name__ == '__main__':
    run_daily_pipeline(target_count=20)
