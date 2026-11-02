# Homepage 让你在一个页面里找到自建服务并查看运行状态

> 💡 **资源说明**：本文档为精选摘要镜像，完整高清配置教程、最新版本与网盘高速下载通道请前往 AronShare 官网浏览。

[![封面图片](https://aronshare.com/covers/cover_homepage-service-dashboard.webp)](https://aronshare.com/posts/homepage-service-dashboard/)

# Homepage 让你在一个页面里找到自建服务并查看运行状态

收录日期：2026-10-30

[在 AronShare 阅读](https://aronshare.com/posts/homepage-service-dashboard/)

![Homepage 让你在一个页面里找到自建服务并查看运行状态](https://aronshare.com/covers/cover_homepage-service-dashboard.webp)


给家里搭了网盘、影音库和监控工具后，浏览器书签里往往多出一串域名与端口。
想找某个应用时，需要回忆它的地址；想知道容器是否运行，又得打开另一套管理页面。
Homepage 适合处理这类入口分散的问题，它能把自建服务整理成分组卡片，并通过小组件显示相关数据，功能介绍见[官方仓库](https://github.com/gethomepage/homepage)。

## 从常用服务入口开始整理

Homepage 使用 YAML 文件配置服务。
根据[服务配置文档](https://gethomepage.dev/configs/services/)，可以在 `services.yaml` 中建立分组，为服务填写访问地址、图标和说明，也能继续嵌套分组。

例如，把网盘与笔记工具放进“资料”，把服务器和监控工具放进“维护”，家人使用的影音应用单独成组。
这样的分类按使用目的展开，打开页面就能判断该去哪里。
只需要链接导航时，填写服务地址即可；希望显示应用中的数据，则需要继续配置相应小组件。

![Homepage 官方展示的服务卡片与系统状态面板](https://aronshare.com/assets/post-images/homepage-service-dashboard-official-ui.png)

*图片来自 Homepage 官方仓库，展示配有背景图和展示边框的真实界面示例，卡片数据为官方示例内容。*


---

### 📥 资源高速获取与完整教程

本项目已通过官方原版校验并同步收录至 **AronShare 资源库**，提供绿色免安装便携版、夸克网盘转存以及详细配置 SOP。

👉 **[点击前往 AronShare 官网获取完整网盘下载与实操指南](https://aronshare.com/posts/homepage-service-dashboard/)**
