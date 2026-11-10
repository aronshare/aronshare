# Buzz 把录音和视频转成字幕全程不联网

> 💡 **资源说明**：本文档为精选摘要镜像，完整工具介绍、官方入口与使用条件请前往 AronShare 官网浏览。

[![封面图片](https://aronshare.com/covers/cover_buzz-audio-transcription.webp)](https://aronshare.com/posts/buzz-audio-transcription/)

BODY

采访录音、课程视频、会议回放，要变成能搜的文字，最直接的办法是丢给在线转写服务。
素材涉及客户或者没公开的内容时，上传这一步就让人犹豫。
Buzz 解决的就是这件事，转写在你自己这台电脑上跑完。

它是开源的桌面程序，界面基于 Whisper 的本地推理，代码用 MIT 许可。
文件拖进去就排进任务队列，每一行显示文件名、用的模型、任务类型和进度，跑完会写已完成和耗时。

![Buzz 任务列表，四个转写任务分别排队、进行中和已完成](https://aronshare.com/assets/post-images/buzz-audio-transcription/detail-1.webp)

*官方仓库截图，队列里能看到 Faster Whisper、Whisper.cpp 和 Hugging Face 三种后端。*

输入来源不止本地文件。
除了音频和视频，粘一个 YouTube 链接也能直接转，麦克风实时转写适合现场记录和演讲，官方还提供了演示用的窗口，投影到大屏上给观众看字幕。

后端选择是它比较实用的部分。
Faster Whisper、Whisper.cpp、Hugging Face 上的 Whisper 系列模型都能接，Nvidia 显卡走 CUDA，Mac 走 Apple Silicon，其他显卡可以试 Whisper.cpp 的 Vulkan 加速。
换后端对应的是速度和精度的取舍，长录音用大模型慢慢跑，随手录的短音频用小模型更快出结果。

![Buzz 转写结果窗口，左侧时间码对应右侧文本](https://aronshare.com/assets/post-images/buzz-audio-transcription/detail-2.webp)

*官方仓库截图，成稿界面按起止时间分行，可以直接改错字。*

转完的文本能导出 TXT、SRT 和 VTT，剪辑软件和视频平台都认这几种格式。
界面里带搜索和倍速播放，校对的时候一边听一边改时间码。
素材多的场景可以开监听文件夹，新文件落进去自动转写；需要批量处理就写命令行脚本，官方提供了 CLI。

安装上有两个坑要先知道。
Mac 版现在只支持 Apple Silicon，Intel 机器停在 1.4.5；Windows 安装包没有签名，系统会弹警告，需要在提示里点更多信息再继续。
Linux 有 Flatpak、Snap 和 AppImage，用 pip 装的版本要自己补 ffmpeg 和 CUDA 依赖。

转写速度全看硬件。
一段一小时的中文录音，独显机器几分钟能出结果，只有 CPU 的话要等更久，长素材安排在空闲时段跑更合适。

---

### 📖 完整介绍与官方入口

完整文章保留官方资料来源、适用场景及版本和费用条件，下载方式以文章中的实际入口为准。

👉 **[点击前往 AronShare 官网阅读全文](https://aronshare.com/posts/buzz-audio-transcription/)**
