# CC Switch 帮你点一下鼠标就切好 Claude Code 和 Codex 的接口配置

[网站全文](https://aronshare.com/posts/cc-switch-ai-cli-manager/)

![Aron 封面](https://aronshare.com/covers/cover_cc-switch-ai-cli-manager.webp)


## CC Switch 是什么

现在很多开发者主力使用 Claude Code、Codex 或 Gemini CLI 在终端里写代码，但日常往往要准备多套接口方案（比如官方订阅、OpenRouter、AWS Bedrock、阿里云百炼、DeepSeek 或智谱 GLM）。每次遇到官方限流要换源时，都得手动去翻找并修改 `.claude.json`、`config.toml` 或环境变量，不小心写错一个逗号还会导致配置报错。

CC Switch 是一款使用 Rust 与 Tauri 2 编写的跨平台桌面配置中心。它专门用来集中接管 Claude Code、Codex、Gemini CLI、OpenCode 与 OpenClaw 五款主流编程 CLI 的底层配置文件，把原本繁琐的改文件操作变成图形界面里的「点一下切换」。

![CC Switch 桌面端多 AI CLI 服务商一键切换与状态管理主界面](https://aronshare.com/assets/post-images/cc-switch-ai-cli-manager-detail-1.webp)

## 它可以解决哪些日常痛点

- **多服务商预设与系统托盘秒级切换**：内置官方登录、OpenRouter、PackyCode、硅基流动、火山方舟、DeepSeek、智谱 GLM、Kimi、MiniMax、百炼等预设模板，配置好 API Key 后可通过系统托盘一键切换生效，并支持接口延迟测速与自动故障转移。
- **统一维护 MCP 服务器与 Skills 扩展**：不用在每个 CLI 工具里重复手写一遍 MCP JSON 配置，可以在同一个面板里通过 stdio、http 或 sse 方式添加 MCP 服务，并扫描管理 GitHub 仓库里的 Claude Skills。
- **跨工具同步系统提示词**：支持保存多套编码规范或角色提示词预设，切换时自动同步写入 Claude 的 `CLAUDE.md`、Codex 的 `AGENTS.md` 以及 Gemini 的 `GEMINI.md`。
- **本地 SQLite 事务存储与云端自动备份**：配置数据采用 SQLite 配合文件原子写入保护，内置最多保留 10 份本地历史快照，并支持结合坚果云、OneDrive、Dropbox 或 iCloud 同步目录在多台开发机之间共享配置。

![CC Switch 统一管理 MCP 服务器与延迟测速配置面板](https://aronshare.com/assets/post-images/cc-switch-ai-cli-manager-detail-2.webp)

## 安装与使用建议

1. **macOS 安装**：可直接通过 Homebrew Tap 安装：`brew tap farion1231/ccswitch && brew install --cask cc-switch`；首次打开如遇未签名拦截，可在「系统设置 -> 隐私与安全性」点击「仍要打开」。
2. **Windows / Linux 安装**：前往 GitHub Releases 下载对应的 `.msi`、便携版 `.zip` 或 `.deb` / `.AppImage` 包；Arch Linux 用户可直接运行 `paru -S cc-switch-bin`。
3. 首次添加并启用新的服务商配置后，请记得**重启正在运行的终端窗口或对应的 CLI 进程**，新的 API 地址与模型映射才会在会话中正式生效。

## 核实来源

- GitHub 仓库：https://github.com/farion1231/cc-switch
- 版本发布与安装包：https://github.com/farion1231/cc-switch/releases
