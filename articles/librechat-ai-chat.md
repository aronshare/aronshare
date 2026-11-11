# LibreChat 把七八家模型塞进一个聊天框，还能自己部署

> 💡 **资源说明**：本文档为精选摘要镜像，完整工具介绍、官方入口与使用条件请前往 AronShare 官网浏览。

[![封面图片](https://aronshare.com/covers/cover_librechat-ai-chat.webp)](https://aronshare.com/posts/librechat-ai-chat/)

同一个人手上往往有四五个模型账号。

Claude 写长文顺手，GPT 处理表格稳，某些任务要跑本地 Ollama，OpenRouter 上还有几个便宜端点备用。

结果是浏览器开着五个标签页，对话记录散在五个地方，谁也翻不回去。

LibreChat 把这件事收进一个界面。它是 MIT 许可的自托管 AI 聊天平台，官方支持的端点包括 Anthropic、AWS Bedrock、OpenAI、Azure OpenAI、Google、Vertex AI 和 OpenAI Responses API，任何 OpenAI 兼容端点都能接，Ollama、LM Studio、OpenRouter、DeepSeek 就这样挂进去。

![](https://aronshare.com/assets/post-images/librechat-ai-chat/detail-1.webp)

它的界面跟主流聊天产品差不多，左边是项目、置顶和按月份分组的会话列表，中间是对话区，底部写着版本号和隐私政策。

差别在你给出的东西不用只喂给一家。

写长文时切 Claude，分析数据切 GPT，需要省钱的长任务丢给本地模型，同一份对话历史跟着走。

Agent 这块支持无代码构建，有 Agent Marketplace，能挂 MCP 服务器和工具，能加载 SKILL.md 技能包，还支持子 Agent 和 Agent 管理 API。

![](https://aronshare.com/assets/post-images/librechat-ai-chat/detail-2.webp)

上图就是 Agent Tools 选择弹窗，Spotify、Google、YouTube、OpenAI 图像工具、Wolfram 这些能力按卡片列出，点 Add 加进来，点 Remove 摘掉。

代码解释器是独立的一套 API，在沙箱里跑 Python、Node.js、Go、C/C++、Java、PHP、Rust、Fortran，底层是 ClickHouse 的 code-interpreter，适合让它算东西、读文件、画图，答案有据可查。

多用户这块给得比较全：OAuth2、LDAP、邮箱登录都支持，内置审核和 token 消耗统计，团队共用一套部署时能看清谁用掉了多少额度。

断线续传从单机到横向扩展都能用，横向扩展要额外挂 Redis。

代价说清楚。

最新功能带实验标记，Agent 管理 API 标着 beta，Attached workspaces 标着 highly experimental，急着上生产要绕开这些。

升级要读 changelog，官方明确要求先看破坏性变更说明再动，直接拉最新镜像有可能把现有配置弄坏。

仓库把最新版本标成 prerelease，说明项目自己的节奏还没走到稳定发布。

自托管需要 MongoDB，配 Docker 起来最省事，模型调用费用另算，走哪家给哪家。

谁适合用：手上有多家模型 key、想统一入口的；团队要一套能看用量、能控权限的 AI 工作台的；被单一供应商限流卡住过的。

谁别碰：只有一个人、只用一家模型、对话记录也不在乎的，官方客户端就够。

官网 librechat.ai 有文档和演示地址，源码在 github.com/danny-avila/LibreChat，两张截图里显示的是官方不同版本的后台界面。

---

### 📖 完整介绍与官方入口

完整文章保留官方资料来源、适用场景及版本和费用条件，下载方式以文章中的实际入口为准。

👉 **[点击前往 AronShare 官网阅读全文](https://aronshare.com/posts/librechat-ai-chat/)**
