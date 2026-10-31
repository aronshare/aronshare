---
title: "changedetection.io 帮你盯住网页变化并在需要时发来提醒"
category: "开源自托管"
category_slug: "open-source"
tags: ["changedetection.io", "网页监控", "自动化", "开源自托管"]
published_at: "2026-10-31 10:30:00"
author: "Aron"
cover: "https://aronshare.com/covers/cover_changedetection-website-monitor.webp"
summary: "changedetection.io 可以定期检查网页、记录内容差异并发送提醒，适合追踪公告、招聘信息、商品价格和补货状态。支持筛选页面区域、浏览器交互与多种通知渠道，可自托管，也有付费托管服务。"
platforms: ["Web", "Docker", "Python"]
license: "Apache-2.0"
pricing: "开源自托管；官方另有付费托管，服务器、代理及可选模型费用需按使用方式承担"
official_url: "https://changedetection.io/"
repo_url: "https://github.com/dgtlmoon/changedetection.io"
download_url: "https://github.com/dgtlmoon/changedetection.io#installation"
source_name: "changedetection.io 官网与官方 GitHub 仓库"
source_url: "https://github.com/dgtlmoon/changedetection.io"
needs_rewrite: false
---

有些公告页没有订阅入口，商品补货也没有邮件提醒，只能隔一段时间打开网页查看。
changedetection.io 可以替你定期检查这些页面，保存变化记录，并把符合条件的更新发到通知渠道。
它适合持续关注一组已知网页，尤其是你只关心其中某个区域或某类变化的时候。

## 把反复打开的网页加入监控列表

在 changedetection.io 中添加网页地址，并设置检查间隔，就可以建立一条监控任务。
后续检查发现变化时，可以打开差异记录，查看增加、删除或修改了哪些文字。
[官方项目说明](https://github.com/dgtlmoon/changedetection.io)介绍了按单词、行和字符查看差异的方式，也支持 PDF 文本变化与 JSON 数据监控。

例如，招聘页面可以关注职位列表，产品网站可以关注更新日志，公共信息网站可以关注公告正文。
这些场景有一个共同点：你已经知道信息会出现在哪里，希望更新出现时收到提醒。
检查间隔由任务配置决定，通知时间也受目标网站响应和抓取情况影响。

![changedetection.io 官方截图中的监控列表、文字变化与价格历史图](https://aronshare.com/assets/post-images/changedetection-website-monitor-ui.png)

*图片来自 changedetection.io 官方仓库，展示任务列表、变化摘要和商品价格历史。*

## 缩小监控范围可以减少无关提醒

网页上的轮播图、日期和推荐内容经常变化。
如果把整页都纳入比较，提醒里容易混入你并不关心的信息。
changedetection.io 提供 CSS 选择器、XPath、关键词与正则表达式等筛选方式，可以限定目标区域、忽略指定文字，或在某段文字出现时触发通知。

配合浏览器抓取器时，还可以使用 Visual Selector，在页面截图上选择关注区域。
对于刚开始使用的人，可以用一个公告列表练习：选择列表主体，排除导航和页脚，检查保存下来的内容是否覆盖标题与日期。
监控范围选得合适，后续差异就更容易阅读。

商品页面还提供价格与补货监控选项，可以设定价格条件，并查看变化历史。
能否提取到正确的商品数据，取决于页面结构和抓取结果；价格提醒到达时，仍需要打开商家页面确认实际售价与库存。

## 动态网页需要浏览器抓取能力

普通静态网页可以使用内置 HTTP 抓取器。
内容依赖 JavaScript 加载时，需要连接浏览器抓取服务。
[官方仓库的 Compose 配置](https://github.com/dgtlmoon/changedetection.io/blob/master/docker-compose.yml)提供了相关连接示例，部署时应按配置说明启用相应服务。

Browser Steps 可以在检查前执行填写输入框、点击按钮等操作，适用于获得授权的登录页面或带有搜索条件的页面。
官方说明中，Browser Steps 与 Visual Selector 需要启用 Playwright。
这类任务还需要维护登录状态，网站改版、验证码或访问限制也可能让抓取中断。
设置任务时，应遵守目标网站的访问规则，并选择适当的检查频率。

## 通知可以接到日常使用的渠道

changedetection.io 通过 Apprise 支持邮件、Telegram、Discord、Slack 等通知方式。
按照[官方通知说明](https://github.com/dgtlmoon/changedetection.io#notifications)，在任务的通知设置中填入相应的通知 URL，就可以指定接收渠道，并定制标题和正文。
通知 URL 可能包含令牌或密码，需要像账户凭据一样保存，避免出现在公开截图或分享链接中。

如果希望把较长的差异整理成简短说明，项目也提供可选的 AI 摘要和条件判断。
[官方 AI 配置教程](https://changedetection.io/tutorial/ai-summary-and-change-detection-bring-your-own-key)介绍了接入自己的模型服务，官方 README 也列出 Ollama 等本地模型选择。
使用在线模型时，需要考虑提交给模型的网页内容及调用费用；普通文字比较和筛选可以独立使用。

## 自托管从本机访问开始更稳妥

准备好 Docker 后，可以参考官方 README 的独立容器方式启动：

```bash
docker run -d --restart always \
  -p "127.0.0.1:5000:5000" \
  -v datastore-volume:/datastore \
  --name changedetection.io \
  dgtlmoon/changedetection.io
```

该示例把服务绑定在本机回环地址，启动后在同一台电脑访问 `http://127.0.0.1:5000`。
`datastore-volume` 用于持久保存监控数据，备份与迁移时需要照顾这个数据卷。
如果运行在远程服务器，可以通过安全隧道访问，或配置带认证与 HTTPS 的访问入口。
上述基础启动方式适合建立普通网页任务；JavaScript 页面和浏览器交互还需要补齐浏览器服务配置。

项目采用 Apache-2.0 许可，自托管的服务器、存储及可选代理费用由自己承担。
不想维护服务，可以查看[官网的付费托管方案](https://changedetection.io/)，按当前页面确认监控数量、检查条件和价格。

从几个确实需要反复查看的页面开始，设置筛选规则并发出测试通知，确认差异内容与提醒渠道都能满足需求。
当任务出现抓取错误或网站改版时，及时调整规则，才能持续得到有用的提醒。

- [访问 changedetection.io 官网](https://changedetection.io/)
- [查看 GitHub 源码与安装说明](https://github.com/dgtlmoon/changedetection.io)
- [阅读官方教程](https://changedetection.io/tutorials)
