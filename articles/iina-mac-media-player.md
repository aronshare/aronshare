# IINA 让 Mac 不用转格式就能顺畅播放各种本地视频和字幕

[网站全文](https://aronshare.com/posts/iina-mac-media-player/)

![Aron 封面](https://aronshare.com/covers/cover_iina-mac-media-player.webp)


## IINA 是什么

Mac 自带的 QuickTime Player 界面很清爽，但一旦遇到 MKV、FLV、RMVB 或带复杂内嵌字幕的高码率视频就会提示无法打开；而老牌的 VLC 虽然格式兼容性好，界面和操作手势却和 macOS 的设计风格格格不入。

IINA 是一款专门为 macOS 开发的开源媒体播放器。它底层采用解码能力极强的开源项目 `mpv`，外壳则完全使用原生开发语言重写，把多格式硬解播放、触控板手势、深色模式、画中画和快捷键自定义做进了同一套符合 Mac 直觉的界面里。

![IINA 在 macOS 桌面下的无边框视频播放与悬浮控制栏界面](https://aronshare.com/assets/post-images/iina-mac-media-player-detail-1.webp)

## 它可以解决哪些日常痛点

- **通吃主流本地视频与网络流媒体**：依托 mpv 与 FFmpeg 解码内核，几乎不用再额外安装转码工具，支持播放本地多音轨、多字幕封装文件，也能直接结合 `yt-dlp` 打开在线视频流和 M3U 播放列表。
- **在线字幕自动搜索与画面自由微调**：播放生肉视频或外语课程时，可以直接在菜单里在线检索并挂载匹配字幕；右侧面板还能随时调节倍速、画面裁剪比例、音频延迟和均衡器参数。
- **原生贴合 Mac 的触控与多任务体验**：完整支持 Force Touch 用力点按、触控板双指滑动调节进度或音量、系统原生画中画悬浮窗，以及专门针对音频文件设计的迷你「音乐模式」。
- **支持命令行调用与浏览器一键唤起**：安装包自带 `iina-cli` 命令行工具，并提供 Chrome 与 Firefox 浏览器扩展，遇到网页视频可以直接一键投送到本地 IINA 窗口播放。

![IINA 音乐模式与播放列表管理窗口展示](https://aronshare.com/assets/post-images/iina-mac-media-player-detail-2.webp)

## 安装与使用建议

1. 可以前往 IINA 官网下载 `.dmg` 安装包，或者在终端直接运行 `brew install --cask iina` 完成安装（支持 macOS 10.15 及以上系统，原生适配 Apple Silicon 与 Intel 芯片）。
2. 安装完成后，建议打开「IINA -> 设置 -> 通用」，点击将 IINA 设为默认的视频文件打开应用，省去每次右键选择打开方式的步骤。
3. 如果需要用 IINA 直接打开网页视频链接，建议在 Homebrew 中一并安装或更新最新的 `yt-dlp`，并在 IINA 的「网络」设置中指向该可执行文件目录，以获得更稳定的解析成功率。

## 核实来源

- 官方网站：https://iina.io
- GitHub 仓库：https://github.com/iina/iina
