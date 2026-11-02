# 163MusicLyrics 帮你批量提取云音乐双语滚动歌词并导出本地 LRC 文件

[网站全文](https://aronshare.com/posts/163musiclyrics-lyric-downloader/)

![Aron 封面](https://aronshare.com/covers/cover_163musiclyrics-lyric-downloader.webp)


## 163MusicLyrics 是什么

喜欢把无损音乐保存在本地硬盘、NAS 音乐库（如 Navidrome、 Jellyfin）或者车载 U 盘里的朋友，经常会遇到只有音频文件却没有配套 `.lrc` 滚动歌词的尴尬；尤其是外语或日漫歌曲，想要找带时间轴的原文、中文翻译和罗马音对照歌词，手动一首首复制转换极其耗时。

163MusicLyrics 是一款基于 C# 与 Avalonia 跨平台框架开发的开源歌词提取与处理工具。它同时接入了网易云音乐与 QQ 音乐两大曲库接口，无需登录复杂的客户端，输入歌曲 ID、歌单链接或直接扫描本地音乐文件夹，就能一键批量生成格式规整的本地歌词文件。

![163MusicLyrics 单曲精准搜索与双语时间戳歌词预览界面](https://aronshare.com/assets/post-images/163musiclyrics-lyric-downloader-detail-1.webp)

## 它可以解决哪些日常痛点

- **支持原版歌词、中文译文与罗马音自由组合**：针对外语歌曲，支持勾选同时提取原文歌词、中文翻译和日语罗马音，并按自定义顺序合并到同一个时间轴下，在本地播放器里直接实现双语同步滚动。
- **整张歌单、专辑与本地目录批量扫盘匹配**：除了单曲搜索，还可以直接粘贴整个歌单或专辑 ID 一次性拉取全部曲目歌词；也可以直接选择本地音乐文件夹，自动读取音频元数据（ID3 标签）批量补全缺失歌词。
- **一键导出标准 LRC 与视频剪辑专用 SRT 字幕**：不仅能输出音乐播放器通用的 `.lrc` 格式，还支持直接转换并导出带精准起止时间戳的 `.srt` 字幕文件，做 MV 混剪或音频可视化视频时无需再手动打轴。
- **丰富的时间戳精度、简繁转换与命名模板**：支持毫秒位数截取、中日韩简繁汉字自动转换、空行清洗以及按 `歌手 - 歌名` 等自定义占位符规则自动命名保存。

![163MusicLyrics 歌单模糊检索与多曲目批量导出列表](https://aronshare.com/assets/post-images/163musiclyrics-lyric-downloader-detail-2.webp)

## 安装与使用建议

1. 可直接通过上方的夸克网盘或迅雷网盘获取打包好的免安装版本，解压后运行主程序即可使用，无需额外安装运行库。
2. 遇到同名翻唱版本较多时，建议直接切到顶部「模糊搜索」标签页，输入歌名和歌手名，从结果列表里核对所属专辑与时长后再双击加载。
3. 如需给外语歌配置双语滚动，在主界面右侧「歌词类型」中同时勾选「原始歌词」与「中文歌词」，并将输出合并方式设为「交错合并」或「并列合并」，保存后即可完美适配主流车载与桌面播放器。

## 核实来源

- GitHub 仓库：https://github.com/jitwxs/163MusicLyrics
- 发行版本：https://github.com/jitwxs/163MusicLyrics/releases
