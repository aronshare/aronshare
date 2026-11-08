# 一款能检测局域网陌生设备的开源小工具

> 💡 **资源说明**：本文档为精选摘要镜像，完整工具介绍、官方入口与使用条件请前往 AronShare 官网浏览。

[![封面图片](https://aronshare.com/covers/cover_watchyourlan-network-devices.webp)](https://aronshare.com/posts/watchyourlan-network-devices/)

家里的电脑、手机、电视和智能设备越来越多，路由器设备列表里很容易出现一串认不出的名称。
想知道网络中有哪些主机、哪台设备刚出现、之前何时在线，可以用 WatchYourLAN 持续整理这些信息。

[WatchYourLAN](https://github.com/aceberg/WatchYourLAN) 是带网页界面的轻量局域网 IP 扫描工具。
它利用 `arp-scan` 发现主机，保存设备列表和在线历史，并支持新主机通知，适合在自己拥有或获准管理的局域网中使用。

## 设备列表能看见哪些信息

官方界面展示了设备名称、扫描网卡、IP、MAC、硬件厂商、时间、已知标记和在线状态。
可以按网卡、是否已知、是否在线筛选，也可以搜索设备，并给常用设备改成便于识别的名称。

例如，把 NAS、打印机和常用电脑命名后，新出现的条目就更容易引起注意。
看到陌生设备时，可以结合路由器记录和设备本身核对身份，确认后更新备注与已知标记。

![WatchYourLAN 官方设备列表展示 IP 地址厂商和在线状态](https://aronshare.com/assets/post-images/watchyourlan-network-devices/detail-1.webp)

*官方设备列表截图使用局域网地址示例，展示了筛选、搜索、设备名称和在线状态。*


---

### 📖 完整介绍与官方入口

完整文章保留官方资料来源、适用场景及版本和费用条件，下载方式以文章中的实际入口为准。

👉 **[点击前往 AronShare 官网阅读全文](https://aronshare.com/posts/watchyourlan-network-devices/)**
