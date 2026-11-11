# DocuSeal 发合同给对方签，签名文件留在自己服务器上

> 💡 **资源说明**：本文档为精选摘要镜像，完整工具介绍、官方入口与使用条件请前往 AronShare 官网浏览。

[![封面图片](https://aronshare.com/covers/cover_docuseal-document-signing.webp)](https://aronshare.com/posts/docuseal-document-signing/)

签一份合同，多数人现在的做法是：把 PDF 发过去，让对方打印、签字、拍照、回传。

来回两轮以后，你手上是几张角度歪掉的照片，甲方那边说「我签过了」，真出问题时谁也证明不了什么。

DocuSeal 把这套流程搬到浏览器里。它是开源的电子签与 PDF 表单平台，AGPLv3 加一项 7(b) 附加条款，自托管一条 docker run 就能起。

用法是先把字段摆到文档上。

打开构建器，左边是你的 PDF，可以直接把 Text、Signature、Date、Image、File、Select、Checkbox、Cells、Multiple、Radio 这些字段拖到指定位置。

![](https://aronshare.com/assets/post-images/docuseal-document-signing/detail-1.webp)

右边是收件人清单和字段归属，图上这个人叫 First Submitter，分配给她的字段有姓名、日期、照片和签名，签名这一项勾了 Required，也就是不签不能提交。

一份文档可以配多个签署人，各自只填自己那一部分，先后顺序能设，第二个签署人收到通知时第一个已经签完了。

对方点开链接看到的是下面这样。

![](https://aronshare.com/assets/post-images/docuseal-document-signing/detail-2.webp)

页面干净到只有标题、签名区和提交按钮，手机上也一样，手指在屏幕上签，签完点 SUBMIT，底部的进度点告诉他还剩几步。

签完的文件带电子签名，平台能做 PDF 签名验证，用来确认这份文件在签署之后没有被改过。这一点对合同来说比界面好看重要得多。

12 种字段类型覆盖了大多数场景：签名、日期、文件、复选框，还有单选和表格单元，报价单、入职表、验收单都能拼出来。

部署这块给得比较松。

容器默认用 SQLite 存数据，单机试用不用额外准备数据库；要上生产就把 DATABASE_URL 指到 PostgreSQL 或 MySQL。

文件存储可以放本机磁盘，也可以接 AWS S3、Google Storage、Azure 云存储。

邮件通知走自建 SMTP，发信服务器要自己准备，域名验证和发信信誉自己处理。

界面给了 7 种语言，签署流程支持 14 种语言，发给海外客户时不用另做一版。

代价说清楚。

白标去 Logo、用户角色、短信身份验证、条件字段与公式、SSO 和 SAML、CSV 批量发送这些都在 Pro 付费档，自托管免费版用不了。

它把附加条款写进了许可证文件，商用前要同时看 LICENSE 和 LICENSE_ADDITIONAL_TERMS 两份，别只看开头那行 AGPLv3 就动手。

签名的法律效力取决于你所在地区的电子签名法规，以及你们双方对签署方式的约定，工具只负责流程和留痕。

谁适合用：经常发合同、报价单、验收单的自由职业者和小团队；客户在海外、签名要跨时区的；不愿意把合同文件放在第三方 SaaS 上的。

谁别碰：一年签不到五份文件、客户还都在本地的，纸质打印比学一套系统快。

官网 docuseal.com，源码在 github.com/docusealco/docuseal，on-premises 页面给了自托管部署的说明和镜像入口。

---

### 📖 完整介绍与官方入口

完整文章保留官方资料来源、适用场景及版本和费用条件，下载方式以文章中的实际入口为准。

👉 **[点击前往 AronShare 官网阅读全文](https://aronshare.com/posts/docuseal-document-signing/)**
