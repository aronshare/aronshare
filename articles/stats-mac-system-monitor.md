# Stats 让你在 Mac 顶部菜单栏一眼看清电脑发烫和网速卡顿原因

[网站全文](https://aronshare.com/posts/stats-mac-system-monitor/)

![Aron 封面](https://aronshare.com/covers/cover_stats-mac-system-monitor.webp)


## Stats 是什么

在 Mac 上跑本地大模型、编译项目或剪辑视频时，电脑偶尔会突然发热掉帧，或者风扇转速飙升。如果每次都要打开「活动监视器」翻找是 CPU 满了、内存交换爆了还是后台在偷偷跑大流量，操作起来非常打断节奏。

Stats 是一款专为 macOS 设计的开源菜单栏系统监控应用。它可以把 CPU、GPU、内存、硬盘读写、网络上下行速度、电池健康度、传感器温度以及风扇转速，以极简的数字、折线图或柱状图常驻在屏幕顶部的菜单栏里，点开即可看到占用最高的进程明细。

![Stats 在 macOS 菜单栏展开的 CPU 与系统负载详细监控面板](https://aronshare.com/assets/post-images/stats-mac-system-monitor-detail-1.webp)

## 它可以解决哪些日常痛点

- **八大硬件模块按需开启与自由组合**：涵盖 CPU、GPU、内存、磁盘、网络、电池、传感器（温度/电压/功耗）与风扇控制，每个模块都可以独立开关，也能把多个指标合并成一个紧凑小组件，避免占满刘海屏两侧的菜单栏空间。
- **点开即查高占用进程与网络详情**：点击任意菜单栏图标会弹出详细面板，不仅有历史走势图，还会直接列出当前消耗 CPU 或内存最多的前几个应用进程，网络面板也能一键查看本机局域网 IP、公网 IP 与连接速率。
- **支持传感器温度读取与风扇转速调节**：在支持的 Mac 机型上可以直接读取芯片核心与电池温度，并支持手动介入风扇转速策略。
- **完全开源免费且资源占用克制**：采用 MIT 协议开源，没有任何订阅内购或广告弹窗，支持 macOS Catalina 及更新系统，对 Apple Silicon和 Intel 机型均有良好适配。

![Stats 磁盘与多模块小组件在 macOS 菜单栏的显示效果](https://aronshare.com/assets/post-images/stats-mac-system-monitor-detail-2.webp)

## 安装与配置建议

1. 推荐使用 Homebrew 一键安装：`brew install --cask stats`，也可以前往 GitHub Releases 页面直接下载最新的 `Stats.dmg` 拖入应用程序目录。
2. 首次启动后，建议进入设置面板只勾选你真正关心的 3~4 项核心指标（例如 CPU 利用率、内存压力和实时网速），如果使用的是带刘海的 MacBook，可以把显示样式设为「文本」或「迷你图表」以节省顶部宽度。
3. 若遇到 macOS 首次打开未签名或第三方开源软件的拦截提示，可在「系统设置 -> 隐私与安全性」中点击允许打开。

## 核实来源

- 官方网站：https://mac-stats.com
- GitHub 仓库：https://github.com/exelban/stats
