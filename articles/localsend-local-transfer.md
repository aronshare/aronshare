# LocalSend 让手机和电脑在局域网里直接传文件

[网站全文](https://aronshare.com/posts/localsend-local-transfer/)

![LocalSend 官方界面](https://aronshare.com/covers/cover_localsend-local-transfer.webp)


手机里拍好的照片要传到电脑，电脑上的 PDF 又要发回手机，设备就在旁边，却经常要绕到聊天软件或网盘里中转。
LocalSend 适合处理这种临时传文件的需求：让设备连接到能够互相访问的局域网，通过应用直接发送文件或文字。

## 不同系统也能互相传送

[LocalSend 官方项目](https://github.com/localsend/localsend)提供 Windows、macOS、Linux、Android 和 iOS 客户端。
它通过本地网络通信，默认使用 HTTPS 加密传输，不依赖第三方中转服务器，也无需互联网连接。
使用时可以保留加密设置，并确认接收设备的名称。
这里仍然需要一条设备之间可用的本地网络，例如家里允许设备互通的 Wi-Fi。

对混用设备的人来说，这意味着可以用同一套工具处理安卓手机到 Mac、iPhone 到 Windows 等组合的文件传送。
传输是否顺利还取决于双方的网络权限、防火墙和路由器设置。

![LocalSend 官方展示的桌面端接收文件窗口](https://aronshare.com/assets/post-images/localsend-local-transfer-official-ui.webp)

*图片来自 LocalSend 官方网站源码仓库，展示桌面端接收文件及传输进度。*

## 用一份文件确认收发过程

双方都安装应用后，可以从一份照片或 PDF 开始使用。
发送端选择文件和目标设备，接收端确认对应的请求，完成后到接收位置查看文件。
设备名称相近时，把应用中显示的名称与对方屏幕对照，避免选错对象。

文字也可以通过 LocalSend 发送。
例如电脑上找到的链接、准备复制到手机里的短段落，都能作为临时传递的内容。
文件发送完成后，可以直接检查接收位置里的文件能否打开，确认自己拿到的是需要的那一份。

## 找不到设备时检查局域网设置

“连着同一个 Wi-Fi，却看不见另一台设备”是这类工具容易遇到的情况。
[官方排查说明](https://github.com/localsend/localsend#troubleshooting)列出了几个具体方向。

- 路由器启用了 AP 隔离时，设备之间的连接会被阻止，访客网络尤其需要留意这一设置。
- macOS 和 iOS 需要允许应用访问本地网络，可以在系统隐私设置中检查权限。
- Windows 的公共网络配置可能限制设备连接，在可信的家庭网络中可检查网络类型与应用防火墙权限。
- VPN 可能拦截局域网流量，需要允许本地网络通信，或在合适的情况下暂时断开 VPN 排查。

官方设置说明列出的入站端口是 TCP 和 UDP 的 `53317`。
如果确实需要调整防火墙，按应用及可信局域网范围放行相应通信，保留其他防护规则。
公司或学校网络有统一管理要求时，应由网络管理员确认设备互通条件。

## 下载安装时留意系统版本和更新渠道

LocalSend 采用 Apache-2.0 许可，官方将其作为免费开源应用提供。
普通使用可以下载安装包，无需搭建服务器，也无需安装开发工具。

官方 README 的兼容性表列出 Android 7.0、iOS 13.0、macOS 11 和 Windows 10 等最低版本要求；从其他应用向 LocalSend 分享内容需要 iOS 14 或更新系统。
旧设备应对照官方兼容性说明选择版本，不要随意下载来源不明的安装包。

应用自身没有自动更新功能，官方建议通过应用商店或包管理器安装，以方便后续更新。
使用独立安装包的人，可以定期查看官方发布页，确认自己安装的版本。

## 适合临时发送文件和文字

LocalSend 的使用场景很明确：设备在同一个可互通的局域网里，需要把选定文件发给另一台设备。
如果希望一个工作文件夹随着每天的编辑持续同步，就需要专门的文件夹同步方案。

可以把它装在经常互传文件的手机和电脑上，确认网络权限后，试着发送一份 PDF 和一张照片。
收发过程与保存位置都符合习惯，就可以把这条方式留作日常传文件的入口。

- [查看官方介绍与下载渠道](https://github.com/localsend/localsend#download)
- [查看官方发布页](https://github.com/localsend/localsend/releases)
- [阅读连接问题排查说明](https://github.com/localsend/localsend#troubleshooting)
