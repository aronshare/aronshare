# Plane 让项目排期回到自己服务器上

> 💡 **资源说明**：本文档为精选摘要镜像，完整工具介绍、官方入口与使用条件请前往 AronShare 官网浏览。

[![封面图片](https://aronshare.com/covers/cover_plane-project-tracking.webp)](https://aronshare.com/posts/plane-project-tracking/)

BODY

小团队的项目管理，往往死在一个不上不下的选择上。
用在线工具，数据在别人服务器，成员离职带走一份导出文件就够麻烦；自己搭一套，又嫌配置和维护太费人。

Plane 走的是自托管这条路。
它是开源的项目管理平台，代码在 GitHub 上公开，用 AGPL-3.0 许可，官方同时提供云版和本地部署两套方式。

![Plane 工作项看板，按 Backlog、Todo、进行中分列](https://aronshare.com/assets/post-images/plane-project-tracking/detail-1.webp)

*官方仓库截图，卡片上带编号、状态、日期和负责人头像。*

功能是按真实项目流程长出来的。
工作项支持富文本编辑和文件上传，还能加子属性和关联其他事项；周期用来固定一段时间的目标，配燃尽图看剩余工作量；模块把大项目切成能独立推进的块；视图把常用筛选存下来，谁都能一键回到自己关心的那批任务。

![Plane 甘特视图与看板叠在一起，能看到任务的时间跨度](https://aronshare.com/assets/post-images/plane-project-tracking/detail-2.webp)

*官方仓库截图，上方是时间线，下方是按状态分列的卡片。*

部署文档写得比较细。
Docker Compose 适合一台机器起步，Kubernetes 给到需要横向扩展的团队，官方还提供了实例管理入口，用来改全局配置、管成员和集成。
云版省掉运维，自托管省掉数据出内网的顾虑，两边之间没有功能墙，切换的代价在迁移数据。

实际用起来，最省时间的是视图和周期这两件事。
每周站会前把周期里的剩余项拉出来，谁卡住了一眼能看到；视图把「我负责的、这周到期、还没开始」存成一条，不用每次重新点筛选。
价格上自托管版本免费，服务器成本按你们自己的机器算，云版按人头订阅。

---

### 📖 完整介绍与官方入口

完整文章保留官方资料来源、适用场景及版本和费用条件，下载方式以文章中的实际入口为准。

👉 **[点击前往 AronShare 官网阅读全文](https://aronshare.com/posts/plane-project-tracking/)**
