---

> 💡 **资源说明**：本文档为精选摘要镜像，完整高清配置教程、最新版本与网盘高速下载通道请前往 AronShare 官网浏览。

[![封面图片](https://aronshare.com/covers/cover_ntfy-push-notifications.webp)](https://aronshare.com/posts/ntfy-push-notifications/)

---
title: "ntfy 让脚本在任务完成或失败时给手机发通知"
category: "开源自托管"
category_slug: "open-source"
tags: ["ntfy", "自动化", "消息推送", "开源自托管"]
published_at: "2026-10-31 12:08:20"
author: "Aron"
cover: "https://aronshare.com/covers/cover_ntfy-push-notifications.webp"
summary: "ntfy 可以通过 HTTP 请求把脚本结果推送到手机和桌面，适合备份提醒、定时任务告警与下载完成通知。支持公共服务和自托管，使用时需要留意主题访问权限、浏览器后台通知与 iOS 推送配置。"
platforms: ["Web", "Android", "iOS", "Docker"]
license: "Apache-2.0 / GPLv2 双许可证"
pricing: "公共服务提供免费使用与付费套餐；自托管需承担服务器费用"
official_url: "https://ntfy.sh/"
repo_url: "https://github.com/binwiederhier/ntfy"
download_url: "https://docs.ntfy.sh/install/"
source_name: "ntfy 官方文档与 GitHub 仓库"
source_url: "https://github.com/binwiederhier/ntfy"
needs_rewrite: false
---

备份脚本半夜跑完、文件下载结束、定时任务报错，这些结果通常留在电脑的终端或日志里。
想在手机上收到提醒，可以给脚本加一条 ntfy 消息。
它通过 HTTP PUT 或 POST 接收文字，再把消息送到订阅同一主题的手机或桌面端，适合为已有自动化任务补上通知。

## 用主题把脚本和手机连起来

ntfy 的基本单位是主题，也就是一段用来区分消息频道的名称。
在 Android、iOS 应用或网页端订阅一个主题后，脚本向对应地址发送消息，订阅端就能接收。
[官方入门文档](https://docs.ntfy.sh/)提供了 curl、Python 和 JavaScript 等写法，只要现有工具能够发出 HTTP 请求，就有机会把结果接进来。

例如，可以把备份提醒与下载提醒分成不同主题，避免普通进度消息淹没故障通知。
任务是否成功仍由脚本的退出状态决定；ntfy 负责传递脚本已经生成的结果。

![ntfy 官方网页端截图中的主题列表、通知内容与图片附件](https://aronshare.com/assets/post-images/ntfy-push-notifications-ui.png)

*图片来自 ntfy 官方仓库，展示网页端通知与附件界面。*


---

### 📥 资源高速获取与完整教程

本项目已通过官方原版校验并同步收录至 **AronShare 资源库**，提供绿色免安装便携版、夸克网盘转存以及详细配置 SOP。

👉 **[点击前往 AronShare 官网获取完整网盘下载与实操指南](https://aronshare.com/posts/ntfy-push-notifications/)**
