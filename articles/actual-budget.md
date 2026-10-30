# Actual Budget 帮你把账户流水整理成看得懂的日常预算

收录日期：2026-10-30

[在 AronShare 阅读](https://aronshare.com/posts/actual-budget/)

![Actual Budget 帮你把账户流水整理成看得懂的日常预算](https://aronshare.com/covers/cover_actual-budget.webp)


账户流水记录了每笔支出，却很难直接回答餐饮、交通和订阅分别花了多少。
每个月都手动复制表格，分类方式又容易前后不一致。
[Actual Budget](https://actualbudget.org/)提供账户、交易和分类预算界面，适合想持续整理日常收支、同时掌握数据存放位置的人。

## 分类预算和交易记录可以放在一起查看

Actual Budget 采用信封式预算思路，围绕已经拥有的资金安排分类，在界面里对照预算金额、实际支出和剩余额度。
[官网](https://actualbudget.org/)还介绍了拆分交易、账户转账，以及现金流和自定义报表等功能。
这些工具让一笔跨多个用途的付款能够分开记录，也方便按同一套分类查看不同时段。

使用时可以围绕自己的记账问题建立分类，例如区分食品采购和外出就餐，避免所有支出都进入同一栏。
分类数量适合保持在能持续维护的范围，名称也应尽量稳定，方便比较每个月的记录。

![Actual Budget 官方预算界面展示账户列表和多月分类预算](https://aronshare.com/assets/post-images/actual-budget-official-ui.webp)

*图片来自 Actual Budget 官网，展示产品预算界面，图中数值为官方展示内容。*

## 不连接银行也能导入流水

[交易导入文档](https://actualbudget.org/docs/transactions/importing/)支持 CSV、QIF、OFX、QFX 和 CAMT 文件，也允许手动录入交易。
导入 CSV 时，可以映射日期、金额等字段，调整日期格式和分隔符，并处理收入支出分列的情况。
这适合能够下载账单文件、但不想配置银行连接的使用方式。

每次导入都值得核对账户、日期范围和金额方向，避免把支出识别成收入。
Actual 会尝试识别重复交易，官方指出 OFX/QFX 携带的交易标识更有利于匹配。
保留原始导出文件，也方便发现异常时回头检查来源。

## 本地使用和多设备同步有不同条件

根据[官方仓库](https://github.com/actualbudget/actual)，项目提供 Windows、macOS 和 Linux 桌面应用，也能通过 Docker 部署服务。
[同步文档](https://actualbudget.org/docs/getting-started/sync/)说明，数据会保存在本地设备，连接选定的服务器后可以在设备之间同步修改。
网络暂时不可用时仍能继续使用本地数据，跨设备更新则需要恢复连接。

可选的端到端加密需要单独启用，并使用加密密码保护同步的预算数据。
本地设备上的数据仍需依靠设备自身的保护措施；如果本地副本丢失、加密密码也遗忘，恢复数据会受到限制。
因此，选择加密时也要安排密码保管和独立备份。

## 银行同步需要核对服务覆盖和数据边界

[银行连接说明](https://actualbudget.org/docs/advanced/bank-sync/)要求运行 actual-server，并向所选服务商申请连接凭据。
支持的服务分别面向不同地区，能否连接自己的银行需要按服务商和账户条件确认，服务费用也应单独查看。
文件导入与手工记录可以作为不接银行服务的入口。

银行连接令牌存放在服务器上，未被预算数据的端到端加密覆盖，有数据库访问权限的管理员或托管方可能读取这些令牌。
预算同步和银行连接涉及不同的数据边界，决定是否接入时要分别考虑。

## 部署费用主要来自运行环境

Actual Budget 在[官方仓库](https://github.com/actualbudget/actual)明确为免费开源软件，采用 MIT 许可。
自己运行需要准备设备、存储和维护，也可以选择官网列出的第三方付费托管方式，具体费用按所选服务确认。

[Docker 文档](https://actualbudget.org/docs/install/docker/)提供官方镜像和 Compose 配置，示例使用 5006 端口，将持久化数据放在容器的 `/data` 目录。
配置数据挂载后启动服务，升级时保留这份数据并安排备份，比单纯记住启动命令更重要。

可以建立一个试用账本，导入一小段流水，检查字段识别、分类和查询是否顺手。
确认记录方式适合自己后，逐步扩大管理范围，让日常记账维持在能够持续完成的程度。

- [访问官网与演示入口](https://actualbudget.org/)
- [查看源码和桌面应用入口](https://github.com/actualbudget/actual)
- [阅读 Docker 部署说明](https://actualbudget.org/docs/install/docker/)
