# Dozzle 让你在浏览器里盯住每个容器的日志

> 💡 **资源说明**：本文档为精选摘要镜像，完整工具介绍、官方入口与使用条件请前往 AronShare 官网浏览。

[![封面图片](https://aronshare.com/covers/cover_dozzle-docker-log-viewer.webp)](https://aronshare.com/posts/dozzle-docker-log-viewer/)

BODY

容器跑起来之后，出问题第一件事是看日志。
`docker logs -f` 一次只能盯一个容器，服务一多，几个终端窗口来回切，滚动的速度还赶不上手速。

Dozzle 把这个动作搬到浏览器里。
它是用 Go 写的轻量应用，镜像压缩后只有 7MB 左右，挂上 Docker 的 socket 就能读到所有容器的日志，自己不做持久化存储，只负责实时看。

![Dozzle 主界面，左侧容器列表，右侧实时日志流](https://aronshare.com/assets/post-images/dozzle-docker-log-viewer/detail-1.webp)

*官方仓库演示动画的截帧，顶部能看到网络、磁盘、CPU 和内存的实时读数。*

搜索是它比命令行顺手的地方。
容器名支持模糊匹配，日志内容可以用正则过滤，还能直接写 SQL 语句查询字段，把 JSON 格式的结构化日志当成一张表来筛。
分屏视图同时盯几个容器的输出，排查调用链上的问题不用来回切页。

![Dozzle 日志操作面板，容器名切换与筛选入口](https://aronshare.com/assets/post-images/dozzle-docker-log-viewer/detail-2.webp)

*官方文档截图，演示数据里是 api、postgres、redis、web、worker 五个容器。*

部署只要一条命令。
把 `/var/run/docker.sock` 挂进容器，映射 8080 端口，浏览器打开就能用。
多用户认证支持转发代理鉴权，Swarm 模式和多主机场景用 agent 模式接进来，同一套界面管几台机器。

有两点限制要提前知道。
它不做离线检索，日志关掉页面就没了，真要做长期归档和全文搜索，官方也直说该上 Loki、Kibana 这类方案。
另一个要留意的是 socket 权限，把 Docker socket 交给容器相当于给了宿主机控制权，暴露到公网之前先套一层带认证的反向代理。

---

### 📖 完整介绍与官方入口

完整文章保留官方资料来源、适用场景及版本和费用条件，下载方式以文章中的实际入口为准。

👉 **[点击前往 AronShare 官网阅读全文](https://aronshare.com/posts/dozzle-docker-log-viewer/)**
