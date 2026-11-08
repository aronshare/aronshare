# 一款可以远程操作别人电脑的开源工具

> 💡 **资源说明**：本文档为精选摘要镜像，完整工具介绍、官方入口与使用条件请前往 AronShare 官网浏览。

[![封面图片](https://aronshare.com/covers/cover_rustdesk-remote-desktop.webp)](https://aronshare.com/posts/rustdesk-remote-desktop/)

帮家人处理电脑设置，或者在外面操作自己留在家中的电脑，都需要一套能看见画面、控制输入的远程桌面工具。
RustDesk 提供跨平台客户端，也允许用户部署自己的连接服务，适合日常远程协助以及愿意管理基础设施的个人和团队。

使用前有一个明确前提：远程会话应获得设备所有者授权，连接信息只交给可信的人。
账号、支付和私人文件等内容，可以在开始协助前关闭或移出共享画面。

## 远程桌面和文件传输怎么用

按照[官方客户端文档](https://rustdesk.com/docs/en/client/)，RustDesk 启动后会显示本机 ID、一次性密码和用于输入远端 ID 的连接框。
控制端输入目标设备的 ID，并按照被控端设置完成授权，就可以建立远程会话。
客户端还提供权限、显示和剪贴板等设置，可以根据协助范围调整。

RustDesk 支持 Windows、macOS、Linux、Android 和 iOS 等平台，但平台角色有区别。
官方文档明确说明 iOS 设备无法作为被远程控制的一端；选型时要分别确认哪台设备负责发起连接、哪台设备接受控制。

![RustDesk 官方仓库展示本机连接信息与远端设备入口](https://aronshare.com/assets/post-images/rustdesk-remote-desktop/detail-1.webp)

*官方仓库提供的连接管理界面示例，本机信息和历史设备名称已在原图中模糊处理。*

需要把文档、安装包或其他文件送到远端时，可以使用文件传输界面。
本地与远端文件分别显示在两侧，选择目标目录和文件后进行发送或接收，右侧显示传输任务。
涉及工作文件时，应确认接收目录、文件权限和设备归属，避免把资料留在错误的电脑上。

![RustDesk 官方文件传输界面展示本地与远端双栏文件列表](https://aronshare.com/assets/post-images/rustdesk-remote-desktop/detail-2.webp)

*官方仓库的文件传输示例展示了本地目录、远端目录和任务进度，界面外观随版本变化。*


---

### 📖 完整介绍与官方入口

完整文章保留官方资料来源、适用场景及版本和费用条件，下载方式以文章中的实际入口为准。

👉 **[点击前往 AronShare 官网阅读全文](https://aronshare.com/posts/rustdesk-remote-desktop/)**
