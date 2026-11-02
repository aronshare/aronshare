# Spotube 让你不充会员也能在电脑和手机上安静听歌管歌单

[网站全文](https://aronshare.com/posts/spotube-music-client/)

![Aron 封面](https://aronshare.com/covers/cover_spotube-music-client.webp)


## Spotube 是什么

平时在电脑上边写代码边听歌，官方流媒体客户端往往占用不少内存，免费账号还会频繁插播语音广告或限制切歌。

Spotube 是一款采用 Flutter 和 Rust 编写的轻量级开源音乐播放器。它在新版架构中改成插件化机制，一面拉取公开的专辑、歌手和榜单元数据，另一面从 YouTube、Piped、Invidious 或 JioSaavn 等公开音源自动匹配对应的音轨进行播放和缓存，界面干净且没有广告弹窗。

![Spotube 桌面端专辑曲库浏览与播放控制界面](https://aronshare.com/assets/post-images/spotube-music-client-detail-1.webp)

## 它可以解决哪些日常痛点

- **把曲库索引与实际播放音源解耦**：通过内置或社区开发的元数据插件管理歌单、专辑和推荐列表，播放时自动从第三方公开音视频流拉取音频，支持手动切换匹配的音源版本。
- **自带逐行同步歌词与本地缓存下载**：播放界面内嵌时间轴同步歌词，遇到常听的曲目可以直接下载到本地离线收听，减少重复流媒体加载消耗。
- **无遥测追踪且支持收听统计集成**：软件本身不收集个人隐私数据，如果平时习惯记录听歌足迹，可以在设置里绑定 Last.fm 或 ListenBrainz 账号自动同步播放记录。
- **全平台统一界面与无头服务端模式**：同时提供 Windows、macOS、Linux、Android 与 iOS（IPA 侧载）版本，并正在推进 CLI 无头服务端加网页远程控制能力。

![Spotube 歌单详情与实时同步歌词界面](https://aronshare.com/assets/post-images/spotube-music-client-detail-2.webp)

## 安装与使用建议

1. 可以从官网下载页或 GitHub Releases 获取对应系统的安装包；macOS 用户也可直接运行 `brew install --cask spotube`，Windows 用户可用 `winget install --id KRTirtho.Spotube` 或 `scoop install spotube`。
2. 自 v5.0 版本起，首次打开软件需要先在插件设置里确认启用一个元数据插件，曲库首页和搜索结果才会正常加载。
3. 由于默认音频流经常来自 YouTube 或 Piped 节点，国内网络环境直接播放如果遇到缓冲慢，建议在音源设置中切换可用的 Piped/Invidious 实例，或配置本地代理。
4. 该项目仅适合点播音乐与个人歌单管理，不支持播客与有声书节目。

## 核实来源

- 官方网站：https://spotube.krtirtho.dev
- 官方下载页：https://spotube.krtirtho.dev/downloads
- GitHub 仓库：https://github.com/KRTirtho/spotube
