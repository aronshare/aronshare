# Formbricks 把站内问卷的编辑和结果分析放在一个后台

> 💡 **资源说明**：本文档为精选摘要镜像，完整工具介绍、官方入口与使用条件请前往 AronShare 官网浏览。

[![封面图片](https://aronshare.com/covers/cover_formbricks-surveys.webp)](https://aronshare.com/posts/formbricks-surveys/)

产品上线三个月，用户为什么不再续费，团队只能翻客服聊天记录去猜。
把问卷丢进用户群，回收率低得可怜，还分不清答卷对应哪个账号。
Formbricks 把问卷做进产品界面里，官方仓库直接把这套东西叫作开源的 Qualtrics 替代品。
它支持应用内弹窗、网站浮层、独立链接和邮件四种投放方式，用户旅程的每个节点都能问一句。
编辑器是无代码的，题目和选项在左侧卡片里堆，右边实时预览。
题目类型从单选多选、评分、NPS、矩阵、排序一路到文件上传，可以按用户群定向投放，不用改业务代码。
官方模板库里存着现成的问卷骨架，做 PMF 调研、流失回访、功能反馈都能拿一份来改。
团队成员可以一起编辑同一份问卷，回收结果都落在同一个工作区里。
![](https://aronshare.com/assets/post-images/formbricks-surveys/detail-1.webp)
截图一是编辑器界面，顶部一排 Questions、Styling、Language、Settings、Follow-ups 五个标签，左边 Block 1 和 Block 2 各挂一道题，右边是手机与桌面两种设备预览。
每张题目卡右上角有上移、复制、删除图标，下面挂 Conditional Logic 和区块设置，改完点 Publish 就上线。
回收之后进 Summary，展示量、开始数、完成数、流失率、平均完成时间五个指标排在顶上。
每道题一张卡片，多选题给横向条形图和百分比，评分题给堆叠分布和平均分。
![](https://aronshare.com/assets/post-images/formbricks-surveys/detail-2.webp)
第二张图就是这个页面，ACME Inc. 下的 Retail Banking 工作区，25 次展示、16 次完成、0 流失、平均 44.88 秒，下面第一道多选题 Everyday Checking 占到 93.75%，第二道评分题平均 3.50。
Responses 标签页能看单条原始回答，也能直接导出，再接 Zapier、n8n、Slack、Notion 这些工具。
部署走 Docker Compose，官方 baseline 里除了 Formbricks Web 还有 PostgreSQL、Redis/Valkey、Formbricks Hub、Cube，外加一个 SpiceDB 管权限数据。
机器上要有 Docker Compose V2、curl、openssl 和一个 POSIX shell，反向代理和 HTTPS 证书得自己配。
生产环境还要填 WEBAPP_URL、BETTER_AUTH_SECRET、ENCRYPTION_KEY、POSTGRES_PASSWORD 这几个变量。
许可证是 AGPLv3 加企业版双轨，核心功能免费、可以商用。
改了再分发就得把改动也按 AGPLv3 开源，并且注明改动日期，这是 AGPL 的硬约束，闭源二次开发绕不开。
apps/web/modules/ee 目录下的功能走企业许可，Docker 镜像里已经带上，没有 license key 打不开。
官方还写明不卖白标，也不允许把编辑器拆出来塞进自家产品。
价格上 Community Edition 永久免费，自托管不需要订阅。
Experience Suite 不公开价目，按每年回收的响应数、工作区数量和授权年限报价，坐席不限。
官方给了 15 天试用 license，能在自己已经跑起来的实例上直接解锁功能，不用迁移数据。
适合谁比较明确，产品团队要在应用内做 NPS、功能反馈、流失回访，又要求答卷留在自己库里的。
只发一次性外部问卷、完全用不到站内触发的，用免费表单工具省事得多。
团队里没人管服务器和证书，AGPL 的公开义务也没人愿意背，这套东西的维护开销会压过收益。
入口在 formbricks.com/docs/self-hosting/setup/docker，代码仓库在 github.com/formbricks/formbricks。
文中截图为官方文档演示数据，ACME Inc. 这个组织和那些百分比都是样例。

---

### 📖 完整介绍与官方入口

完整文章保留官方资料来源、适用场景及版本和费用条件，下载方式以文章中的实际入口为准。

👉 **[点击前往 AronShare 官网阅读全文](https://aronshare.com/posts/formbricks-surveys/)**
