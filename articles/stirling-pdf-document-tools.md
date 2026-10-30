# Stirling PDF 帮你在自己的电脑和服务器上处理 PDF 文件

收录日期：2026-10-30

[在 AronShare 阅读](https://aronshare.com/posts/stirling-pdf-document-tools/)

![Stirling PDF 帮你在自己的电脑和服务器上处理 PDF 文件](https://aronshare.com/covers/cover_stirling-pdf-document-tools.webp)


收到几份扫描材料，需要调整页序、合成一个 PDF，文件太大还要压缩，遇到图片文字又需要识别。
Stirling PDF 把这些日常文档操作做成了图形界面，并提供桌面客户端、浏览器界面和自托管服务器等入口。
涉及内部资料时，可以按自己的部署方式安排文件处理位置，减少临时寻找在线转换网站的次数。

## 一份文档可以完成哪些处理

[官方项目说明](https://github.com/Stirling-Tools/Stirling-PDF)列出了合并、拆分、编辑、压缩、格式转换、OCR、签名和内容遮盖等工具，也提供用于系统集成的 REST API。
整理培训资料时，可以合并不同来源的 PDF；只需其中几页时，可以拆分文件；纸质资料扫描后，可以使用 OCR 识别文字。
这些能力适合围绕一个明确任务组合使用，具体格式与参数仍需查看对应工具页面。

![Stirling 官方展示的 PDF 工作区和工具侧栏](https://aronshare.com/assets/post-images/stirling-pdf-document-tools-official-ui.png)

*图片来自 Stirling 官方仓库，展示文件入口、文档库与 PDF 工具侧栏。*

界面右侧按用途排列处理工具，中间区域负责添加文件。
同一个工作区能够覆盖多种日常操作，批量处理还可以通过工作流和 API 接入已有业务。
自动化涉及处理额度，部署时应把人工使用与程序调用分别核算。

## 自托管适合怎样的使用场景

个人可以从桌面端了解工具，团队也可以把服务器部署在自己维护的环境中，通过浏览器访问。
[官方 README](https://github.com/Stirling-Tools/Stirling-PDF)给出的快速体验方式是使用 Docker 启动服务，并将容器的 8080 端口映射到主机。
运行后打开本机对应端口，即可进入界面。

快速启动适合了解工具布局。
长期使用还需要按官方服务器文档配置持久化目录、登录、安全访问与备份，团队应明确谁能上传文件、谁维护实例，以及文件如何保存。
如果接入云端能力或其他服务，也要单独核对数据流向，不能把所有入口都理解成完全离线运行。

## 免费方案与团队方案有明确分界

[自托管方案说明](https://docs.stirlingpdf.com/Server/Licensing/Plans-and-Licences)列出 Free、Team 和 Enterprise 三档。
Free 默认支持 5 位用户；从 V1 升级且原有用户更多的服务器，文档说明会保留原有数量作为上限。
基础 PDF 工具、REST API、OAuth2／OIDC 登录及服务器证书签名列在 Free 能力范围内。

外部数据库、集群、S3 或数据库文件存储等能力列在 Team 及以上方案，SAML2、审计日志等列在 Enterprise。
Processor 自动化与 AI 工具有月度处理额度，Enterprise 另有安排；使用 API Key 的 PDF 调用也有计量规则，Team 许可存在相应例外。
因此，选型时需要同时查看人数、部署能力和处理额度，具体价格以官方定价页面为准。

## 许可也要按代码范围核对

仓库将项目称为开放核心模式。
[根目录 LICENSE](https://github.com/Stirling-Tools/Stirling-PDF/blob/main/LICENSE)说明，指定目录之外的代码适用 MIT，proprietary、saas、engine 及部分前端目录适用各自的许可文件。
准备二次开发、重新分发或集成到自己的产品时，应检查实际使用到的目录，不能用单一许可名称概括整个仓库。

## 用自己的文档判断是否合适

可以选一份允许用于测试的材料，分别检查拆分页码、压缩后的图像清晰度、OCR 文字和转换后的排版。
表格、签章、扫描噪点等细节值得单独核对，处理完成后保留原始文件便于比较。
个人使用重点看常用操作是否顺手，团队使用还要检查登录方式、人数限制和自动化成本。

- [访问 Stirling 官网](https://stirling.com)
- [查看源码与快速启动说明](https://github.com/Stirling-Tools/Stirling-PDF)
- [阅读自托管方案与许可说明](https://docs.stirlingpdf.com/Server/Licensing/Plans-and-Licences)
