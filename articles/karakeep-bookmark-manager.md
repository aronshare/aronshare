# Karakeep 帮你把收藏的网页和图片整理成可搜索的资料库

收录日期：2026-10-30

[在 AronShare 阅读](https://aronshare.com/posts/karakeep-bookmark-manager/)

![Karakeep 官方界面](https://aronshare.com/covers/cover_karakeep-bookmark-manager.webp)

收藏了一篇教程、一张设计参考图和几个产品链接，过几天要用，却忘了分别存在哪个应用里。
如果你经常遇到这种情况，可以看看 Karakeep。
它能把网页、笔记、图片和 PDF 集中保存，再通过标签、列表和搜索找回来。

## Karakeep 能保存哪些内容

Karakeep 是一款支持自托管的开源收藏工具，原名 Hoarder。
保存网页链接时，它会自动获取标题、描述和配图，方便浏览；零散的文字想法、图片和 PDF 也可以放进去。
Chrome、Firefox 和 Safari 有配套扩展，手机端提供 iOS 和 Android 应用。
这些功能和入口都能在[官方项目说明](https://github.com/karakeep-app/karakeep)中找到。

![Karakeep 官方展示的网页端收藏卡片与手机端界面](https://aronshare.com/assets/post-images/karakeep-official-ui.webp)

*图片来自 Karakeep 官方仓库，展示网页端与手机端的收藏界面。*

## 收藏多了还能按内容找回来

Karakeep 支持全文搜索，也提供阅读视图和文字高亮。
阅读教程时，可以标出重要段落；收集同一个项目的资料时，可以放进对应列表。
[官网](https://karakeep.com/)还介绍了 RSS 自动收藏和规则管理，例如按照链接特征给新书签添加标签、加入列表。

对做内容的人来说，可以用一个列表收集选题依据，另一个列表保存配图参考。
写稿时围绕主题检索，找到相关原文后核对细节，会比在聊天收藏夹里逐条翻找更有条理。
这是一种使用建议，列表名称可以按自己的工作来设。

## AI 标签需要配置模型

自动标签和摘要依赖模型服务。
根据[官方配置说明](https://docs.karakeep.com/configuration/environment-variables/)，配置模型连接后才能启用 AI 自动标签，摘要还有独立开关。
项目支持通过 Ollama 使用本地模型，也能接入兼容的在线模型接口。

模型选择会影响标签质量、运行速度和成本。
使用云端模型时，需要考虑发送给模型的收藏内容；希望控制资料流向，可以评估本地模型与自己的硬件条件。
只想管理书签和阅读资料，也可以暂时不配置 AI。

## 自托管需要准备什么

[官方 Docker 安装文档](https://docs.karakeep.com/installation/docker/)要求准备 Docker 和 Docker Compose，下载项目提供的 Compose 文件，并设置服务地址与随机密钥。
完成配置后，用 `docker compose up -d` 启动服务。
数据持久化和服务之间的连接已包含在官方 Compose 方案中。

自托管适合愿意维护服务器、备份资料的人。
软件采用开源许可，服务器、存储和所选模型的费用需要自己承担。
如果希望省去服务器维护，项目也提供云服务，订阅条件以官网为准。

## 从一个具体的资料夹开始使用

可以围绕正在做的项目，放入几篇常用教程、产品链接和参考图。
使用时关注三个问题：保存是否顺手，搜索能否找到需要的内容，列表和标签是否符合自己的习惯。
这些环节顺畅后，再决定是否开启 AI 摘要、RSS 自动收藏等功能。

- [访问 Karakeep 官网](https://karakeep.com/)
- [查看 GitHub 源码](https://github.com/karakeep-app/karakeep)
- [阅读 Docker 安装文档](https://docs.karakeep.com/installation/docker/)
