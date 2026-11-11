# Grist 让表格里的列写 Python，数据存一个 SQLite 文件

> 💡 **资源说明**：本文档为精选摘要镜像，完整工具介绍、官方入口与使用条件请前往 AronShare 官网浏览。

[![封面图片](https://aronshare.com/covers/cover_grist-spreadsheet-db.webp)](https://aronshare.com/posts/grist-spreadsheet-db/)

用表格管业务，撑到一定规模就会崩。

同一份客户名单，销售那边改了公司名，财务的表里还是旧的；想算一个跨表的汇总，得靠 VLOOKUP 和一串手工操作，谁改错一格没人知道。

Grist 把表格和数据库缝在一起。它是开源的「现代关系型电子表格」，grist-core 按 Apache-2.0 发布，一套 docker run 就能跑起自己的服务。

它跟普通表格最大的差别在列上。

一列可以写 Python 公式，完整 Python 语法和标准库都能用，另外还给了一大批 Excel 函数。也就是说，做数据清洗、拼字符串、按条件算值这些事，不用导出到脚本里再倒回来。

一个文档就是一个 SQLite 文件，自包含，任何能读 SQLite 的工具都能直接读出里面的数值和文本。备份就是复制一个文件，迁移就是把它搬到另一台机器。

表格、卡片、图表三种视图可以摆在一起。

![](https://aronshare.com/assets/post-images/grist-spreadsheet-db/detail-1.webp)

上图是一个联系人管理文档：左边是页面列表和几个工具入口，中间 CONTACTS 表，右边上半是选中那行的完整卡片，下半是关联的 INTERACTIONS 记录表。

选一行，右侧立刻显示这行的全部字段和关联记录，这种主从视图在普通表格里要自己拼半天。

仪表盘是拖出来的。

![](https://aronshare.com/assets/post-images/grist-spreadsheet-db/detail-2.webp)

这张是信用卡流水的月度分类页：左边一列月份，点中哪个月，右边饼图和汇总表就跟着变，图的占比和下面的金额是同一份数据的两种看法。

widget 之间能联动，用一个表当筛选器去控制另一张图和一张表，做业务看板不用再开一个 BI 工具。

代价说清楚，这部分比功能重要。

它是 open-core 模式，完整版有一批功能不在 grist-core 里，比如 GristConnect、Azure 文档存储、审计日志。

默认的 gristlabs/grist 镜像里混了非自由许可的扩展，只有把后台版本切到 Full Grist 时才激活；想完全用开源版本，要换 gristlabs/grist-oss 镜像。写「开源」两个字之前，这一条得先搞明白。

AI 公式助手依赖外部模型服务，OpenAI、Llama、OpenRouter 或任意兼容端点都行，自托管之后数据仍在你的网外跑。

Python 公式默认跑在服务进程里，官方给了 gVisor、macSandboxExec、Deno 加 Pyodide 几种沙箱方案，但都要自己配。多人协作的环境里，这一层必须处理。

完整版对小机构免费，条件是年资金低于 100 万美元，超过就要谈商业授权。

谁适合用：用表格管客户、库存、项目，已经被多表关联折磨过的；团队里有人会写 Python 的；想要数据落在自己机器上的。

谁别碰：只是记记账、做做简单汇总的，Excel 和飞书表格够用，自建服务只会多一份运维。

官网 getgrist.com，源码在 github.com/gristlabs/grist-core，自托管文档在 support.getgrist.com；截图是官方示例文档的数据，非真实客户记录。

---

### 📖 完整介绍与官方入口

完整文章保留官方资料来源、适用场景及版本和费用条件，下载方式以文章中的实际入口为准。

👉 **[点击前往 AronShare 官网阅读全文](https://aronshare.com/posts/grist-spreadsheet-db/)**
