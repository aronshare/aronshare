# wallabag 帮你保存文章正文并在有空时继续阅读

[网站全文](https://aronshare.com/posts/wallabag-read-it-later/)

![wallabag 官方界面](https://aronshare.com/covers/cover_wallabag-read-it-later.webp)


遇到值得细读的长文时，手头往往还在处理别的事。
把它留在浏览器标签页里，过几天可能已经淹没在一排网页中；只存一个链接，也会把下次阅读时的弹窗和页面干扰一起留下。
wallabag 可以保存文章正文，把这些待读内容集中成一份阅读清单。

## 把网页文章收进自己的阅读列表

[wallabag](https://github.com/wallabag/wallabag) 是一款开源稍后阅读应用，会从网页中提取内容，提供更专注的阅读界面。
它适合保存长文、教程和访谈，让你有空时回到正文继续读。
官方提供浏览器扩展 wallabagger，以及 Android 和 iOS 应用入口；资料也能通过网页端查看。

实际使用可以围绕自己的阅读主题整理，比如“写作”“设计”或某个正在学习的技术。
标签用于区分主题，收藏标记保留值得反复查看的文章，读过的内容则放入归档。
未读清单负责提醒近期要读什么，归档负责保存以后可能用到的材料，两者分开更容易安排阅读时间。

![wallabag 官方截图中的未读文章卡片、标签和归档入口](https://aronshare.com/assets/post-images/wallabag-read-it-later-ui.png)

*图片来自 wallabag 官方仓库，展示未读列表和文章卡片。*

## 阅读时可以把想法留在段落旁

看到值得记住的论点，可以选中相关文字添加批注。
[官方批注文档](https://doc.wallabag.org/user/articles/annotations/)说明，保存批注后文字会高亮，鼠标移到相应位置可以查看说明。
这些批注显示在 wallabag 内的文章里，原网站仍保留自己的页面内容。

如果正在读一篇技术教程，可以在关键段落写下使用条件；阅读访谈时，也可以记下与自己工作有关的想法。
以后回看文章，批注能够帮你找到当时关注的位置。
对于只想安心读完文章的人，标签和阅读状态已经能承担基本整理任务，无需给每篇内容都加上复杂分类。

## 用移动应用或导出文件继续阅读

[官方托管服务介绍](https://wallabag.it/en/)列出了网页、手机和平板等阅读方式，也提供离线阅读与导出功能。
需要离线使用时，应在联网状态下完成相应应用的内容同步，确保要读的文章已经保存到设备。

[导出文档](https://doc.wallabag.org/user/articles/download/)介绍了单篇文章和整类文章的下载方式，包含 EPUB、PDF 等格式。
例如想把几篇长文放到电子阅读器上，可以根据设备支持的格式导出阅读文件。
整理资料时，也可以把文章导出留存；阅读器能接收什么格式、怎样传输文件，需要结合具体设备确认。

wallabag 主要围绕文章正文组织阅读体验。
保存一篇带有大量交互图表、视频或复杂排版的网页后，可以检查正文和关键图片是否齐全，需要查看交互内容时保留原网页入口。

## 选择托管服务或自己部署

想直接开始阅读，可以注册官方提供的 wallabag.it 托管服务，由服务方维护运行环境。
它采用付费订阅，并提供试用入口；套餐价格和试用条件以[官方服务页面](https://wallabag.it/en/)为准。

愿意自己管理服务器的人，可以部署开源版本。
项目采用 MIT 许可，[官方环境要求](https://doc.wallabag.org/admin/installation/requirements/)列出了 PHP、Composer、所需扩展及数据库驱动，支持 MySQL、PostgreSQL 或 SQLite 对应的连接方式。
部署时还需要配置 Web 服务，并安排数据库与文章资料的备份。
软件本身开源，服务器、维护和备份空间的成本需要自行承担。

可以从几篇已经想读、却一直没有读完的文章开始。
用浏览器扩展保存，在常用设备上打开阅读，给重要段落留下批注，读完后归档。
当保存、阅读和回看都符合你的习惯，这份清单才会逐渐成为用得上的阅读资料库。

- [访问 wallabag 官网](https://wallabag.org/)
- [查看官方源码与应用入口](https://github.com/wallabag/wallabag)
- [查看自托管环境要求](https://doc.wallabag.org/admin/installation/requirements/)
- [了解 wallabag.it 托管服务](https://wallabag.it/en/)
