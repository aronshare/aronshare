# Bruno 让接口请求跟着项目一起保存在 Git 里

> 💡 **资源说明**：本文档为精选摘要镜像，完整高清配置教程、最新版本与网盘高速下载通道请前往 AronShare 官网浏览。

[![封面图片](https://aronshare.com/covers/cover_bruno-api-client.webp)](https://aronshare.com/posts/bruno-api-client/)

# Bruno 让接口请求跟着项目一起保存在 Git 里

[网站全文](https://aronshare.com/posts/bruno-api-client/)

![Bruno 让接口请求跟着项目一起保存在 Git 里](https://aronshare.com/covers/bruno-api-client.webp)


后端接口改了，代码已经提交，调试时用的请求却还留在某位同事的个人工作区里。
其他人拿到项目，还要询问请求地址、认证方式和测试参数；过一段时间，团队又很难确定哪个请求集合对应哪个版本。
Bruno 提供了一种适合开发团队的整理方式：把接口请求保存为本地文件，用 Git 管理这些文件，让请求定义和项目变更一起被查看、讨论和保留。

它是面向 API 探索与测试的桌面客户端，提供 Windows、macOS 和 Linux 安装包。
开源版可以免费使用，项目仓库采用 MIT 许可，另外还有付费版本供有进阶需求的个人和团队选择[1]。

## 请求集合就是可以保存和比较的项目文件

Bruno 的集合保存在本地文件夹里，官方仓库介绍使用纯文本 Bru 格式记录请求信息，当前文档也介绍了 OpenCollection YAML 格式。
文件可以交给 Git 或其他版本控制工具管理，因此你能够把请求变更放进代码评审，也能在查阅旧版本时找到对应的接口调用方式[1][2]。

这种设计比较适合已经围绕仓库协作的团队。
例如，开发者增加了一个查询参数，可以同时修改服务代码和相关请求文件；评审者能够看到参数的变化，而不用额外索取一份导出的工作区。
团队仍需要约定文件目录、命名和提交规则，请求文件才会持续保持可用。

![Bruno 官方界面展示 GitHub REST API 请求集合、查询参数和 JSON 响应](https://aronshare.com/assets/post-images/bruno-api-client.png)

*图片来自 Bruno 官方仓库，展示 GitHub REST API 的演示请求；截图中的界面版本为 v3.0.1。*

本地保存也意味着同步方式由你选择。
Bruno 官方仓库明确说明不提供云端集合同步；团队可以利用已有的 Git 服务共享请求[1]。
发送请求时，客户端仍要连接实际的 API 地址，远程接口需要相应的网络和访问权限。
如果测试目标运行在本机，也可以在本机服务可用的情况下进行调试。


---

### 📥 资源高速获取与完整教程

本项目已通过官方原版校验并同步收录至 **AronShare 资源库**，提供绿色免安装便携版、夸克网盘转存以及详细配置 SOP。

👉 **[点击前往 AronShare 官网获取完整网盘下载与实操指南](https://aronshare.com/posts/bruno-api-client/)**
