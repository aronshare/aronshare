# Ghost 把博客会员和邮件订阅装进一个开源后台

> 💡 **资源说明**：本文档为精选摘要镜像，完整工具介绍、官方入口与使用条件请前往 AronShare 官网浏览。

[![封面图片](https://aronshare.com/covers/cover_ghost-cms-selfhosted.webp)](https://aronshare.com/posts/ghost-cms-selfhosted/)

写公众号、写邮件订阅的人，早晚会卡在同一件事上：文章在一个地方，订阅名单在另一个地方，收钱又在第三个地方。

Ghost 把这三件事塞进一个后台。它是 MIT 许可的开源 Node.js 发布平台，文章、会员、付费订阅、邮件订阅都在同一套系统里。

打开后台看到的是数据面板。左边是文章、页面、标签、成员，中间是成员总数和付费成员的增长曲线，右侧浮出最近的文章列表。

![](https://aronshare.com/assets/post-images/ghost-cms-selfhosted/detail-1.webp)

图里这个 40,349 的成员数和那条付费成员曲线就是 Ghost 的主线。读者在文章页留邮箱成为免费成员，愿意付钱的走 Stripe 升级成付费会员。

会员这块是原生的。会员注册、付费订阅、邮件订阅都内置，Stripe 直连你自己的账户，Ghost 抽 0%，Stripe 自己的手续费照付。目前原生支持的支付渠道只有 Stripe 一个。

会员名单随时能导出，订阅和账单都留在自己的 Stripe 账户里，这批人不会因为换平台就带不走。

文章可以设成付费会员专享，免费成员只能看到公开部分，这是它区别于普通博客插件的地方。

再往下是集成。设置页把会员、增长、高级分成三组，内置集成和自定义集成分开列，自定义那条可以挂 webhook 或者对接自己的服务。

![](https://aronshare.com/assets/post-images/ghost-cms-selfhosted/detail-2.webp)

装法不复杂。npm install ghost-cli -g 装完 CLI，服务器上跑 ghost install 会连 Let's Encrypt 的 SSL 一起配好，本地试用跑 ghost install local 就能起来。

官方推荐的自托管底子是 Ubuntu 22.04 到 26.04 的 LTS，Node.js 22 或 24 的 LTS，数据库 MySQL 8.0 或 8.4，前面再放一层 NGINX。

自托管要自己扛什么，官方文档写得很清楚。产品功能和官方托管完全一样，差别在每周更新、SSL 续期、备份、24 小时值守这些活都落到自己头上，邮件发送的成本也得自己付。

两条路要算清楚。图省事就用 Ghost(Pro)，年付 18 美元一个月起，带 1,000 个成员额度，升级、备份、CDN 都不用管。想省钱或者数据必须落在自己机器上，就自托管，一台 VPS 加 MySQL 起步。

谁适合：做会员制内容的独立写作者、想把订阅名单握在自己手里的团队、需要 headless CMS 给前端供内容的开发者。

谁别碰：一个月写不了几篇、也不想碰服务器和邮件配置的人，用现成博客平台更省事；需要复杂电商或多站点统一管理的，Ghost 不覆盖这些。

官网 ghost.org，源码在 github.com/TryGhost/Ghost，安装文档 docs.ghost.org。截图里的成员数和文章都是官方文档的演示数据。

---

### 📖 完整介绍与官方入口

完整文章保留官方资料来源、适用场景及版本和费用条件，下载方式以文章中的实际入口为准。

👉 **[点击前往 AronShare 官网阅读全文](https://aronshare.com/posts/ghost-cms-selfhosted/)**
