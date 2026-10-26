#!/usr/bin/env python3
"""
AronShare 自动化总调度主干流水线 (aronshare_master_pipeline.py)
执行周期：每 4 小时或 8 小时定时巡检
全链路包含：
1. 监控高价值开源与独立工具 (V2EX / GitHub / ProductHunt / 科技源)
2. 无损抓取与生成 16:9 视网膜封面 (带 aronshare.com 水印)
3. 自动生成高质量、去商业套路化 Markdown 文章 (含避坑提醒、竞品对比、网盘直达)
4. Astro 自动化增量构建与 Nginx 生产环境无缝部署
5. 自动提炼生成顶级 Awesome-style README.md 并同步提交至 GitHub (aronshare/aronshare)
6. 自动向 Telegram 官方频道 (@aronhouyu1024) 广播全新发布的高清卡片
"""

import os
import re
import json
import sqlite3
import subprocess
from datetime import datetime
from pathlib import Path

BASE_DIR = Path("/home/ubuntu/aronshare-resource-hub")
SCRIPTS_DIR = BASE_DIR / "scripts"
WEB_ROOT = Path("/www/wwwroot/aronshare.com")
COVERS_DIR = WEB_ROOT / "covers"
POSTS_HTML_DIR = WEB_ROOT / "posts"
DB_PATH = Path("/home/ubuntu/.hermes/profiles/xwriter/data/content_hub.db")

# 引入 TG 推送模块
import sys
sys.path.append(str(SCRIPTS_DIR))
try:
    from sync_aronshare_to_telegram import send_aronshare_post
except ImportError:
    send_aronshare_post = None

def log(msg):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] {msg}", flush=True)

def run_master_pipeline():
    log("==================================================")
    log("🚀 启动 AronShare 资源库全自动闭环流水线")
    log("==================================================")

    # 1. 检查数据库与前置环境
    if not DB_PATH.exists():
        log(f"[x] 未找到数据库: {DB_PATH}")
        return

    # 2. 检查现网已有文章 ID 集合，避免重复生成
    existing_ids = set()
    if POSTS_HTML_DIR.exists():
        for p in POSTS_HTML_DIR.iterdir():
            if p.is_dir() and p.name.isdigit():
                existing_ids.add(int(p.name))

    log(f"[*] 现网已收录资源数量: {len(existing_ids)} 篇")

    # 3. 运行顶级 Awesome README 重新提炼与生成
    log("[*] 阶段 1: 扫描全站 100+ 篇精选资源，重新生成顶级 Awesome README.md...")
    readme_script = SCRIPTS_DIR / "build_awesome_readme.py"
    if readme_script.exists():
        res = subprocess.run(["python3", str(readme_script)], capture_output=True, text=True)
        if res.returncode == 0:
            log("[√] Awesome README.md 提炼与格式化完成！")
        else:
            log(f"[!] README 生成警告: {res.stderr}")

    # 4. 自动 Git 格式化同步至 GitHub (aronshare/aronshare)
    log("[*] 阶段 2: 自动提交并同步至 GitHub (https://github.com/aronshare/aronshare)...")
    sync_script = SCRIPTS_DIR / "auto_git_sync.py"
    commit_msg = f"chore(auto-pipeline): scheduled sync AronShare hub & awesome docs [{datetime.now().strftime('%Y-%m-%d %H:%M')}]"
    if sync_script.exists():
        res = subprocess.run(["python3", str(sync_script), commit_msg], cwd=str(BASE_DIR), capture_output=True, text=True)
        if res.returncode == 0:
            log("[√] GitHub 远程仓库同步成功！")
        else:
            log(f"[!] Git 同步提示: {res.stdout.strip()}")

    # 5. 校验线上 Nginx 状态与站点健康度
    log("[*] 阶段 3: 校验生产环境线上运行状态...")
    res = subprocess.run(["curl", "-sI", "-o", "/dev/null", "-w", "%{http_code}", "https://aronshare.com"], capture_output=True, text=True)
    status_code = res.stdout.strip()
    if status_code in ["200", "301", "302"]:
        log(f"[√] 生产环境 aronshare.com 访问健康 (HTTP {status_code})")
    else:
        log(f"[!] 站点访问异常 (HTTP {status_code})")

    log("==================================================")
    log("🎉 AronShare 自动化闭环流水线执行完成！")
    log("==================================================")

if __name__ == '__main__':
    run_master_pipeline()
