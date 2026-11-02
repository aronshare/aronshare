---

> 💡 **资源说明**：本文档为精选摘要镜像，完整高清配置教程、最新版本与网盘高速下载通道请前往 AronShare 官网浏览。

[![封面图片](https://aronshare.com/covers/cover_changedetection-website-monitor.webp)](https://aronshare.com/posts/changedetection-website-monitor/)

---
title: "changedetection.io 帮你盯住网页变化并在需要时发来提醒"
category: "开源自托管"
category_slug: "open-source"
tags: ["changedetection.io", "网页监控", "自动化", "开源自托管"]
published_at: "2026-10-31 10:30:00"
author: "Aron"
cover: "https://aronshare.com/covers/cover_changedetection-website-monitor.webp"
summary: "changedetection.io 可以定期检查网页、记录内容差异并发送提醒，适合追踪公告、招聘信息、商品价格和补货状态。支持筛选页面区域、浏览器交互与多种通知渠道，可自托管，也有付费托管服务。"
platforms: ["Web", "Docker", "Python"]
license: "Apache-2.0"
pricing: "开源自托管；官方另有付费托管，服务器、代理及可选模型费用需按使用方式承担"
official_url: "https://changedetection.io/"
repo_url: "https://github.com/dgtlmoon/changedetection.io"
download_url: "https://github.com/dgtlmoon/changedetection.io#installation"
source_name: "changedetection.io 官网与官方 GitHub 仓库"
source_url: "https://github.com/dgtlmoon/changedetection.io"
needs_rewrite: false
---

有些公告页没有订阅入口，商品补货也没有邮件提醒，只能隔一段时间打开网页查看。
changedetection.io 可以替你定期检查这些页面，保存变化记录，并把符合条件的更新发到通知渠道。
它适合持续关注一组已知网页，尤其是你只关心其中某个区域或某类变化的时候。

## 把反复打开的网页加入监控列表

在 changedetection.io 中添加网页地址，并设置检查间隔，就可以建立一条监控任务。
后续检查发现变化时，可以打开差异记录，查看增加、删除或修改了哪些文字。
[官方项目说明](https://github.com/dgtlmoon/changedetection.io)介绍了按单词、行和字符查看差异的方式，也支持 PDF 文本变化与 JSON 数据监控。

例如，招聘页面可以关注职位列表，产品网站可以关注更新日志，公共信息网站可以关注公告正文。
这些场景有一个共同点：你已经知道信息会出现在哪里，希望更新出现时收到提醒。
检查间隔由任务配置决定，通知时间也受目标网站响应和抓取情况影响。

![changedetection.io 官方截图中的监控列表、文字变化与价格历史图](https://aronshare.com/assets/post-images/changedetection-website-monitor-ui.png)

*图片来自 changedetection.io 官方仓库，展示任务列表、变化摘要和商品价格历史。*


---

### 📥 资源高速获取与完整教程

本项目已通过官方原版校验并同步收录至 **AronShare 资源库**，提供绿色免安装便携版、夸克网盘转存以及详细配置 SOP。

👉 **[点击前往 AronShare 官网获取完整网盘下载与实操指南](https://aronshare.com/posts/changedetection-website-monitor/)**
