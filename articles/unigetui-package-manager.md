# UniGetUI 让你用图形界面一键批量安装和更新 Windows 里的所有软件

[网站全文](https://aronshare.com/posts/unigetui-package-manager/)

![Aron 封面](https://aronshare.com/covers/cover_unigetui-package-manager.webp)


## UniGetUI 是什么

在 Windows 电脑上装软件或升级旧版本时，普通用户往往要挨个去官网找安装包，稍不留神还会下到捆绑推广软件；而虽然微软自带了 `Winget` 命令行包管理器，社区也有 `Scoop` 和 `Chocolatey`，但每次都要敲命令行记参数依然不够直观。

UniGetUI（原名 WingetUI）是一款专门为 Windows 常用命令行包管理器打造的开源图形界面工具。它把 `Winget`、`Scoop`、`Chocolatey`、`Pip`、`Npm`、`Cargo` 和 `.NET Tool` 全部整合进同一个原生窗口里，无需记忆任何终端指令，就能像使用应用商店一样搜索、安装、升级和卸载电脑上的几乎所有软件。

![UniGetUI 深色模式下聚合搜索与安装各类 Windows 软件包界面](https://aronshare.com/assets/post-images/unigetui-package-manager-detail-1.webp)

## 它可以解决哪些日常痛点

- **把主流包管理器聚合成一个无广告软件库**：在一个搜索框里同时检索 Winget 官方源、Scoop 便携源与开发工具包，点击勾选即可批量静默安装，彻底告别去各个下载站找安装包的繁琐。
- **后台自动检测更新与一键全量升级**：支持系统托盘常驻检测电脑上所有已安装软件的新版本，弹窗提醒后点一下即可后台静默更新，也支持把某个不想升级的软件加入忽略黑名单。
- **重装系统前一键导出软件配置包**：内置「软件包束（Package Bundles）」导出与导入功能，换新电脑或重装系统时，只需导入之前保存的列表文件，就能自动把几十个常用软件一次性装回原位。
- **精细控制安装路径与管理员权限**：在安装单个软件前，可以直接在界面上自定义目标安装文件夹、开启静默安装参数、校验安装包 SHA256 哈希或指定以管理员权限运行。

![UniGetUI 浅色模式下检查已安装软件版本与批量更新列表](https://aronshare.com/assets/post-images/unigetui-package-manager-detail-2.webp)

## 安装与使用建议

1. 可以直接通过页面上方提供的夸克网盘或迅雷网盘获取打包好的安装程序，解压后直接运行安装向导即可完成部署。
2. 首次启动后，点击左侧导航栏的「发现软件包（Discover Packages）」，输入软件名称即可看到来自不同源的版本对比；日常普通办公软件建议优先选择 `Winget` 来源，免安装便携工具则推荐选择 `Scoop` 来源。
3. 建议进入「设置 -> 更新通知」开启后台自动检查更新，并将自己平时习惯固定版本的生产力工具右键设为「忽略此软件的更新」，兼顾安全补丁与工作流稳定。

## 核实来源

- 官方网站：https://www.marticliment.com/unigetui/
- GitHub 仓库：https://github.com/marticliment/WingetUI
