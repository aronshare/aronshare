# Glance 让你把所有想看的资讯拼成早上打开就看完的一页

> 💡 **资源说明**：本文档为精选摘要镜像，完整工具介绍、官方入口与使用条件请前往 AronShare 官网浏览。

[![封面图片](https://aronshare.com/covers/cover_glance-selfhosted-dashboard.webp)](https://aronshare.com/posts/glance-selfhosted-dashboard/)

早上开工的第一件事，往往是十几个标签页各开一遍。
邮箱看一眼，行业资讯扫一遍，服务器状态再确认一遍，半小时就过去了。
Glance 把这几件事收进一个自己搭的面板里，打开一页就能看完。

它是开源自托管的信息面板，最新版本为 v0.8.8，2026 年 11 月 7 日发布[1]。
单个可执行文件不到 20MB，官方也提供同样小巧的 Docker 镜像[1]。

## 一个 YAML 文件决定页面长什么样

配置写在 YAML 里，pages 下面可以挂多个页面，每个页面按列排布，列里放 widget[2]。
常用的是 RSS、Reddit、Hacker News、YouTube 频道更新、Twitch、天气、行情、Docker 容器状态和服务器状态[1]。
官方文档还给了现成的配置模板，改成自己要看的源就能跑起来[2]。

![Glance 桌面端三栏面板，显示日历、RSS、Hacker News、天气和行情](https://aronshare.com/assets/post-images/glance-selfhosted-dashboard/detail-1.webp)

*图片来自 Glance 官方文档截图，展示三栏布局下的各类 widget。*

widget 的写法很直白，一个 type 加几个参数就是一块内容。
比如 rss 里填 feed 地址和条数，releases 里填仓库名，就能盯着几个项目的版本更新。
同一列里可以塞多个 widget，也可以把几个 widget 归到一个 group 里并排显示。


---

### 📖 完整介绍与官方入口

完整文章保留官方资料来源、适用场景及版本和费用条件，下载方式以文章中的实际入口为准。

👉 **[点击前往 AronShare 官网阅读全文](https://aronshare.com/posts/glance-selfhosted-dashboard/)**
