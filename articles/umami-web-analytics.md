# Umami 装上就能看访问来源，不必给访客挂 Cookie

> 💡 **资源说明**：本文档为精选摘要镜像，完整工具介绍、官方入口与使用条件请前往 AronShare 官网浏览。

[![封面图片](https://aronshare.com/covers/cover_umami-web-analytics.webp)](https://aronshare.com/posts/umami-web-analytics/)

网站装了统计，多数人第一件事是看昨天来了多少人。

第二件事才发现麻烦：访客那边要弹 Cookie 同意条，你自己这边要在一堆菜单里翻半天，才能回答「上周那篇文章到底带来了多少个注册」。

Umami 是冲这两件事来的。它是一套开源的网站与产品分析平台，MIT 许可，数据存在自己的 PostgreSQL 里，页面不写 Cookie，也不做跨站跟踪。

后台长这个样子：Views、Visits、Visitors、跳出率、平均停留时间五个数字排在上面，下面是一条按小时堆叠的柱状图，再往下左边是访问最多的页面，右边是流量来源。

![](https://aronshare.com/assets/post-images/umami-web-analytics/detail-1.webp)

图上这份数据看的是 umami.is 自己，24 小时里 6.75k 浏览量、2.13k 次访问、1.93k 个访客，右上角还挂着实时在线人数。

它真正能干活的地方在这里。

除了页面浏览，它可以自定义事件，把「点了下载按钮」「提交了表单」「看完视频」这类动作单独统计，也可以给事件带数值，用来记金额、时长、次数。

事件能拼成漏斗。下面这张就是官方后台里的漏斗报表，第一条从首页走到定价页，23.1k 个访客里剩 4.90k，转化率 21%；第二条从首页走到文档页再触发 get-started-button 事件，三步走完全程的只剩 105 人。

![](https://aronshare.com/assets/post-images/umami-web-analytics/detail-2.webp)

这种报表的价值在于它能直接回答「哪一步把人漏掉了」，而不用你自己导出数据去拼。

它还把转化和收入接进来了，可以按来源、按活动、按渠道看谁带来了付费，不必把统计工具和收款系统两边的数字手工对。

分享报表不需要给对方开账号，链接发过去就是只读页面。

代价说清楚。

从源码装的话，硬性依赖是 Node.js 18.18 以上加 PostgreSQL 12.14 以上，装完第一次构建会自动建表，并生成默认账号 admin 和密码 umami，这个必须立刻改掉。

默认监听在 localhost:3000，对外提供服务要自己做反向代理。

两因素认证默认不可用，得先设一个 64 位十六进制的 TWO_FACTOR_ENCRYPTION_KEY 才能开启。

官方给了 Docker 镜像 docker.umami.is/umami-software/umami:latest，随附的 compose 文件会顺带跑一个 PostgreSQL，这是最省事的一条路。

不想自己维护服务器，官方云版的免费档每月 0 美元，给 10 万事件、1 个站点、6 个月数据保留；Pro 是 20 美元每月，100 万事件、20 个站点、10 个成员。

谁适合用：手上有一个或几个内容站、独立产品，需要看清来源和转化的；被 Cookie 同意条和合规问题烦过的；不想把访客数据交给第三方的。

谁别碰：一天只有几十个访问量、连日报都不看的新站，装什么统计都是浪费。

官网 umami.is，源码在 github.com/umami-software/umami，README 里同时给了源码安装和 Docker 两条路。

---

### 📖 完整介绍与官方入口

完整文章保留官方资料来源、适用场景及版本和费用条件，下载方式以文章中的实际入口为准。

👉 **[点击前往 AronShare 官网阅读全文](https://aronshare.com/posts/umami-web-analytics/)**
