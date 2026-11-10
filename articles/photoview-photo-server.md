# Photoview 让你按硬盘目录直接浏览上万张照片

> 💡 **资源说明**：本文档为精选摘要镜像，完整工具介绍、官方入口与使用条件请前往 AronShare 官网浏览。

[![封面图片](https://aronshare.com/covers/cover_photoview-photo-server.webp)](https://aronshare.com/posts/photoview-photo-server/)

硬盘里按年份、按拍摄地点分了上百个文件夹，找一张照片还得靠文件名猜。
Photoview 做的就是把服务器上的目录直接变成相册，浏览器打开就能按时间线翻。

它是开源的相册服务器，代码在 GitHub 上公开，用 AGPL-3.0 授权。
和那种把照片导入自家库的设计不同，它跟文件系统绑得很紧：网站展示的就是服务器目录里的文件，文件夹对应相册，移动或者重命名目录，网站上的结构跟着变。

面向摄影师的功能是它的重点。
RAW 格式能解析，EXIF 信息会读出来，右侧详情面板能看到机身、镜头、光圈、快门、ISO 和拍摄时间。
视频也支持，常见的格式能用，播放前会针对网页做优化。

![Photoview 时间线界面，左侧导航，中间按日期分组，右侧是照片详情](https://aronshare.com/assets/post-images/photoview-photo-server/detail-1.webp)

*官方仓库截图，右侧面板显示 EXIF 与各尺寸下载选项。*

多用户按目录隔离。
每个账号绑定一个本地路径，只能看到自己路径下的照片，家里几个人各放各的库，互不打扰。

分享做得很直接。
相册或者单张照片可以生成公开链接，链接能加密码，发给朋友看某次旅行的照片不用开账号。

![Photoview 初始设置页，填用户名、密码和照片目录路径](https://aronshare.com/assets/post-images/photoview-photo-server/detail-2.webp)

*首次启动的设置页，Photo Path 填服务器上的照片目录。*

人脸识别和缩略图是自动跑的。
扫描时生成缩略图，照片滚动到可见位置才加载，全屏时先显示缩略图，原图下载完再替换，几千张的库翻起来不会卡死。

安全上官方提到几件事：媒体资源走 cookie token 校验，密码做哈希存储，接口用严格的跨域策略。

部署用 Docker Compose 最省事，官方给了示例文件，数据库可以选内置的 SQLite、MariaDB 或者 PostgreSQL。
官方仓库提醒了一件事，PostgreSQL 升到 18 之后容器里的数据目录挂载点变了，照着示例文件改 compose 配置，升级前先备份数据库。

资源占用取决于库的规模。
只是自己几百 GB 的照片，一台小主机加一块硬盘就够；几万张原图要开人脸识别和缩略图，扫描那阵子 CPU 会跑满，安排在夜里更合适。

---

### 📖 完整介绍与官方入口

完整文章保留官方资料来源、适用场景及版本和费用条件，下载方式以文章中的实际入口为准。

👉 **[点击前往 AronShare 官网阅读全文](https://aronshare.com/posts/photoview-photo-server/)**
