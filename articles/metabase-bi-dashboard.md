# Metabase 让不会写 SQL 的同事自己查数据

> 💡 **资源说明**：本文档为精选摘要镜像，完整工具介绍、官方入口与使用条件请前往 AronShare 官网浏览。

[![封面图片](https://aronshare.com/covers/cover_metabase-bi-dashboard.webp)](https://aronshare.com/posts/metabase-bi-dashboard/)

运营想看上周的注册转化，市场想知道哪个渠道的客单价高，产品在追一个功能的使用率。
每个问题都提给数据同学，排期一周，等报表出来业务节奏已经过去了。

Metabase 的思路是把提问的权力交回业务手里。
它是开源的商业智能工具，代码以 AGPL 为主，企业目录下的功能走商业许可，官方同时提供云版和自托管两条路。

![查询构建器按产品类别和月份汇总订单数，右侧实时给出预览](https://aronshare.com/assets/post-images/metabase-bi-dashboard/detail-1.webp)

*官方文档截图，Summarize 区按 Category 与 Created At 分组，预览表直接给出每组的计数。*

用起来的路径分两种。
不懂 SQL 的人打开查询构建器，选表、点字段、加筛选、按维度汇总，下面实时出预览，表的每一行就是答案。
写 SQL 的人在原生编辑器里敲语句，结果一样能存成问题、挂到仪表盘上。

![带筛选条件的查询，第一步选表，第二步限定最近三个月](https://aronshare.com/assets/post-images/metabase-bi-dashboard/detail-2.webp)

*官方文档截图，Filter 区写的是 Created At is in the previous 3 months，底部一排按钮是筛选、汇总、关联、排序和可视化。*

图表类型不用自己想。
点 Visualize 之后在折线、柱状、饼图、地图、漏斗里挑一个，改配色和坐标轴都在侧边面板里，改坏了撤回一步就回去。

仪表盘是它落地最实的一块。
把几个问题拖到同一页，配上筛选器，销售、运营、老板看的是同一份数字。
定时订阅把仪表盘按天或者按周发到邮箱和 Slack，不用每天早上手动截图。

权限按数据源和集合分开配。
哪些人能看哪个库、能不能导出、能不能写 SQL，都能限制；对外分享可以生成公开链接，也可以嵌到自家后台里。

部署方式不复杂。
Docker 跑一个容器，配一个应用数据库存元数据，业务数据仍然留在原来的 MySQL、PostgreSQL、ClickHouse 里，它只读不写。
JAR 包直接跑在已有 Java 环境里也行，适合不想多开容器的小团队。

AI 那块已经接进来了。
Metabot 支持用自然语言提问生成查询，官方文档里也标了用量限制，这套功能适合当辅助，复杂口径还是得有人对过数。

---

### 📖 完整介绍与官方入口

完整文章保留官方资料来源、适用场景及版本和费用条件，下载方式以文章中的实际入口为准。

👉 **[点击前往 AronShare 官网阅读全文](https://aronshare.com/posts/metabase-bi-dashboard/)**
