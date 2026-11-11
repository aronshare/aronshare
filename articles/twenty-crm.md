# Twenty 把 CRM 写成代码，字段和视图跟着业务改

> 💡 **资源说明**：本文档为精选摘要镜像，完整工具介绍、官方入口与使用条件请前往 AronShare 官网浏览。

[![封面图片](https://aronshare.com/covers/cover_twenty-crm.webp)](https://aronshare.com/posts/twenty-crm/)

买过 CRM 的人都有一个共同经历：销售流程一改，字段就得提工单。

标准版不给改，企业版报价谈三个月，业务部门只好自己用表格凑合，客户数据又散回 Excel。

Twenty 走的是另一条路。它是开源的 CRM，官方在 README 首屏直接写「第一大开源 CRM」，主体按 AGPLv3 发布，给技术团队提供的是可改的组件。

它的核心做法是把 CRM 的结构写成代码：对象、字段、视图都用 TypeScript 定义，定义完就跟着代码仓库一起走版本管理。

![](https://aronshare.com/assets/post-images/twenty-crm/detail-1.webp)

打开工作区是这样一个仪表盘：左边是收藏的公司列表，下面是 workspace 里的各个对象，中间四张 KPI 卡，两枚半环仪表看目标进度和赢单率，再往下是收入曲线和按阶段拆的管道柱状图。

这些卡片和图表都能自己加，dashboard 和 widget 都是配置出来的，字段更是。

改业务流程的流程变成这样：官方给了 Twenty CLI，一条 twenty app 初始化应用脚手架，改完对象定义，再 twenty app publish 推到工作区。

对技术团队的意义是，CRM 的改动进了 git，能 review、能回滚、能分环境。

它内建 AI agents 和对话，作为 CRM 数据之上的查询层；你问「这个季度哪几个单子快黄了」，它去读的是你自己的对象和字段。

邮件营销也能在同一个工作区里管。

![](https://aronshare.com/assets/post-images/twenty-crm/detail-2.webp)

上图是 Campaigns 列表，一行一个活动，状态分 Scheduled、Draft、Sent，右边能看到受众、发件地址和发送时间。

这类界面对做外贸和出海的人不陌生，问题是多数 CRM 把营销、客户、机会分成三个产品卖三份钱。

代价说清楚。

许可证是混合的：主体 AGPLv3，文件头标了 Enterprise 注释的部分走商业许可，CLI 和 SDK、UI 这些包是 MIT。商用前要看清你改的是哪一部分。

自托管要走 Docker Compose，后端是 NestJS 加 BullMQ，数据层要 PostgreSQL 和 Redis，一台小机器跑得动，但备份和升级得自己管。

云版按人头收费，Cloud Pro 每人每月 9 美元，Organization 每人每月 39 美元，都按年计费。人一多，账单涨得比自托管贵。

功能还在快速迭代，版本号到了 2.x，升级前建议先看 breaking change。

谁适合用：销售流程跟同行不一样、需要自己定义对象和字段的；团队里有开发能写 TypeScript 的；想把 CRM、邮件营销、任务放进一个工作区的。

谁别碰：销售流程就是标准的「线索—商机—成交」、团队里没人写代码的，用现成 SaaS 学起来更快。

官网 twenty.com，源码在 github.com/twentyhq/twenty，文档站 docs.twenty.com 有自托管和 CLI 的完整说明；截图里的公司与金额是官方演示数据。

---

### 📖 完整介绍与官方入口

完整文章保留官方资料来源、适用场景及版本和费用条件，下载方式以文章中的实际入口为准。

👉 **[点击前往 AronShare 官网阅读全文](https://aronshare.com/posts/twenty-crm/)**
