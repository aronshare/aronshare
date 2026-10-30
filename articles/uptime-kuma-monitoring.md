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

## 通知和状态页分别服务不同的人

[项目说明](https://github.com/louislam/uptime-kuma)列出了 Telegram、Discord、Slack、Gotify 和 SMTP 邮件等通知渠道，也支持多个状态页及独立域名映射。
维护者可以接收异常通知，使用服务的人则可以查看状态页，了解相关服务的可用情况。

实际配置时，选择你会及时查看的通知渠道，并确认接收账户与监控项之间的关联。
可以为一个测试地址制造短暂的不可访问状态，检查告警能否送达，恢复后观察状态变化。
这种演练能直接发现通知凭证、网络连接或接收位置配置中的问题。

公开状态页应围绕用户需要了解的服务组织内容。
内部主机名称、私人服务入口和管理用途的备注，适合留在自己的监控面板中。
如果只需要家庭网络内使用，也可以保留内部访问范围。

## 用 Docker 部署时保存好监控数据

[官方 Compose 文件](https://github.com/louislam/uptime-kuma/blob/master/compose.yaml)使用 `louislam/uptime-kuma:2` 镜像，通过 3001 端口提供访问，并把数据保存在 `/app/data` 对应的持久化卷。
准备好 Docker 与 Compose 后，可按[安装文档](https://github.com/louislam/uptime-kuma/wiki/%F0%9F%94%A7-How-to-Install)下载配置，在配置目录执行 `docker compose up -d`。

官方明确要求数据目录使用本地目录或卷，NFS 文件系统不受支持。
部署前确认卷实际保存的位置，把它纳入备份计划，避免重建环境时遗失监控设置与历史数据。
不使用 Docker 的用户，也可以按文档准备 Node.js、Git 和 PM2，通过源码运行。

需要通过域名访问时，参考[反向代理文档](https://github.com/louislam/uptime-kuma/wiki/Reverse-Proxy)。
Uptime Kuma 使用 WebSocket，代理需要正确转发连接升级相关头部；官方建议使用独立域名或子域名，普通子目录部署不受支持。
对公网开放还应配置 HTTPS，并限制不必要的直接端口访问。

## 监控位置和费用也会影响使用方式

Uptime Kuma 使用 [MIT 许可](https://github.com/louislam/uptime-kuma/blob/master/LICENSE)，自托管无需购买软件订阅。
长期运行的主机、存储，以及选用的外部通知服务，可能产生费用。
[官方在线演示](https://demo.kuma.pet/start-demo)适合了解界面，README 明确说明演示数据会在 10 分钟后删除。

选择部署位置时，可以考虑让监控服务与被监控网站分开运行。
两者放在同一台主机上时，整机离线也会让监控程序停止工作；如果希望观察外部访问情况，监控节点还需要具备相应的外部网络视角。

从一个重要网站和一个通知渠道开始，确认检查条件合理、异常能够送达，就能形成一套日常可用的维护提醒。
需要追踪更多服务时，按相同方法逐项验证，避免只增加面板上的监控数量。

- [查看 Uptime Kuma 官方项目](https://github.com/louislam/uptime-kuma)
- [阅读安装文档](https://github.com/louislam/uptime-kuma/wiki/%F0%9F%94%A7-How-to-Install)
- [查看反向代理配置示例](https://github.com/louislam/uptime-kuma/wiki/Reverse-Proxy)
