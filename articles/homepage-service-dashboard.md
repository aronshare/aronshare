# Homepage 让你在一个页面里找到自建服务并查看运行状态

收录日期：2026-10-30

[在 AronShare 阅读](https://aronshare.com/posts/homepage-service-dashboard/)

![Homepage 让你在一个页面里找到自建服务并查看运行状态](https://aronshare.com/covers/cover_homepage-service-dashboard.webp)


给家里搭了网盘、影音库和监控工具后，浏览器书签里往往多出一串域名与端口。
想找某个应用时，需要回忆它的地址；想知道容器是否运行，又得打开另一套管理页面。
Homepage 适合处理这类入口分散的问题，它能把自建服务整理成分组卡片，并通过小组件显示相关数据，功能介绍见[官方仓库](https://github.com/gethomepage/homepage)。

## 从常用服务入口开始整理

Homepage 使用 YAML 文件配置服务。
根据[服务配置文档](https://gethomepage.dev/configs/services/)，可以在 `services.yaml` 中建立分组，为服务填写访问地址、图标和说明，也能继续嵌套分组。

例如，把网盘与笔记工具放进“资料”，把服务器和监控工具放进“维护”，家人使用的影音应用单独成组。
这样的分类按使用目的展开，打开页面就能判断该去哪里。
只需要链接导航时，填写服务地址即可；希望显示应用中的数据，则需要继续配置相应小组件。

![Homepage 官方展示的服务卡片与系统状态面板](https://aronshare.com/assets/post-images/homepage-service-dashboard-official-ui.png)

*图片来自 Homepage 官方仓库，展示配有背景图和展示边框的真实界面示例，卡片数据为官方示例内容。*

## 链接和小组件使用的地址可能不同

[官方服务文档](https://gethomepage.dev/configs/services/)将 `href` 用作点击卡片后打开的地址，小组件则使用自己的 `url` 与服务凭证读取数据。
例如，用户访问应用可以走公开域名，Homepage 与应用之间的数据请求则可以使用双方能够连接的内部地址。

配置时需要分别检查浏览器能否打开服务、Homepage 容器能否访问组件接口。
对于需要 API Key 的服务，应按对应组件文档填写凭证，并妥善保存配置文件。
官方说明后端服务请求由 Homepage 代理，以减少在浏览器端暴露 API Key 的情况；能够看到面板的人仍可能看到组件展示的私人信息。

页面也可以显示时间、天气和搜索等信息，具体项目见[官方功能说明](https://github.com/gethomepage/homepage#features)。
这些内容适合按使用频率取舍，页面保留经常会点开的服务与真正需要查看的数据即可。

## Docker 自动发现需要明确配置

[Docker 集成](https://gethomepage.dev/configs/docker/)可以读取容器状态，并通过标签发现服务。
在容器上填写 `homepage.group`、`homepage.name` 和 `homepage.href` 等标签后，已配置的 Docker 连接可以把对应服务加入面板。

这项能力适合经常增减容器的人，不过它需要访问 Docker 接口。
官方文档提供了 Docker Socket Proxy 方案，用受限制的接口连接，示例中还禁用了 POST 操作。
只想整理链接时，可以省去 Docker 集成；决定启用时，应一并考虑接口权限与网络访问范围。

## 部署时把主机名和登录保护配置好

[官方仓库](https://github.com/gethomepage/homepage#with-docker)给出了 Docker Compose 示例，使用 `ghcr.io/gethomepage/homepage:latest` 镜像，把配置目录挂载到 `/app/config`，并映射 3000 端口。
配置目录需要持久保存，更新容器时继续使用同一份目录。

[安装文档](https://gethomepage.dev/installation/)要求通过非本机地址访问时设置 `HOMEPAGE_ALLOWED_HOSTS`，填写实际使用的域名或 IP，必要时包含端口。
遇到主机名校验错误，应对照日志核对访问地址，保留明确的允许列表。

同一份文档说明，Homepage 从 2.0 起提供可选的密码或 OIDC 登录功能，需要显式启用并配置相应环境变量。
对外开放时仍应使用带访问保护的反向代理或 VPN，配置 TLS，并对密码登录请求设置限速。
这类安全设置应与服务上线一起完成，尤其是面板连接了家庭自动化或私人资料服务时。

## 适合愿意维护配置文件的人

Homepage 采用 [GPL-3.0 开源许可](https://github.com/gethomepage/homepage/blob/dev/LICENSE)，自托管无需购买软件订阅。
运行主机与所连接的第三方服务各自计算成本，付费应用接入面板后仍按原有规则收费。

它的配置方式适合愿意编辑 YAML、管理地址和凭证的人。
如果需求只是保存几个网址，浏览器书签已经足够直接；当你还希望同时查看服务数据、容器状态，并为不同用途整理入口，Homepage 才能发挥更完整的作用。
可以从几个常用服务开始配置，确认链接可达与组件正常后，逐步补齐真正需要的信息。

- [访问 Homepage 官方文档](https://gethomepage.dev/)
- [查看源码和 Docker 配置示例](https://github.com/gethomepage/homepage)
- [阅读服务分组与小组件配置](https://gethomepage.dev/configs/services/)
