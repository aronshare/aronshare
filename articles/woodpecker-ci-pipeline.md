# Woodpecker 把 CI 流水线搬回自己的服务器

> 💡 **资源说明**：本文档为精选摘要镜像，完整工具介绍、官方入口与使用条件请前往 AronShare 官网浏览。

[![封面图片](https://aronshare.com/covers/cover_woodpecker-ci-pipeline.webp)](https://aronshare.com/posts/woodpecker-ci-pipeline/)

代码提交之后自动跑测试、打包镜像、推到仓库，这套流程大部分团队都在用。
问题出在托管服务上：私有仓库要付费，构建机在别人那里，密钥配置散在第三方后台。

Woodpecker 把这套流程放回自己的服务器。
它是开源的持续集成工具，代码 Apache-2.0 许可，一个 server 负责界面和调度，一个或多个 agent 负责真正跑任务，源码托管在 Gitea、Forgejo、GitHub、GitLab 都能接。

流水线用 YAML 写，和大多数 CI 一样的思路。
每个 step 指定一个容器镜像，在里面跑命令；多个 step 组成 pipeline，能并行也能串行，构建产物在 step 之间共享工作目录。

![流水线详情里的本地复跑面板，给出 woodpecker exec 命令和元数据下载](https://aronshare.com/assets/post-images/woodpecker-ci-pipeline/detail-1.webp)

*官方文档截图，下载 metadata 之后用 CLI 在本地复现同一次构建。*

排错这块有个省时间的做法。
界面能把某次流水线的元数据导出，本地执行 `woodpecker exec --metadata-file` 复跑同一套配置，改完再提交，不用每次推上去等结果。
构建日志在界面上按 step 折叠，失败那一步直接展开到出错行。

![流水线配置校验报错列表，四条问题逐条指出文件和字段](https://aronshare.com/assets/post-images/woodpecker-ci-pipeline/detail-2.webp)

*官方文档截图，linter 指出同时配置了 commands 与 settings、image 类型不对等问题。*

配置写错的时候它拦得比较早。
提交之后先跑一遍 lint，把字段类型、不允许的属性、插件参数逐条列出来，错误定位到 `steps.某一步`，不用等整条流水线跑完才看到红叉。

部署分两半。
server 起来之后用 Gitea 或者 GitHub 账号授权登录，agent 注册时拿一个共享密钥连上来，可以只跑 docker 的任务，也可以开 Kubernetes 后端把 pod 当执行环境。
密钥和环境变量配在仓库、组织、全局三层，权限跟着仓库走。

资源占用比想象中低。
一台 2 核 4G 的小机器跑 server 加上一个 agent，中小项目的构建够用；跑镜像构建这类重活时，把 agent 单独放到一台配置好点的机器上更合适。

迁移成本主要在 YAML。
已有的 GitHub Actions 或者 GitLab CI 配置不能直接搬，需要按 Woodpecker 的语法改写 step 和插件；逻辑不复杂的流水线，一下午能迁完。

---

### 📖 完整介绍与官方入口

完整文章保留官方资料来源、适用场景及版本和费用条件，下载方式以文章中的实际入口为准。

👉 **[点击前往 AronShare 官网阅读全文](https://aronshare.com/posts/woodpecker-ci-pipeline/)**
