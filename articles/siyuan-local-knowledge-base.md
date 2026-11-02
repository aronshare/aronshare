# 思源笔记 让你把个人资料留在自己电脑里并按段落自由关联

[网站全文](https://aronshare.com/posts/siyuan-local-knowledge-base/)

![Aron 封面](https://aronshare.com/covers/cover_siyuan-local-knowledge-base.webp)


## 思源笔记 是什么

把工作SOP、客户资料和项目复盘全部写在纯云端笔记里，一旦遇到网络断连、平台调整收费策略或者账号风控，导出迁移往往是一场灾难；而直接用纯 Markdown 文件夹管理，当文档超过几百篇时又缺少跨段落引用和结构化数据库查询能力。

思源笔记是一款主打「隐私优先、数据完全保存在本地设备」的开源个人知识库软件。它把所见即所得的排版体验、精确到单个段落的「块级双向链接」以及本地 JSON/Markdown 开放存储结合在一起，断网状态下依然可以使用全部核心编辑与检索功能。

![思源笔记桌面端多文档分屏编辑、双向链接与关系图谱界面](https://aronshare.com/assets/post-images/siyuan-local-knowledge-base-detail-1.webp)

## 它可以解决哪些日常痛点

- **精确到段落的块级引用与双向链接**：不仅能链接整篇文档，还可以直接引用或嵌入任意一个标题、段落、表格甚至代码块；在一处修改原块内容，所有嵌入引用的地方都会同步更新。
- **融合大纲、卡片复习与多视图数据库**：同一个工作空间里既能像写普通文档一样排版（内置数学公式、Mermaid 流程图、甘特图），也能创建类似 Notion 的多视图属性表格，或把重点块标记为间隔重复闪卡定期复习。
- **百万字级全文检索与 SQL 高级聚合**：底层把内容块建立本地索引，支持按关键字、标签、属性快速过滤，进阶用户甚至可以直接写一行 SQL 语句把散落在不同日记里的待办事项动态汇总成一张报表。
- **全平台离线可用并支持 S3 / WebDAV / Docker 自托管**：客户端覆盖 Windows、macOS、Linux、iOS 与 Android，多设备同步除了可选官方端到端加密云服务外，也完全支持自己配置第三方 S3 对象存储、WebDAV 或用 Docker 在服务器上自建。

![思源笔记块级内容大纲、数学公式与多主题展示](https://aronshare.com/assets/post-images/siyuan-local-knowledge-base-detail-2.webp)

## 安装与部署建议

1. **桌面与移动端**：可直接前往官网下载页、GitHub Releases 或各大应用商店安装；本地编辑、块级双链、PDF 标注、闪卡以及自行配置 S3 / WebDAV 同步均免费开放。
2. **服务器 Docker 自托管**：如果习惯在任何电脑打开浏览器直接记笔记，可用官方镜像一键部署：
   `docker run -d -v /siyuan/workspace:/siyuan/workspace -p 6806:6806 -u $(id -u):$(id -g) b3log/siyuan --workspace=/siyuan/workspace/ --accessAuthCode=你的访问密码`
3. 注意务必设置 `--accessAuthCode` 强密码，不要将未设防的 6806 端口直接暴露在公网；多设备同时开启第三方 WebDAV/S3 同步时，建议养成一端写完同步后再开另一端的习惯，减少并发冲突。

## 核实来源

- 官方网站：https://b3log.org/siyuan/
- 官方下载页：https://b3log.org/siyuan/download.html
- GitHub 仓库：https://github.com/siyuan-note/siyuan
