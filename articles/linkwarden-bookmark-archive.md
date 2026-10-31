# Linkwarden 帮你保存网页副本并和同事整理参考资料

[网站全文](https://aronshare.com/posts/linkwarden-bookmark-archive/)

![Linkwarden 官方界面](https://aronshare.com/covers/cover_linkwarden-bookmark-archive.webp)


做一个项目时，教程、产品文档和参考案例往往散在浏览器书签、聊天记录与笔记里。
等到需要引用，原网页可能已经改版，收藏时看中的内容也跟着消失了。
Linkwarden 可以围绕同一个项目整理链接，并为网页保存多种副本，让日后查资料时多一份可用的依据。

## 收藏网页时也把内容留下来

[Linkwarden](https://github.com/linkwarden/linkwarden) 是一款开源书签管理工具，支持自托管，也提供官方云服务。
保存链接后，后台会处理网页，根据启用的选项生成阅读视图、完整 HTML、截图和 PDF。
阅读视图方便看文章，HTML 副本保留页面样式与图片，截图和 PDF 则适合回看当时的页面内容。

这些格式由后台逐步生成，新加入的链接会经历等待处理的状态。
需要长期引用的资料，可以打开链接详情里的 Preserved Formats，确认实际保存了哪些格式，并下载重要副本。
[官方存档说明](https://docs.linkwarden.app/usage/preservation)也提醒，重新抓取会删除已有副本；原站已经下线的页面，适合保留现有存档，避免随手刷新。

![Linkwarden 官方展示的桌面资料集合与手机端收藏界面](https://aronshare.com/assets/post-images/linkwarden-bookmark-archive-ui.png)

*图片来自 Linkwarden 官方仓库，展示桌面和手机端的书签界面。*

## 用集合组织资料并分配协作权限

Linkwarden 支持集合、子集合和多个标签，还能修改链接名称与描述。
例如准备一个网站改版项目，可以按“设计参考”“技术方案”“用户研究”建立集合，用标签补充具体主题。
同事收集的材料可以放进共同的集合，成员权限按分工设置，需要对外展示的资料也能公开分享。
这些能力在[官方功能清单](https://github.com/linkwarden/linkwarden#features)中有明确说明。

阅读视图支持高亮和批注，适合把“为什么保存这篇文章”写在相关段落旁边。
对于团队资料夹，简短批注能够说明一条链接和当前项目的关系，减少后来接手的人重新阅读整篇文章的负担。
公开集合前应检查其中的内容，内部文档和带有个人信息的页面适合留在受限集合里。

## 全文搜索和网页存档各有条件

收藏较多时，全文搜索可以从保存的文章正文里查找关键词。
按照[官方文档](https://docs.linkwarden.app/usage/preservation#full-text-search)，这项能力依赖 Meilisearch；官方云服务已提供，自托管实例需要具备相应配置。
没有该服务时，搜索范围包括链接名称、地址、描述和标签。

网页抓取由服务器以匿名访问者身份进行。
遇到登录页面、付费内容或网站拦截时，存下来的可能是登录提示或拦截页面；过长、过慢或超出大小限制的页面，也可能缺少部分格式。
这类资料需要检查保存结果，有访问权限的用户还可参考官方的浏览器保存方案。
存档功能应围绕自己有权访问和保存的内容使用。

## 自托管要准备服务器和备份空间

[官方安装文档](https://docs.linkwarden.app/self-hosting/setup)提供 Docker Compose 方案，建议以双核处理器、4 GB 内存作为较舒适的起点，并为镜像和收藏内容预留磁盘空间。
配置时需要设置服务地址，以及彼此不同的认证密钥、搜索密钥和数据库密码。
正式长期使用还应安排数据备份，网页截图、PDF 和 HTML 会随着收藏量持续占用空间。

Linkwarden 采用 AGPL-3.0 许可，自托管需要自己承担服务器、存储与维护成本。
希望省去部署维护，可以选择官方付费云服务，订阅方案通过官网查看。
手机应用需要连接已有的 Linkwarden 账户，可以使用云端账户或自己的实例。

如果你的收藏常被用作工作依据，可以围绕一个正在进行的项目建立集合，放入几篇真正会再次引用的文章。
检查副本能否打开、批注是否便于理解、同事的访问权限是否合适，这些具体体验更能帮助你判断它是否适合长期使用。

- [访问 Linkwarden 官网](https://linkwarden.app/)
- [查看官方源码与功能说明](https://github.com/linkwarden/linkwarden)
- [阅读自托管安装文档](https://docs.linkwarden.app/self-hosting/setup)
- [了解网页存档的条件与限制](https://docs.linkwarden.app/usage/preservation)
