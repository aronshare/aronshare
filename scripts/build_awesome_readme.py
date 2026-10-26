#!/usr/bin/env python3
"""
生成面向 GitHub 社区的顶级引流 Awesome 风格 README.md
为 https://github.com/aronshare/aronshare 量身打造
直接提炼全站 100 篇高价值已发布的开源工具与实战应用
"""

import re
from pathlib import Path
from collections import defaultdict

POSTS_DIR = Path("/www/wwwroot/aronshare.com/posts")
OUTPUT_README = Path("/home/ubuntu/aronshare-resource-hub/README.md")

def clean_text(t):
    if not t:
        return ""
    t = re.sub(r'[\r\n\t]+', ' ', t)
    t = re.sub(r'\s+', ' ', t)
    return t.strip()

def build_awesome_readme():
    print("[*] 正在扫描 /www/wwwroot/aronshare.com/posts/ 中的 100 篇高质量资源...")
    
    posts = []
    for p in sorted(POSTS_DIR.iterdir(), key=lambda x: int(x.name) if x.name.isdigit() else 0, reverse=True):
        idx_file = p / 'index.html'
        if not idx_file.exists():
            continue
            
        content = idx_file.read_text(encoding='utf-8')
        
        # 提取标题
        title_m = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
        raw_title = re.sub(r'<[^>]+>', '', title_m.group(1)).strip() if title_m else p.name
        # 清理冒号
        clean_title = re.sub(r'[:：]\s*', ' ', raw_title)
        
        # 提取描述/摘要
        desc_m = re.search(r'<meta[^>]+name=\"description\"[^>]+content=\"([^\"]+)\"', content)
        desc = clean_text(desc_m.group(1)) if desc_m else ''
        # 去掉前端可能多余的前缀
        desc = re.sub(r'^(编辑说明|内容说明)[：:]\s*', '', desc)
        if len(desc) > 95:
            desc = desc[:92] + "..."
            
        posts.append({
            "id": p.name,
            "title": clean_title,
            "desc": desc
        })

    print(f"[*] 成功提取 {len(posts)} 篇已发布资源，开始多维分组...")

    # 分组映射
    categorized = defaultdict(list)
    for item in posts:
        t_lower = item['title'].lower()
        d_lower = item['desc'].lower()
        combined = t_lower + " " + d_lower

        if any(k in combined for k in ['ai', 'agent', 'llm', 'rag', 'gpt', '模型', '写作', '标书', '提示词', '投研']):
            cat_key = "🤖 AI 智能体与提效工具 (AI Agents & LLM Tools)"
        elif any(k in combined for k in ['开源', 'github', '自托管', 'docker', '清理', '运维', '磁盘', 'linux', '存储']):
            cat_key = "🚀 精选开源自托管神器 (Self-Hosted & Open Source)"
        elif any(k in combined for k in ['在线', 'web', '压缩', '网页', '免安装', '转换', '查询', '海关', '数据']):
            cat_key = "⚡ 免安装 Web 在线利器 (Web & Cloud Utilities)"
        elif any(k in combined for k in ['出海', '搞钱', '副业', '增长', '社群', '漫剧', '短视频', '教程', '课程']):
            cat_key = "💰 出海增长与实战副业课 (Growth & Money Making)"
        else:
            cat_key = "💻 macOS / Windows 生产力应用 (Desktop Apps)"

        categorized[cat_key].append(item)

    # 构造 Markdown
    lines = [
        "<div align=\"center\">",
        "",
        "# 🌟 AronShare - 精选开源自托管神器与独立开发者实用资源导航",
        "",
        "[![Website](https://img.shields.io/badge/Official%20Site-aronshare.com-0284c7?style=for-the-badge&logo=googlechrome&logoColor=white)](https://aronshare.com)",
        "[![GitHub Stars](https://img.shields.io/github/stars/aronshare/aronshare?style=for-the-badge&logo=github&color=blue)](https://github.com/aronshare/aronshare)",
        "[![License](https://img.shields.io/badge/License-MIT-emerald?style=for-the-badge)](https://github.com/aronshare/aronshare)",
        "[![Awesome](https://awesome.re/badge.svg)](https://github.com/aronshare/aronshare)",
        "",
        "**拒绝商业割韭菜与流氓软件捆绑 · 专注好看、好用、可落地的独立开源神器与技术增长资产**",
        "",
        "🔗 **官网在线即刻浏览**：[https://aronshare.com](https://aronshare.com) （支持全局实时搜索、全端响应式、高清大图与网盘直达通道）",
        "",
        "---",
        "</div>",
        "",
        "## 📑 目录导航 (Table of Contents)",
        ""
    ]

    for cat_name, items in categorized.items():
        anchor = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fa5]+', '-', cat_name).strip('-').lower()
        lines.append(f"- [{cat_name}](#{anchor}) (`{len(items)}` 款工具)")

    lines.extend([
        "- [⚡ 自动化监控与流水线声明](#-自动化监控与流水线声明)",
        "- [🤝 贡献与推荐收录](#-贡献与推荐收录)",
        "- [⚖️ 免责声明与开源协议](#️-免责声明与开源协议)",
        "",
        "---",
        ""
    ])

    for cat_name, items in categorized.items():
        anchor = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fa5]+', '-', cat_name).strip('-').lower()
        lines.append(f"## <a id=\"{anchor}\"></a>{cat_name}")
        lines.append("")
        lines.append("| 编号 | 实用神器名称与核心痛点拆解 | 深度评测与完整包直达 | 状态 |")
        lines.append("| :--- | :--- | :---: | :---: |")

        for idx, item in enumerate(items, 1):
            detail_url = f"https://aronshare.com/posts/{item['id']}/"
            title_part = f"**{item['title']}**"
            desc_part = f"<br><sub>💡 {item['desc']}</sub>" if item['desc'] else ""
            badge = f"[![查看评测](https://img.shields.io/badge/查看拆解与下载-aronshare.com-0284c7?style=flat-square)]({detail_url})"
            lines.append(f"| `{idx:02d}` | {title_part}{desc_part} | {badge} | `已收录` |")

        lines.append("")

    # 尾部声明与社区共建
    lines.extend([
        "---",
        "",
        "## ⚡ 自动化监控与流水线声明",
        "",
        "本项目收录的所有工具与开源项目均由 **AronShare 自动化监控流水线** 持续巡检：",
        "- **拒绝流氓二改**：100% 溯源至开发者官方代码仓库或官方纯净发布页；",
        "- **极清视网膜大图**：所有封面图均由自动化流水线真机沙箱运行无损捕获；",
        "- **商业价值与技术落地**：正文坚决剔除废话套话，聚焦技术规格、横向对比、避坑提醒与官方 FAQ。",
        "",
        "## 🤝 贡献与推荐收录",
        "",
        "如果你是独立开发者，或者发现了令人惊艳的开源工具与副业实战模型：",
        "1. 欢迎直接提交 [Issue](https://github.com/aronshare/aronshare/issues) 或发起 Pull Request；",
        "2. 也可在官网留言交流：[https://aronshare.com](https://aronshare.com) ；",
        "3. 一旦入选，将自动被官网索引并在 GitHub 全球同步展示，获得长期的开发者流量曝光。",
        "",
        "## ⚖️ 免责声明与开源协议",
        "",
        "本仓库所列条目均基于开源社区公开信息与开发者官方声明整理，仅供技术研究、学习与工具参考。相关软件版权与知识产权归原作者所有。",
        "",
        "<div align=\"center\">",
        "<sub>Crafted with ❤️ by <a href=\"https://aronshare.com\">AronShare Team</a>. Keeping the open-source spirit alive.</sub>",
        "</div>"
    ])

    OUTPUT_README.write_text("\n".join(lines), encoding="utf-8")
    print(f"[√] 顶级 Awesome README.md 生成完毕！累计收录 {len(posts)} 篇，写入路径: {OUTPUT_README}")

if __name__ == '__main__':
    build_awesome_readme()
