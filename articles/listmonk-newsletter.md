# Listmonk 用一个二进制文件发邮件，七百万封只占 57MB 内存

> 💡 **资源说明**：本文档为精选摘要镜像，完整工具介绍、官方入口与使用条件请前往 AronShare 官网浏览。

[![封面图片](https://aronshare.com/covers/cover_listmonk-newsletter.webp)](https://aronshare.com/posts/listmonk-newsletter/)

做 Newsletter 的人，卡点很少在写。

在发。

发信域名要验，SPF、DKIM、DMARC 要配，退信要处理，订阅要确认真实的还是灌水的；平台按月按人头收费，订阅数涨到五万，账单也跟着跳一档。

Listmonk 是冲着这层来的。它是开源的邮件列表与 Newsletter 管理系统，AGPL-3.0，一个二进制文件加一个 PostgreSQL 就能跑起来。

整个东西只有两样东西：Go 编译的单文件程序，和一张 Postgres 库。没有 Node、没有额外中间件，内存和 CPU 占用都低到不像话。

官方公布过一个生产实例：一次 campaign 发七百万封邮件，CPU 占用不到单核的一小部分，峰值内存 57MB。

![](https://aronshare.com/assets/post-images/listmonk-newsletter/detail-1.webp)

打开后台是这样一个面板：列表数、订阅者数、campaign 数、发送量，中间是 campaign 浏览量和链接点击两条曲线，右边是系统状态（运行时长、进程内存、系统内存、CPU 负载）。

下面这些是它真正能干活的部分。

订阅者管理支持单向和双向确认（double opt-in），支持用 SQL 表达式直接分群：按订阅时间、打开过哪些 campaign、点了哪些链接，都能写成条件筛出人群。

模板不只是填个空。它用 Go 模板语法，支持表达式、逻辑判断和一百多个内置函数，标题行和正文都能套。邮件界面有四种做法：可视化拖拽、所见即所得编辑器、Markdown、原生 HTML 加代码高亮，也可以用纯文本。

![](https://aronshare.com/assets/post-images/listmonk-newsletter/detail-2.webp)

发送是多线程、多 SMTP 的队列，带吞吐量和滑动窗口限速。换句话说，你有多个发信通道可以轮着用，不会一个域名打到黑。

分析是内置的：campaign 表现、打开、点击、退信、热门链接，不用另装统计。

再往外还有两块常被忽略的：一个是事务邮件 API，用预设模板给订阅者发任意通知，能走邮件、短信、WhatsApp 或任何 Messenger 通道；另一个是完整的 API 覆盖，加上 Messenger HTTP webhook。媒体库支持 S3 兼容存储。

权限方面有 OIDC 单点登录、细分角色和限定了作用域的 API token。订阅者要导出自己的数据或者要求彻底删除，后台能处理。

代价说清楚。

第一，发信这块它不替你解决。SMTP 服务器要自己配，可以是你的 VPS，也可以是 Amazon SES、Postmark 这类服务商，但域名验证、SPF、DKIM、DMARC、IP 信誉都要你自己打理。发不进收件箱，问题九成在这里，不在软件。

第二，退信和投诉处理要自己看。Listmonk 会给数据，但决定谁该被拉黑是你的事。

第三，数据库要自己备份。它是单文件程序加 Postgres，好处是简单，坏处是出问题没人兜底。

第四，官网首页现在挂的是 v7.0.0-beta.2，发布日期就是今天。想上生产就别用 beta，等稳定版。

谁适合用：手上已经有域名、愿意花半天把发信信誉这件事理顺的人；给自己做 Newsletter、给产品做通知邮件、或者一个团队要统一管几个邮件列表的，这套东西的成本比按月付费低一个量级。

谁别碰：连域名邮箱都没配过的新手。你会把时间全花在为什么邮件进垃圾箱上，而不是写内容上。

官网 listmonk.app 上有在线 demo，不用装就能点开看后台长什么样。仓库在 github.com/knadh/listmonk，安装文档给了 Docker 和二进制两条路。

---

### 📖 完整介绍与官方入口

完整文章保留官方资料来源、适用场景及版本和费用条件，下载方式以文章中的实际入口为准。

👉 **[点击前往 AronShare 官网阅读全文](https://aronshare.com/posts/listmonk-newsletter/)**
