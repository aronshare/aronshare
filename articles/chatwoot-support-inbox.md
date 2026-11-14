# Chatwoot 把网站聊天和邮件汇进同一个客服收件箱

> 💡 **资源说明**：本文档为精选摘要镜像，完整工具介绍、官方入口与使用条件请前往 AronShare 官网浏览。

[![封面图片](https://aronshare.com/covers/cover_chatwoot-support-inbox.webp)](https://aronshare.com/posts/chatwoot-support-inbox/)

网站在线聊天挂着一个窗口，邮件里还躺着三十封没回，WhatsApp 那头客户已经在追问第二遍，客服得开三个标签页来回抄。
回复慢上半小时，单子往往就凉了，这是小团队做客服最常见的失血点。
Chatwoot 把这些入口收进一个收件箱，官方仓库第一行写着它是 Intercom、Zendesk 的开源替代品。
许可证是 MIT，核心代码可以商用、可以改、可以整套部署在内网。
打开后台，最左一栏是收件箱、提及、参与中、未分配和按业务切好的队列，中间是会话列表，右边是联系人资料加分配、优先级、标签。
会话里能直接切到私密备注，同事之间 @ 一下就能接手。
预设回复和宏把常见问题的答复压成一键，自动分配按坐席在线情况派单。
左侧收件箱那个数字角标，是客服每天真正盯的东西。
![](https://aronshare.com/assets/post-images/chatwoot-support-inbox/detail-1.webp)
这张图是官方演示环境，左边 All Conversations 下面挂着 Tech queue、Billing queue、Open bugs 三个队列，中间的会话分别来自 Facebook、Instagram、WhatsApp、Website、Email 五个渠道，右边把联系人 Lorrie 的邮箱、电话、公司、优先级 High 和 login-issue 标签一次摆开。
这条会话从客户说登不上网页版，到客服让清缓存，再到客户回一句 Perfect，整条链路都留在同一个线程里，没有跑到邮箱里重开一封。
另一块能力是帮助中心门户，可以自己发文章、FAQ 和指南，让客户先自助查答案。
![](https://aronshare.com/assets/post-images/chatwoot-support-inbox/detail-2.webp)
第二张图就是它的帮助中心首页，顶部一个全文搜索框带 ⌘K 快捷键，左侧按 Getting started、Plans and billing、Projects and tasks 分类排开，主区是分类卡片和热门主题胶囊按钮。
客服在会话里贴一条帮助中心链接，比重复解释十遍省事。
报表里有会话量、坐席、收件箱、标签、团队五类，外加 CSAT 满意度。
Captain 是官方内置的 AI 客服，能自动回常见问题、给坐席写回复草稿、把长对话压成摘要。
自托管的前提不算轻，官方文档写的是 4 核 CPU、4GB 内存起步，这个配置撑到每天一万条会话，翻倍要加到 8 核 8GB。
数据库只支持 PostgreSQL，Redis 要 7.0 以上，后台任务压在 Sidekiq 上，官方说这个进程忙起来能吃到 1GB 以上内存。
装完还得补 1GB swap，不然升级时容易被打爆。
Docker 和 Docker Compose V2 是最省事的路子，环境变量漏配就会缺功能。
钱的部分要看清楚，自托管 Community Edition 是 0 美元一个坐席，免费永久。
Captain AI、语音通话、自定义品牌、坐席容量管理、角色权限、SAML 单点登录、SLA 策略全都不在社区版里。
想打开这些，Premium Support 报价 19 美元一个坐席一个月，Enterprise Edition 99 美元。
云端版 Hacker 档 0 美元，限 2 个坐席、每月 500 条会话、数据只留 30 天，Startups 19 美元、Business 39 美元、Enterprise 99 美元，都是一个坐席一个月的价格。
适合谁的判断很简单，三五个人轮班、渠道超过两个、又不想把客户对话托管给第三方的团队最合适。
只做单一渠道、每天十几条咨询的小站，养一套 Rails 加 PostgreSQL 的运维成本会高过省下来的订阅费。
要白牌转售，或者要原厂中文支持，社区版给不了。
部署文档在 chatwoot.com/docs/self-hosted/deployment/docker，代码仓库在 github.com/chatwoot/chatwoot。
文中截图取自官方演示数据，界面里的客户名、工单编号和对话都是样例。

---

### 📖 完整介绍与官方入口

完整文章保留官方资料来源、适用场景及版本和费用条件，下载方式以文章中的实际入口为准。

👉 **[点击前往 AronShare 官网阅读全文](https://aronshare.com/posts/chatwoot-support-inbox/)**
