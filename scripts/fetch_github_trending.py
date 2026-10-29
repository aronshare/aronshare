#!/usr/bin/env python3
"""
自动采集 GitHub Trending 与高质量开源神器到 content_hub.db
特点：
1. 专注 stars > 200 的近期高热度实用开源工具、自托管神器、跨平台客户端
2. 自动提取 README 中的原生 UI 真实截图
3. 严格清洗，杜绝任何论坛防爬盾/无图口水帖
"""

import sqlite3
import json
import urllib.request
import re
from datetime import datetime
from pathlib import Path

DB_PATH = Path("/home/ubuntu/.hermes/profiles/xwriter/data/content_hub.db")
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0"

def get_trending_repos():
    # 搜索近期高星实用项目
    queries = [
        "stars:>300+pushed:>2026-10-15+topic:tools",
        "stars:>500+pushed:>2026-10-15+topic:desktop",
        "stars:>400+pushed:>2026-10-15+topic:utility"
    ]
    repos = []
    seen = set()
    for q in queries:
        url = f"https://api.github.com/search/repositories?q={q}&sort=stars&order=desc&per_page=15"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode())
                for item in data.get("items", []):
                    full_name = item["full_name"]
                    if full_name not in seen:
                        seen.add(full_name)
                        repos.append(item)
        except Exception as e:
            print(f"[!] GitHub API 请求提示: {e}")
    return repos

def extract_readme_images(repo_name):
    url = f"https://api.github.com/repos/{repo_name}/readme"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/vnd.github.v3.raw"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            text = resp.read().decode("utf-8", errors="ignore")
            imgs = re.findall(r'https?://[^\s"\'<>]+\.(?:png|jpg|jpeg|webp)', text, re.I)
            clean = [i for i in imgs if not any(k in i.lower() for k in ["badge", "shields.io", "travis", "workflow", "avatar"])]
            return clean, text[:1500]
    except Exception:
        return [], ""

def sync_to_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 确保源存在
    cur.execute("SELECT id FROM monitor_sources WHERE name = 'GitHub Trending 实用神器';")
    row = cur.fetchone()
    if not row:
        cur.execute("""
            INSERT INTO monitor_sources (name, category, site_url, feed_url, fetch_type, enabled, created_at)
            VALUES ('GitHub Trending 实用神器', '开源神器与自托管工具', 'https://github.com/trending', 'https://github.com/trending', 'github', 1, datetime('now'));
        """)
        source_id = cur.lastrowid
    else:
        source_id = row[0]

    repos = get_trending_repos()
    print(f"[*] 发现 {len(repos)} 个 GitHub 热门开源项目...")

    added = 0
    for r in repos:
        repo_name = r["full_name"]
        html_url = r["html_url"]
        desc = r.get("description") or repo_name
        stars = r.get("stargazers_count", 0)

        # 检查是否已收录
        cur.execute("SELECT id FROM raw_articles WHERE url = ?", (html_url,))
        if cur.fetchone():
            continue

        imgs, readme_snippet = extract_readme_images(repo_name)
        cover_img = imgs[0] if imgs else f"https://opengraph.githubassets.com/aronshare/{repo_name}"

        cur.execute("""
            INSERT INTO raw_articles (
                source_id, source_name, category, title, url, author, 
                cover_image, summary, content_text, score, status, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending', datetime('now'))
        """, (
            source_id,
            "GitHub Trending 实用神器",
            "开源工具与软件应用",
            f"{r['name']} - {desc[:60]}",
            html_url,
            r["owner"]["login"],
            cover_img,
            f"{desc}\nStars: {stars}\n语言: {r.get('language') or '通用'}",
            readme_snippet or desc,
            90.0
        ))
        added += 1

    conn.commit()
    conn.close()
    print(f"[√] 成功收录 {added} 个高质量开源神器候选入库！")

if __name__ == "__main__":
    sync_to_db()
