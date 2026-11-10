# Nginx Proxy Manager 用鼠标配好反向代理和证书

> 💡 **资源说明**：本文档为精选摘要镜像，完整工具介绍、官方入口与使用条件请前往 AronShare 官网浏览。

[![封面图片](https://aronshare.com/covers/cover_nginx-proxy-manager.webp)](https://aronshare.com/posts/nginx-proxy-manager/)

BODY

家里或者公司内网跑了一堆服务，每个都在 `IP:端口` 上。
想用域名访问、想让浏览器不再提示证书不安全，就得改 Nginx 配置文件，改错一个分号，整站 502。

Nginx Proxy Manager 把这份配置搬到网页表单里。
它是开源的反向代理管理面板，底层还是 Nginx，代码用 MIT 许可，用 Docker 镜像分发，官方的目标是让不懂 Nginx 的人也能把域名指到内网服务上。

![Nginx Proxy Manager 后台仪表盘，四个统计卡片分别是代理主机、重定向、流和 404 主机](https://aronshare.com/assets/post-images/nginx-proxy-manager/detail-1.webp)

*官方文档截图，右上角能看到当前管理员账号和主题切换入口。*

建一条代理记录要填的东西不多。
源域名、目标地址和端口、要不要开 SSL、挂不挂访问限制，填完保存，剩下的 Nginx 配置由它生成。
证书可以自动走 Let's Encrypt 申请和续期，也可以传自己的证书文件。

![代理主机列表，源域名、目标地址、SSL 状态和在线状态并排列出](https://aronshare.com/assets/post-images/nginx-proxy-manager/detail-2.webp)

*官方文档截图，表格里两条记录分别是 HTTP Only 与 Let's Encrypt。*

除了反向代理，它把常见的几类入口都做成了独立类型。
重定向主机做 301/302 跳转，Stream 处理 TCP 和 UDP 转发，404 主机接住没有匹配的域名，访问列表能给整站加一层 Basic 认证。

团队共用的时候，用户管理和审计日志有用。
可以给不同人开不同权限，谁改过哪条记录日志里查得到；高级用户还能直接写自定义 Nginx 配置，插在生成的配置里生效。

部署就是一份 compose 文件，数据目录挂出来持久化。
有一条版本限制要记住，2.14 之后不再支持 armv7，路由器或者老 ARM 盒子得停在 2.13.7。
软件免费，成本是服务器、域名和一张证书本来就不用花的钱。

---

### 📖 完整介绍与官方入口

完整文章保留官方资料来源、适用场景及版本和费用条件，下载方式以文章中的实际入口为准。

👉 **[点击前往 AronShare 官网阅读全文](https://aronshare.com/posts/nginx-proxy-manager/)**
