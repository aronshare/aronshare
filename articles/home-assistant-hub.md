# Home Assistant 把家里各种品牌的设备收进一个面板

> 💡 **资源说明**：本文档为精选摘要镜像，完整工具介绍、官方入口与使用条件请前往 AronShare 官网浏览。

[![封面图片](https://aronshare.com/covers/cover_home-assistant-hub.webp)](https://aronshare.com/posts/home-assistant-hub/)

家里灯是米家的，空调是美的，窗帘电机走 Zigbee，门口摄像头只认自家 App。
每买一件设备就多一个 App，想实现「进门开灯、家里没人就关空调」，只能靠人记。

Home Assistant 把这些设备收进同一个面板。
它是开源的家庭自动化平台，代码用 Apache-2.0 许可，规则和界面都跑在自己的树莓派或者小主机上，官方强调本地控制和隐私优先。

![官方仓库的集成列表，十八个常见品牌和协议并排](https://aronshare.com/assets/post-images/home-assistant-hub/detail-1.webp)

*官方仓库截图，Alexa、ESPHome、Google Cast、HomeKit、Matter、MQTT、Zigbee、Z-Wave 都在列表里。*

接入方式按品牌分两种。
云端设备走各家官方接口，授权一次就能拉回状态；本地协议直接对接，Zigbee、Z-Wave、Matter、MQTT 都是本机通，断网也能开关灯。

![社区做的 Lovelace 仪表盘示例，灯光、温控、能源和平面图摆在一页](https://aronshare.com/assets/post-images/home-assistant-hub/detail-2.webp)

*官方 README 指向的线上演示界面，作者署名 Arsaboo 保留在卡片上。*

界面按房间和用途自己拼。
官方叫 Lovelace 仪表盘，卡片能拖能换，灯光、温控、能耗曲线、房屋平面图可以放在同一页，手机端自动重排。

自动化是它的核心。
触发条件、判断条件、执行动作三段写完，就是一条规则；时间段、设备状态、日出日落、有人在家都能当条件。
写完的规则能在界面上看执行历史，哪一步没触发有据可查。

安装有三条路。
官方系统镜像刷到树莓派或迷你主机上最省心，整套环境打包好；容器方式适合已经有 Docker 的机器；核心版给自己管理 Python 环境的人，自由度最高，维护也最费人。

跑起来之后要留意的两件事。
数据库会随历史数据长大，官方文档给了换 SQLite 之外数据库的做法；暴露到公网要配反向代理和双因素认证，把设备控制权放到公网上，风险不小。

适合愿意折腾一次、长期省事的人。
设备买回来接进去，规则写几条，之后换手机、换 App 都不用重新适应；代价是头一周要花时间理解实体、区域和设备的关系。

---

### 📖 完整介绍与官方入口

完整文章保留官方资料来源、适用场景及版本和费用条件，下载方式以文章中的实际入口为准。

👉 **[点击前往 AronShare 官网阅读全文](https://aronshare.com/posts/home-assistant-hub/)**
