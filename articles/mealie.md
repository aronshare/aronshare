# Mealie 帮你把收藏的菜谱用进每周菜单和购物清单

收录日期：2026-10-30

[在 AronShare 阅读](https://aronshare.com/posts/mealie/)

![Mealie 帮你把收藏的菜谱用进每周菜单和购物清单](https://aronshare.com/covers/cover_mealie.webp)


收藏夹里放着许多菜谱，到了买菜的时候，还是要重新想今天吃什么、家里缺什么。
菜谱、菜单和采购清单之间少了一步整理，收藏的内容就很难真正用起来。
[Mealie](https://mealie.io/)把这几件事连在一起，可以保存菜谱、安排每周餐食，并把食材加入购物清单。

## 网页里的菜谱可以整理成统一格式

Mealie 支持从受支持的网站链接导入菜谱，也提供手动编辑入口。
[功能文档](https://mealie.io/documentation/getting-started/features/)分别介绍了网址抓取与手动创建，选择入口时可以看手头是网页链接还是已有的文字做法。
家里口头传下来的做法可以直接录入，不必为它额外制作一个网页。

整理时可以保留食材、步骤和备注，并用分类、标签或所需厨具帮助查找。
例如，将常做的菜按主食、配菜分类，用“适合冷冻”这样的标签标出使用特点。
Cookbooks 可以按照筛选条件集中展示一组菜谱，适合建立经常翻看的常用菜单。

![Mealie 官方菜谱详情页展示菜品照片、食材和步骤](https://aronshare.com/assets/post-images/mealie-official-ui.webp)

*图片来自 Mealie 官网，展示 Chicken Parmesan 菜谱的详情界面。*

## 每周菜单可以直接关联菜谱

[官方说明](https://mealie.io/documentation/getting-started/features/)中的餐食计划采用日历视图，可以手动添加菜谱，也能使用随机选择功能。
外食、吃剩菜等没有对应菜谱的安排，可以用备注记录。
这样做的好处是，日历能反映真实的一周安排，不需要每天都填一份正式食谱。

[官网](https://mealie.io/)还介绍了购物清单，既能手动添加物品，也能把菜谱的食材加入清单，用标签帮助整理。
买菜前可以对照家里现有的东西删减条目，把厨房纸等非食材用品一起补上。
菜谱中的原料用词和家里习惯可能不同，常用菜值得统一一下名称，采购时更容易看懂。

## 家庭共享可以保留各自的安排

Mealie 的群组和家庭有不同作用：群组内可以共享菜谱，各家庭保留独立的餐食计划与购物清单。
[官网功能概览](https://mealie.io/)也列出了邀请用户、管理账号和 REST API 等入口。
对于共享一套菜谱、但分开做饭的家庭成员，这种结构能减少重复录入。

实际使用时，可以从共同常做的几道菜开始，让负责做饭和买菜的人都找到相同版本。
如果只是自己保存菜谱，保持简单的分类和一个购物清单即可，不必用上所有协作功能。

## 导入范围和部署条件需要看清楚

普通网址导入依赖项目支持的菜谱抓取器，适用范围可在[官方功能文档](https://mealie.io/documentation/getting-started/features/)查看。
碰到无法提取的页面，可以用编辑器补录食材和步骤。
导入后也适合检查份数、单位和说明，尤其是原文存在多个做法时，确认保留的是自己要做的版本。

[安装清单](https://mealie.io/documentation/getting-started/installation/installation-checklist/)推荐 Docker 部署，并提供 SQLite 和 PostgreSQL 两种方案。
普通家庭可以从 SQLite 方案入手；多人并发使用或需要模糊搜索时，可以评估 PostgreSQL。
官方镜像支持 amd64 与 arm64，32 位 ARM 系统不在支持范围内，旧设备需要核对系统架构。

## 免费源码也需要维护自己的数据

Mealie 的[官方仓库](https://github.com/mealie-recipes/mealie)采用 AGPL-3.0 许可，自托管仍需承担设备、存储与维护费用。
部署时需要设置服务地址等参数，需要邮件邀请或密码重置时还要配置 SMTP，具体项目见[安装文档](https://mealie.io/documentation/getting-started/installation/installation-checklist/)。
文档提供完整站点备份机制，并要求把备份保存到部署服务器以外的位置。

可以挑一个工作周，用常做的菜排菜单，并带着生成的清单完成一次采购。
如果菜谱容易找到，清单也符合自己的买菜习惯，就值得逐渐整理更多收藏；菜谱库的规模可以跟着实际做饭频率增长。

- [访问 Mealie 官网与演示入口](https://mealie.io/)
- [查看源码与许可](https://github.com/mealie-recipes/mealie)
- [阅读 Docker 安装清单](https://mealie.io/documentation/getting-started/installation/installation-checklist/)
