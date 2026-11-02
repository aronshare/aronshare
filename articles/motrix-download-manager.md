# Motrix 帮你用清爽无广告的界面跑满大文件与磁力链接下载速度

[网站全文](https://aronshare.com/posts/motrix-download-manager/)

![Aron 封面](https://aronshare.com/covers/cover_motrix-download-manager.webp)


## Motrix 是什么

浏览器自带的单线程下载器遇到几十 GB 的系统镜像、开源模型权重或压缩包时，不仅速度容易卡死，网络稍微抖动一下还可能前功尽弃；而传统商业下载软件往往塞满了弹窗广告、游戏中心和后台驻留进程。

Motrix 是一款基于 `Aria2` 驱动开发的开源全能下载工具。它把复杂的命令行多线程参数封装进了清爽的图形界面里，同时支持 HTTP/HTTPS 直链、FTP、BT 种子（`.torrent`）和磁力链接，开箱即用且完全没有广告干扰。

![Motrix 桌面端多任务并发下载进度列表界面](https://aronshare.com/assets/post-images/motrix-download-manager-detail-1.webp)

## 它可以解决哪些日常痛点

- **最高 10 任务并发与单任务 64 线程加速**：针对支持断点续传的直链文件，可通过最高 64 线程分块拉取跑满本地宽带，并支持模拟自定义 User-Agent 配合浏览器扩展接管下载。
- **每日自动同步公开 BT Tracker 列表**：很多开源软件用 Aria2 下不动 BT 种子是因为缺少活跃节点，Motrix 内置了「自动更新 Tracker 列表」开关，能每天自动拉取公开 Tracker 提升磁力寻址速度。
- **支持限速调度、UPnP 端口映射与完成后通知**：正在开会或打游戏时可以随时开启全局上下行限速，下载完成后支持系统原生弹窗提醒并自动移除已完成的残留控制文件。
- **跨平台体验一致且原生支持深色模式**：提供 Windows、macOS（含触控栏快捷键）与 Linux多端安装包。

![Motrix 深色模式下的任务详情与速度状态展示](https://aronshare.com/assets/post-images/motrix-download-manager-detail-2.webp)

## 安装与配置建议

1. 前往 Motrix 官网下载安装包，macOS 用户推荐使用 Homebrew 安装：`brew update && brew install --cask motrix`。
2. 首次打开后，强烈建议依次进入「偏好设置 -> 进阶设置」，找到 **Tracker 服务器** 一栏，点击右上角的刷新图标并勾选「每天自动更新 Tracker 服务器列表」，然后点击保存并应用，否则默认状态下磁力链接很容易没有速度。
3. 如果希望在 Chrome 或 Edge 浏览器里点击下载链接时自动唤起 Motrix，可以在应用商店安装配套的 `Motrix WebExtension` 插件并填入本地 RPC 密钥。

## 核实来源

- 官方网站：https://motrix.app
- GitHub 仓库：https://github.com/agalwood/Motrix
