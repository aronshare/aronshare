# Glances 让你用一块面板看清这台机器的负载

> 💡 **资源说明**：本文档为精选摘要镜像，完整工具介绍、官方入口与使用条件请前往 AronShare 官网浏览。

[![封面图片](https://aronshare.com/covers/cover_glances-system-monitor.webp)](https://aronshare.com/posts/glances-system-monitor/)

一台跑着十几个容器的机器突然变慢，登录进去敲 top，看 df，切到网卡，来回几个命令才拼出全貌。
Glances 把这些指标放在一个界面里，终端和浏览器都能看。

它是用 Python 写的跨平台监控工具。
CPU、内存、交换分区、负载、磁盘读写、文件系统、网络和温度传感器都在一屏里刷新，Docker、Podman、LXD 里的容器状态也能一起列出来。

两种用法。
命令行里直接敲 glances 就是一个会变色的终端面板；加 -w 参数启动 Web 服务，浏览器打开 61208 端口就是网页版，手机浏览器也能看。

![Glances 网页版，左侧是网络、磁盘、文件系统和传感器，中间是 CPU 与内存](https://aronshare.com/assets/post-images/glances-system-monitor/detail-1.webp)

*官方截图里的网页面板，进程列表按 CPU 占用排序。*

界面之外还有接口。
同一次启动会暴露 REST API，路径在 /api/5 下，脚本或者监控系统可以直接拉数据；指标也能导出到 InfluxDB、Prometheus 这类时序库，或者写成 CSV 文件。

![Glances 手机浏览器里的监控页面，CPU、负载、内存和网卡流量纵向排列](https://aronshare.com/assets/post-images/glances-system-monitor/detail-2.webp)

*手机浏览器访问同一台服务器的 61208 端口，指标会自适应成纵向布局。*

安装方式按习惯挑。
Python 环境用 pip 或 uv 装，服务器上更省事的是直接跑 nicolargo/glances 的 Docker 镜像，容器要能读到宿主机的指标，网络和权限按文档配。

暴露到公网前记得加保护。
Web 模式可以用 glances --set-password 生成访问密码写进配置，放在公网前面再加一层反向代理和 HTTPS 更稳。

适合谁用。
手上有几台 VPS 或者一台家用服务器，想快速看负载和温度，又不想为监控单独搭一套大系统的人。

它管的是单机。
多台机器各开各的实例，看的时候分标签页切换，要做汇总就往时序库里导，交给 Grafana 这类工具画图。
指标超过阈值会标红，底部留一条记录，事后翻是哪台机器在哪个时间点抖过。

---

### 📖 完整介绍与官方入口

完整文章保留官方资料来源、适用场景及版本和费用条件，下载方式以文章中的实际入口为准。

👉 **[点击前往 AronShare 官网阅读全文](https://aronshare.com/posts/glances-system-monitor/)**
