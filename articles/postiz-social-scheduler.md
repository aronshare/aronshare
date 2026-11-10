# Postiz 是能自己部署的社媒排期工具，账号和次数都不限量

> 💡 **资源说明**：本文档为精选摘要镜像，完整工具介绍、官方入口与使用条件请前往 AronShare 官网浏览。

[![封面图片](https://aronshare.com/covers/cover_postiz-social-scheduler.webp)](https://aronshare.com/posts/postiz-social-scheduler/)

做内容的人真正卡住的地方，从来不是写不出东西。

是写完之后那一层：十几个账号，谁发哪个平台，什么时候发，上一条发出去没有，这条能不能顺手改成 Instagram 的版本再发一遍。

全靠手工，就一定会有漏发、错时区和重复发的日子。

Postiz 就是冲这一层来的。它是开源的社媒排期与内容管理工具，代码以 AGPL-3.0 发布，可以自己部署在服务器上。

先说它认多少平台：Instagram、YouTube、Dribbble、LinkedIn、Reddit、TikTok、Facebook、Pinterest、Threads、X、Slack、Discord、Mastodon、Bluesky。官方仓库首页列出的就是这些。

![](https://aronshare.com/assets/post-images/postiz-social-scheduler/detail-1.webp)

进去以后是一张周历。左边是频道列表，可以先点「Generate Posts」让 AI 起草一批，也可以自己写；主区按时间格子排，每个账号的帖子落在自己的格子里，改时间就是拖一下。

一次写、多平台发是它的基本盘。同一篇内容按各平台的格式拆成不同版本，日历上能看见全局节奏，不用切五个网页后台。

再往上，它把内容团队那些零碎活都收进同一个界面：重复发布、发帖评论与延迟、内容签名、RSS 自动发、客户分组、内部与全局 Plugs。团队协作和「向外部创作者买帖」也在里面，界面上就有 Messages 和 Marketplace。

![](https://aronshare.com/assets/post-images/postiz-social-scheduler/detail-2.webp)

分析在同一个后台。页面曝光、帖子曝光、互动、视频播放、粉丝变化都能看，时间范围可切 90 天。

还有一个容易被忽略的点：它有公开 API 和 webhook，也能通过 MCP、CLI 以及 Claude、ChatGPT、Codex、OpenClaw、Cursor 这些连接器接进去。也就是说，让 AI agent 直接往排期队列里塞内容，是它设计里的一部分，不是外挂。

代价要说清楚，这是自部署真正花时间的地方。

第一，每个平台的开发者应用要你自己去申请、自己过审。Meta、YouTube、TikTok 这几家，等的周期是按周算的。云版之所以贵，贵的就是这批已经过审的应用。

第二，要自备基础设施：Postgres、Redis、对象存储和一堆环境变量。官方给了 Docker 镜像和 docker-compose，Coolify、Railway、任意 VPS 都能跑，但不是一键就能用的东西。

第三，分析要跑起来，得在你的应用凭据里加对应的数据权限；AI 功能（Copilot、AI 图、AI 视频、Smart Agent）要自带 OpenAI 等供应商的 key，费用直接付给模型方。

第四，升级要自己拉新镜像、跑数据库迁移；备份、可用性、安全补丁也都是你自己的事。

所以谁该用，谁别碰。

同时运营多个账号、做矩阵、做代运营、或者内容团队超过三个人的，这套东西能省掉大量切后台和盯发布的时间，值得折腾一次。

只想发一两个账号的人，别碰。云版按月付的那点钱，比自己维护一套 Postgres 加 Redis 便宜得多。

它没有阉割版：官方说得很直白，开源版不锁功能、不限许可证，云版和自部署版是同一套核心产品，差别只在基础设施、平台审核、和谁负责运维。

仓库在 github.com/gitroomhq/postiz-app，部署步骤看 docs.postiz.com/quickstart。近两天仓库还在提交代码，项目是活的。

---

### 📖 完整介绍与官方入口

完整文章保留官方资料来源、适用场景及版本和费用条件，下载方式以文章中的实际入口为准。

👉 **[点击前往 AronShare 官网阅读全文](https://aronshare.com/posts/postiz-social-scheduler/)**
