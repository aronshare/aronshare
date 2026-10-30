# FreshRSS 让你在自己的阅读器里集中追踪博客和网站更新

收录日期：2026-10-30

[在 AronShare 阅读](https://aronshare.com/posts/freshrss-feed-reader/)

![FreshRSS 让你在自己的阅读器里集中追踪博客和网站更新](https://aronshare.com/covers/cover_freshrss-feed-reader.webp)


关注的博客越来越多，检查更新就变成了反复打开网页、寻找上次读到的位置。
FreshRSS 适合把这件事集中处理：你选择订阅来源，阅读器收集更新，读过的文章留下状态，需要的内容可以收藏。
它是一款能部署在自己服务器上的 RSS 阅读器，提供网页版，也支持兼容客户端接入，具体能力见[官方项目说明](https://github.com/FreshRSS/FreshRSS)。

## 让订阅清单围绕自己的兴趣展开

添加订阅时，可以填写 RSS 或 Atom 地址；网站按标准声明了订阅源时，FreshRSS 也能从网站地址中发现它。
[订阅管理文档](https://freshrss.github.io/FreshRSS/en/users/04_Subscriptions.html)还介绍了分类和 OPML 导入，方便迁入已有的订阅清单。

如果你关注软件开发，可以把项目博客、技术教程、行业消息分成几组。
日常阅读围绕当前任务展开，写代码时查看技术组，收集选题时查看行业组，避免一打开阅读器就面对所有未读文章。
分类名称由自己决定，保留真正会读的来源，比不断扩充订阅数量更容易坚持。

![FreshRSS 官方历史示例中的订阅分类与文章列表](https://aronshare.com/assets/post-images/freshrss-feed-reader-official-ui.png)

*图片来自 FreshRSS 官方仓库，截图中的示例文章日期为 2014 年，展示订阅列表的组织方式。*

## 阅读和整理可以在同一处完成

[阅读视图文档](https://freshrss.github.io/FreshRSS/en/users/03_Main_view.html)提供普通、全局和阅读三种模式。
普通视图适合浏览标题，并按分类或单个订阅源查看；文章旁的已读状态与收藏星标，方便区分已经处理和准备留存的内容。
想逐篇展开阅读时，可以切换阅读视图。

手机端可以使用网页，也可以从[官方兼容客户端列表](https://github.com/FreshRSS/FreshRSS#apis--native-apps)挑选应用。
这些客户端通过 Google Reader 或 Fever 兼容 API 连接 FreshRSS，支持的标签、离线阅读和订阅管理能力各有差异。
选择时核对自己会用到的功能，也留意客户端是否单独收费。

## 网页抓取需要匹配具体网站

遇到没有 RSS 的网页，[内置抓取功能](https://freshrss.github.io/FreshRSS/en/users/11_website_scraping.html)可以通过 HTML 与 XPath 提取条目，也支持 JSON 路径配置。
这类设置需要明确标题、链接和内容位于页面的哪个位置，适合愿意调整规则的人。

网站结构变化后，原来的路径可能需要更新。
对于只提供摘要的订阅源，可以查看[完整内容提取设置](https://freshrss.github.io/FreshRSS/en/users/04_Subscriptions.html)，为正文配置选择器。
FreshRSS 不运行网页 JavaScript，依赖脚本加载的正文无法直接按这套方式提取。
能否获取完整内容仍取决于目标网页的结构与访问条件；涉及登录或订阅的文章，应使用网站提供的合法阅读入口。

## 自托管要安排刷新和备份

[官方 Docker 文档](https://github.com/FreshRSS/FreshRSS/blob/edge/Docker/README.md)提供镜像和部署示例，将数据目录与扩展目录分别持久化，并通过 `CRON_MIN` 设置订阅刷新时间。
例如文档中的 `1,31` 表示每小时第 1 分钟和第 31 分钟刷新，时区也应按使用地点配置。
容器启动后，打开服务地址完成网页安装即可。

愿意自行维护 PHP 环境，也可以参考[手动安装说明](https://freshrss.github.io/FreshRSS/en/admins/03_Installation.html)。
对外开放时只暴露应用的 `p` 目录，保存个人数据的 `data` 目录需要保持私有。
服务器运行、软件更新与资料备份，都需要纳入日常维护。

## 把费用和维护时间一起考虑

FreshRSS 采用 AGPL-3.0 开源许可，自托管使用无需购买软件订阅，服务器、存储与运维仍由自己承担。
官网列出的[第三方托管服务](https://freshrss.org/cloud-providers.html)有各自的套餐和条件，适合希望减少维护工作的人。

开始使用时，可以只放入几项每周都会查看的来源，观察分类是否好找、文章能否正常刷新、手机阅读是否顺手。
当这份阅读清单确实帮你追上关注的网站，扩展订阅范围就有了清晰方向。

- [访问 FreshRSS 官网](https://freshrss.org/)
- [查看源码与客户端兼容列表](https://github.com/FreshRSS/FreshRSS)
- [阅读 Docker 部署说明](https://github.com/FreshRSS/FreshRSS/blob/edge/Docker/README.md)
