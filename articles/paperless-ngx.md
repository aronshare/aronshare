# Paperless-ngx 让扫描的票据和合同也能按内容搜索

收录日期：2026-10-30

[在 AronShare 阅读](https://aronshare.com/posts/paperless-ngx/)

![Paperless-ngx 让扫描的票据和合同也能按内容搜索](https://aronshare.com/covers/cover_paperless-ngx.webp)


家电需要维修时，购买凭证可能在邮箱里，保修单是手机照片，合同又放在另一个文件夹。
如果文件名只有日期和扫描编号，找一张票据就得逐个打开。
[Paperless-ngx](https://github.com/paperless-ngx/paperless-ngx)是一款开源文档管理工具，能把这类资料整理成可搜索的档案库。

## 扫描件可以按正文内容查找

根据[官方功能说明](https://raw.githubusercontent.com/paperless-ngx/paperless-ngx/main/docs/index.md)，Paperless-ngx 使用 Tesseract 做 OCR，让原本只有图像的扫描件拥有可选择、可检索的文字。
系统保留原始文件，也能生成适合长期归档的 PDF/A 副本。
找到文件时，你可以查看预览，下载需要的版本，避免只有搜索结果却找不到原件。

全文搜索可以结合标签、往来单位、文档类型等条件使用。
例如，把商家设为往来单位，将购买凭证归为票据，再用型号或正文关键词缩小范围。
这类整理方式适合持续积累的合同、账单和家庭资料，文件夹名称不必承担所有分类任务。

![Paperless-ngx 官方文档卡片界面展示标签与筛选条件](https://aronshare.com/assets/post-images/paperless-ngx-official-ui.png)

*图片来自 Paperless-ngx 官方文档仓库，展示文档卡片与筛选界面。*

## 文件可以从网页和指定目录进入

[使用文档](https://raw.githubusercontent.com/paperless-ngx/paperless-ngx/main/docs/usage.md)介绍了网页拖放上传、消费目录和邮件规则等导入方式。
消费目录可以理解成待处理入口，文件被识别和归档后，会移入 Paperless-ngx 自己管理的存储结构，从入口目录移除。
因此，这个目录适合接收新扫描件，长期备份应另行安排。

经常收到电子票据的人，可以配置邮箱和匹配规则，让符合条件的附件进入档案库。
邮件规则还能移动邮件、标记已读或删除邮件，启用时要逐项确认动作。
如果只是整理少量家庭资料，网页上传更方便检查，没必要一开始就接入整个邮箱。

## 分类规则要服务于实际查找

同一份文件可以拥有多个标签，往来单位用于记录关联的人或机构，文档类型用于区分合同、发票等材料。
这些字段的含义见[官方使用说明](https://raw.githubusercontent.com/paperless-ngx/paperless-ngx/main/docs/usage.md)。
可以围绕“我要找哪家公司的哪类文件”设计分类，避免建立大量含义相近的标签。

OCR 提供搜索线索，金额、日期和编号等关键内容仍适合对照原图检查。
使用建议是拿一批清晰、模糊和倾斜程度不同的扫描件试用，观察自己的资料是否容易检索。
遇到难以识别的页面，补充准确的标题和标签，也能改善后续查找。

## Docker 部署需要同时考虑存储和维护

[官方安装文档](https://raw.githubusercontent.com/paperless-ngx/paperless-ngx/main/docs/setup.md)提供交互式安装脚本与 Docker Compose 模板，要求准备 Docker 和 Docker Compose。
手动部署可以按数据库方案选择模板，并一起配置环境变量、数据目录和访问地址。
需要处理 Office 等额外文件格式时，应查看带 Tika 的配置方案，别把可选组件当成默认能力。

软件按 GPL-3.0 许可开放源码，使用自托管方案需要自己承担设备、磁盘、备份和维护成本，许可信息可在[官方仓库](https://github.com/paperless-ngx/paperless-ngx)查看。
[功能说明](https://raw.githubusercontent.com/paperless-ngx/paperless-ngx/main/docs/index.md)明确文档以普通文件保存在磁盘上，因此服务器账号、磁盘访问和备份位置都需要妥善管理。

## 从一类常用资料建立档案习惯

可以用家电凭证或租房资料作为第一批内容，为每份文件确认标题、日期和类型。
尝试用正文关键词找回文件，也检查原件下载与备份恢复是否符合需要。
这几个环节形成习惯后，扩展到更多资料会更容易，档案库也能保持清楚的结构。

- [访问官方文档](https://docs.paperless-ngx.com/)
- [查看源码与许可](https://github.com/paperless-ngx/paperless-ngx)
- [阅读官方安装说明源码](https://raw.githubusercontent.com/paperless-ngx/paperless-ngx/main/docs/setup.md)
