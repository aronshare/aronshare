# Uptime Kuma 帮你持续检查网站是否在线并在异常时发出通知

> 💡 **资源说明**：本文档为精选摘要镜像，完整高清配置教程、最新版本与网盘高速下载通道请前往 AronShare 官网浏览。

[![封面图片](https://aronshare.com/covers/cover_uptime-kuma-monitoring.webp)](https://aronshare.com/posts/uptime-kuma-monitoring/)

# Uptime Kuma 帮你持续检查网站是否在线并在异常时发出通知

收录日期：2026-10-30

[在 AronShare 阅读](https://aronshare.com/posts/uptime-kuma-monitoring/)

![Uptime Kuma 帮你持续检查网站是否在线并在异常时发出通知](https://aronshare.com/covers/cover_uptime-kuma-monitoring.webp)


网站打不开时，最让人被动的情况是用户已经发来消息，维护者才发现服务出了问题。
Uptime Kuma 可以持续检查指定的网站和服务，并把异常发送到你配置的通知渠道。
对于自己维护博客、小型网站或家庭服务器的人，它提供了一套可以部署在自己设备上的监控面板，功能范围见[官方项目说明](https://github.com/louislam/uptime-kuma)。

## 检查方式要对应你关心的问题

Uptime Kuma 支持 HTTP 和 HTTPS、TCP 端口、Ping、DNS 记录、WebSocket、Docker 容器，以及网页关键词和 JSON 查询等监控类型。
这些检查各自回答不同的问题：端口检查关注连接，网页关键词检查关注响应内容，DNS 检查关注解析记录。
相关类型列在[官方功能清单](https://github.com/louislam/uptime-kuma#-features)中。

例如，一个网站能够返回页面，却只显示维护提示。
如果你关心首页内容是否正常，可以考虑关键词检查，并选择页面中相对稳定的文字。
动态活动标题经常变化，适合作为阅读内容，用它作为健康检查条件则容易产生误报。
监控目标应尽量贴近你希望及时发现的故障。

![Uptime Kuma 官方展示的网站监控面板](https://aronshare.com/assets/post-images/uptime-kuma-monitoring-official-ui.jpg)

*图片来自官方 README，展示历史示例中的在线状态、响应时间与统计曲线，图内数据属于官方演示内容。*


---

### 📥 资源高速获取与完整教程

本项目已通过官方原版校验并同步收录至 **AronShare 资源库**，提供绿色免安装便携版、夸克网盘转存以及详细配置 SOP。

👉 **[点击前往 AronShare 官网获取完整网盘下载与实操指南](https://aronshare.com/posts/uptime-kuma-monitoring/)**
