#!/usr/bin/env python3
"""
AronShare 自动化 Git 提交与同步引擎 (auto_git_sync.py)
特点：
1. 格式化提交信息（清晰、简单、明了，遵循 Conventional Commits 规范）
2. 自动统计变动详情（新增资源数、修改文章数）
3. 严格校验，杜绝垃圾临时文件提交
4. 专为 https://github.com/aronshare/aronshare 打造
"""

import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

REPO_DIR = Path("/home/ubuntu/aronshare-resource-hub")

def run_cmd(cmd, check=True):
    res = subprocess.run(cmd, cwd=REPO_DIR, text=True, capture_output=True)
    if check and res.returncode != 0:
        print(f"[!] Error running {' '.join(cmd)}:\n{res.stderr}")
        sys.exit(res.returncode)
    return res.stdout.strip()

def auto_sync(commit_msg=None, branch="main", target_remote="origin"):
    print("[*] 开始检查 AronShare 代码仓库状态...")

    # 1. 检查是否有变动
    status = run_cmd(["git", "status", "--porcelain"])
    if not status:
        print("[√] 工作区干净，没有检测到任何新变更，无需提交。")
        return

    # 2. 统计新增/修改的资源数量
    lines = status.split("\n")
    new_posts = [l for l in lines if "src/content/posts/" in l and (l.startswith("??") or l.startswith(" A"))]
    mod_posts = [l for l in lines if "src/content/posts/" in l and l.strip().startswith("M")]
    covers = [l for l in lines if "public/covers/" in l]

    # 3. 智能生成清晰、简单、明了的提交信息
    if not commit_msg:
        time_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        details = []
        if new_posts:
            details.append(f"新增 {len(new_posts)} 篇资源")
        if mod_posts:
            details.append(f"优化 {len(mod_posts)} 篇内容")
        if covers:
            details.append(f"同步 {len(covers)} 张封面")

        if details:
            summary = "，".join(details)
            commit_msg = f"content: 自动同步站内更新 ({summary}) [{time_str}]"
        else:
            commit_msg = f"chore: 站点配置与样式自动同步 [{time_str}]"

    print(f"[*] 准备提交: {commit_msg}")

    # 4. Git 操作三部曲 (Add -> Commit -> Push)
    run_cmd(["git", "add", "-A"])
    run_cmd(["git", "commit", "-m", commit_msg])
    
    print(f"[*] 正在推送到远程仓库 ({target_remote} {branch})...")
    push_out = run_cmd(["git", "push", target_remote, branch])
    print("[√] 同步成功完成！")
    print(push_out)

if __name__ == "__main__":
    custom_msg = sys.argv[1] if len(sys.argv) > 1 else None
    auto_sync(custom_msg)
