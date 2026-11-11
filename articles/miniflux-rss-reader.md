# Miniflux 跑 RSS 阅读器只用一个文件，几百个源几 MB

> 💡 **资源说明**：本文档为精选摘要镜像，完整工具介绍、官方入口与使用条件请前往 AronShare 官网浏览。

[![封面图片](https://aronshare.com/covers/cover_miniflux-rss-reader.webp)](https://aronshare.com/posts/miniflux-rss-reader/)

做内容的人每天缺的是筛选。

打开社交平台，算法推给你的是它想让你看的；打开十几个公众号和博客，光点开就花掉一小时。

RSS 这个老办法反而还在。问题是大部分阅读器越做越重，一个页面加载几十个请求，看完一轮眼睛疼。

Miniflux 走的是另一条路。它是 Apache-2.0 许可的 RSS 阅读器，用 Go 编译成单个静态二进制文件，静态资源直接用 embed 打进程序内，装完就是跑。

![](https://aronshare.com/assets/post-images/miniflux-rss-reader/detail-1.webp)

界面就这么朴素：顶上一排导航，Unread 后面跟着未读数，下面是文章列表，每行是标题、来源域名、发布时间，行末三个操作 Save、Original、Star。

不给你推荐，不给你猜你喜欢，也不放信息流广告位。打开就是你自己订的那几十个源，看完清空。

支持的格式覆盖 Atom 0.3 和 1.0、RSS 1.0 和 2.0、JSON Feed 1.0 和 1.1，OPML 能导入导出，从别的阅读器搬家不用手工重订。

点开一篇文章是阅读视图，正文去掉原站的侧栏和广告，只留内容。

![](https://aronshare.com/assets/post-images/miniflux-rss-reader/detail-2.webp)

底下有上一篇和下一篇，键盘按 J、K 就能翻，看完按一下标为已读，全程不用摸鼠标。

搜索这块值得单说。它把全文搜索交给 PostgreSQL 直接做，不额外装 Elasticsearch 之类的搜索引擎，几十万篇历史文章搜起来还是秒回。

隐私侧的处理比多数阅读器都认真：去像素追踪、剥掉 utm_ 系列和 fbclid 之类的追踪参数、YouTube 视频用 youtube-nocookie 域名播放、禁止外部 JavaScript、加了 CSP 和 Trusted Types。

换句话说，你订了什么源，不会变成别人手里的画像。

技术上，官方给了 Debian 包、RPM 包、预编译二进制和多架构 Docker 镜像，ARM 和 RISC-V 都有，树莓派能跑。

资源占用低到夸张，官方说几百个订阅源也只吃几 MB 内存。

代价说清楚。

数据库只支持 PostgreSQL 一种，没有 MySQL 和 SQLite 选项，机器上得单独跑一个 PG。

默认抓取间隔是 1 小时，想更快得自己用 cron 调度，官方没给分钟级抓取。

界面只有六套主题和一套紧凑布局，想要卡片式、杂志式排版的人会觉得太素。

它没有移动端原生 App，手机上用浏览器打开，或者用第三方客户端接它的 API。

谁适合用：订了几十个博客和资讯源、要每天扫一遍的；做内容选题需要稳定输入源的；受不了推荐算法和追踪脚本的。

谁别碰：习惯在信息流里刷推荐、需要图片墙和视频内嵌播放的，Miniflux 的克制会劝退你。

官网 miniflux.app 有在线 demo，源码在 github.com/miniflux/v2，安装文档覆盖 Docker、Debian 包和二进制三条路。

---

### 📖 完整介绍与官方入口

完整文章保留官方资料来源、适用场景及版本和费用条件，下载方式以文章中的实际入口为准。

👉 **[点击前往 AronShare 官网阅读全文](https://aronshare.com/posts/miniflux-rss-reader/)**
