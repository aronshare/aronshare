# Cherry Studio 让你在一个软件里同时调用多家大模型和本地知识库

[网站全文](https://aronshare.com/posts/cherry-studio-ai-client/)

![Cherry Studio 官方界面](https://aronshare.com/covers/cover_cherry-studio-ai-client.webp)


## Cherry Studio 是什么

日常使用大模型处理文档或写代码时，很多人会同时打开 ChatGPT、Claude、DeepSeek 等多个网页标签页，或者在本机运行 Ollama 模型。不同平台的对话记录分散在各处，提示词模板和知识库文件也得重复上传。

Cherry Studio 是一款跨平台桌面客户端，用来把不同来源的模型接口整合到同一个工作台里。无论是云端 API 还是本地运行的开源模型，都可以在同一套界面里切换调用，并且共用本地保存的预设助手、文档知识库和 MCP 工具扩展。

![Cherry Studio 桌面端多模型对话与内置智能体助手界面](https://aronshare.com/assets/post-images/cherry-studio-ai-client-detail-1.webp)

## 它可以解决哪些日常痛点

- **统一接入云端与本地模型**：原生支持 OpenAI、Anthropic、Gemini、OpenRouter 等云端服务商，也能直接连接本机运行的 Ollama 和 LM Studio，还可以导入兼容 OpenAI、Anthropic 或 Gemini 格式的自定义接口。
- **一条提问同时发给多个模型对比**：遇到拿不准的翻译、润色或代码排错问题，可以在同一个对话框里同时勾选多个模型并发作答，直观对比哪家的输出更可用。
- **本地知识库支持多种办公文档格式**：可以把 PDF、DOCX、PPTX、XLSX、TXT、Markdown 乃至网页链接和整站 Sitemap 导入本地知识库，检索后再结合大模型回答，不必每次手动复制长文档。
- **定时后台任务与 WebDAV 多机备份**：支持用自然语言配置定时执行的监控、汇总或日报生成任务；对话记录与配置支持通过 WebDAV 或本地导出在不同电脑之间同步。

![Cherry Studio 代码高亮渲染与多服务商配置面板](https://aronshare.com/assets/post-images/cherry-studio-ai-client-detail-2.webp)

## 安装与配置建议

1. 前往 Cherry Studio 官网下载页或 GitHub Releases，根据系统选择对应的安装包（支持 Windows、macOS 和 Linux）。
2. 打开软件后进入左下角的「设置 -> 模型服务」，填入你常用的 API Key，或者开启本地 Ollama 地址连接。
3. 如果需要用到知识库功能，建议在模型服务里先启用一个 Embedding（嵌入）模型，再新建知识库导入文档，检索准确度会明显高于纯文本截断。
4. 个人与日常办公使用开源社区版完全免费，但调用第三方云端模型的 API 费用由对应服务商按量计费；团队单点登录与集中管控属于商业企业版范畴。

## 核实来源

- 官方网站：https://cherry-ai.com
- 官方文档：https://docs.cherry-ai.com
- GitHub 仓库：https://github.com/CherryHQ/cherry-studio
