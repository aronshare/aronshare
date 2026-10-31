---
title: "ntfy 让脚本在任务完成或失败时给手机发通知"
category: "开源自托管"
category_slug: "open-source"
tags: ["ntfy", "自动化", "消息推送", "开源自托管"]
published_at: "2026-10-31 12:08:20"
author: "Aron"
cover: "https://aronshare.com/covers/cover_ntfy-push-notifications.webp"
summary: "ntfy 可以通过 HTTP 请求把脚本结果推送到手机和桌面，适合备份提醒、定时任务告警与下载完成通知。支持公共服务和自托管，使用时需要留意主题访问权限、浏览器后台通知与 iOS 推送配置。"
platforms: ["Web", "Android", "iOS", "Docker"]
license: "Apache-2.0 / GPLv2 双许可证"
pricing: "公共服务提供免费使用与付费套餐；自托管需承担服务器费用"
official_url: "https://ntfy.sh/"
repo_url: "https://github.com/binwiederhier/ntfy"
download_url: "https://docs.ntfy.sh/install/"
source_name: "ntfy 官方文档与 GitHub 仓库"
source_url: "https://github.com/binwiederhier/ntfy"
needs_rewrite: false
---

备份脚本半夜跑完、文件下载结束、定时任务报错，这些结果通常留在电脑的终端或日志里。
想在手机上收到提醒，可以给脚本加一条 ntfy 消息。
它通过 HTTP PUT 或 POST 接收文字，再把消息送到订阅同一主题的手机或桌面端，适合为已有自动化任务补上通知。

## 用主题把脚本和手机连起来

ntfy 的基本单位是主题，也就是一段用来区分消息频道的名称。
在 Android、iOS 应用或网页端订阅一个主题后，脚本向对应地址发送消息，订阅端就能接收。
[官方入门文档](https://docs.ntfy.sh/)提供了 curl、Python 和 JavaScript 等写法，只要现有工具能够发出 HTTP 请求，就有机会把结果接进来。

例如，可以把备份提醒与下载提醒分成不同主题，避免普通进度消息淹没故障通知。
任务是否成功仍由脚本的退出状态决定；ntfy 负责传递脚本已经生成的结果。

![ntfy 官方网页端截图中的主题列表、通知内容与图片附件](https://aronshare.com/assets/post-images/ntfy-push-notifications-ui.png)

*图片来自 ntfy 官方仓库，展示网页端通知与附件界面。*

## 发出第一条提醒只需要一条请求

打开 ntfy 手机应用或网页端，订阅自己选择的主题。
下面是依据官方接口整理的命令示例，运行前需要把 `YOUR_PRIVATE_RANDOM_TOPIC` 替换成自己的随机主题名，并确认客户端订阅的是同一个名称。

```bash
curl --fail \
  -H "Title: Backup finished" \
  -H "Tags: white_check_mark" \
  -d "Backup completed. Check the log for details." \
  https://ntfy.sh/YOUR_PRIVATE_RANDOM_TOPIC
```

这条命令会向官方公共服务发送一条通知。
[发送文档](https://docs.ntfy.sh/publish/)还介绍了优先级、标签、附件和点击链接等字段，可以让失败消息更醒目，也可以让通知直接指向相关页面。
把请求放在脚本的成功或失败分支里，通知文字就能对应实际运行结果。
通知请求本身也可能遇到断网或限流，重要任务需要保留原有日志，并处理 curl 的失败退出状态。

## 公共主题需要认真处理访问权限

官方入门文档明确提醒，公共服务上的主题名是公开的。
未保护的主题如果被他人知道，就存在消息被读取或被发送无关内容的风险。
试用时使用难以猜到的随机名称，并只发送不敏感的测试信息。
密码、访问令牌、客户资料和完整业务日志应留在受保护的系统中。

需要控制谁能读写时，可以查看服务套餐中的主题保留功能，或在自托管服务器上配置用户、访问令牌和主题权限。
[官方访问控制说明](https://docs.ntfy.sh/config/#access-control)给出了相关配置，私有实例可以采用默认拒绝访问的方式，为需要使用的账户单独授权。
随机主题名适合降低被碰巧发现的概率；业务消息的保护还需要明确的访问控制。

## 自托管要照顾数据和推送链路

ntfy 提供 Docker 等安装方式。
按照[官方安装文档](https://docs.ntfy.sh/install/)，容器可运行 `binwiederhier/ntfy` 镜像，服务通过 `serve` 启动。
长期使用需要配置消息缓存的持久化目录，并按需要挂载配置文件；向外提供服务时，还要安排 HTTPS、认证和备份。

手机平台也有配置差异。
[官方配置文档](https://docs.ntfy.sh/config/#ios-instant-notifications)说明，自托管实例要在 iOS 上获得即时推送，需要设置上游地址，让上游转发唤醒请求，手机应用随后向自己的服务器读取消息正文。
如果希望完全掌握消息流向，这条链路也应该纳入部署考虑。

桌面端则要检查浏览器通知权限与后台通知设置。
根据[网页端说明](https://docs.ntfy.sh/subscribe/web/)，关闭后台通知时需要保持 ntfy 标签页打开；开启后仍会受浏览器和系统支持情况影响。
部署完成后，可以用一条普通提醒核对手机锁屏、浏览器后台等实际接收场景。

## 适合给已有自动化任务补上提醒

ntfy 的公共服务提供免费使用方式，也有付费套餐；免费使用受到服务限额约束，具体配额应查看当前账户方案。
项目提供 Apache-2.0 与 GPLv2 双许可证，自托管的服务器、网络与维护由自己承担。
[官方仓库](https://github.com/binwiederhier/ntfy)提供源码、客户端入口及套餐说明。

如果已经有 NAS 备份、定时脚本或下载任务，可以从一个低敏感度提醒开始接入。
确定消息内容、权限和接收设备都符合需要后，再扩展到其他任务。
对于需要完整流程编排的工作，ntfy 更适合作为其中的通知环节。

- [打开 ntfy 网页端](https://ntfy.sh/app)
- [阅读发送消息文档](https://docs.ntfy.sh/publish/)
- [查看自托管安装方式](https://docs.ntfy.sh/install/)
