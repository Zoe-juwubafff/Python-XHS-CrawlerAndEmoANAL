# 基于Python-爬取小红书搜索关键词下面的所有笔记的内容、点赞数量、评论数量等数据，绘制词云图、词频分析、情感分析等
## 上手指南：以下指南将帮助你在本地机器上安装和运行该项目，进行开发和测试。关于如何将该项目部署到在线环境，请参考部署小节
## 环境配置步骤----安装NodeJS----配置Python解释器（3.8）----安装所需的库
### 1.NodeJS
### NodeJS下载地址：https://nodejs.org/zh-cn/download/ （根据自己的计算机系统、配置选择对应的版本）
### 下载NodeJS后按照指引安装即可，安装完成后记得配置系统环境变量
### 我这里使用pycharm专业版（必须专业版）配置nodejs环境
### file-setting-plugin-marketplace
### 搜索nodejs，我的显示已经安装过
### 如果没有安装过，直接点击install即可
### ![image](https://github.com/Zoe-juwubafff/BAES-Python-XHS-CrawlerAndEmoANAL/assets/90123940/1dc81454-bdd3-40d4-8704-0b8b67b498f8)
### 接着点击如下图框选的内容
### ![image](https://github.com/Zoe-juwubafff/BAES-Python-XHS-CrawlerAndEmoANAL/assets/90123940/b9ea2f44-7488-48c6-bb3e-631f15fedc97)
### 选择本地安装nodejs的路径
### ![image](https://github.com/Zoe-juwubafff/BAES-Python-XHS-CrawlerAndEmoANAL/assets/90123940/b62c6bd4-4dec-4f3a-ba91-50076cf97724)
### 至此，nodejs配置完成

### 2.Python解释器要求
#### 本人测试使用的为3.8版本无任何问题，测试过3.11会有一些小问题，建议版本为3.8~3.9

### 3.运行所需的库
    pip install -r requirements.txt
##主要代码说明
小红书关键词爬虫.py----根据关键词爬虫小红书笔记
爬虫数据的情感分析.py----根据爬虫所得到的数据对此关键词内容的情绪判断并反馈
## 运行步骤
小红书关键词爬虫.py————>爬虫数据的情感分析.py
## 重点（windows电脑请忽略）：mac电脑绘制词云图的时候，数据分析代码中，注释或者删除上面一行代码，解除注释下面一行代码（删除前面的 ＃ 解除注释），如下图：![image](https://github.com/Zoe-juwubafff/BAES-Python-XHS-CrawlerAndEmoANAL/assets/90123940/6438b4a0-9fbb-4967-8283-6eb3be548fea)

##Q&A总结
###一个关键词能爬取多少数据？
一个关键词只能吧取220条笔记内容，也就是11页，这是小红书的限制(在网页上搜素一个关键词，然后往下翻，就会发现在翻了11页后会触底)。
###遇见直接显示爬取完毕的情况，如下图，应该怎么解决？
![3ad0ccc1c09fdecf6b76170a8be9e77](https://github.com/user-attachments/assets/ecdec8f3-4870-4c06-bd2f-0391856e511e)
如果遇到这种情况，只能通过更换cookie解决(只用更换一次，成功了就不用换了关键词就更换，等下次再出现这种情况再换)，必须登录xhs账号，并且登录过后重新打开浏览器，再更换cookie
###運见所有笔记都不允许查看，下面图片所示
![1720859171226](https://github.com/user-attachments/assets/e581a872-9c29-499a-92cc-eb81f11faefa)
这种情况是因为没有获取正确的cookie。解决方法:用手机验证码重新登录账号，再换cookie，不行的话更换网络，再换cookie，或者更换浏览器，重新登录，再换cookie。

# Contributing

When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the owners of this repository before making a change. 

Please note we have a code of conduct, please follow it in all your interactions with the project.

## Pull Request Process

1. Ensure any install or build dependencies are removed before the end of the layer when doing a 
   build.
2. Update the README.md with details of changes to the interface, this includes new environment 
   variables, exposed ports, useful file locations and container parameters.
3. Increase the version numbers in any examples files and the README.md to the new version that this
   Pull Request would represent. The versioning scheme we use is [SemVer](http://semver.org/).
4. You may merge the Pull Request in once you have the sign-off of two other developers, or if you 
   do not have permission to do that, you may request the second reviewer to merge it for you.

## Code of Conduct

### Our Pledge

In the interest of fostering an open and welcoming environment, we as
contributors and maintainers pledge to making participation in our project and
our community a harassment-free experience for everyone, regardless of age, body
size, disability, ethnicity, gender identity and expression, level of experience,
nationality, personal appearance, race, religion, or sexual identity and
orientation.

### Our Standards

Examples of behavior that contributes to creating a positive environment
include:

* Using welcoming and inclusive language
* Being respectful of differing viewpoints and experiences
* Gracefully accepting constructive criticism
* Focusing on what is best for the community
* Showing empathy towards other community members

Examples of unacceptable behavior by participants include:

* The use of sexualized language or imagery and unwelcome sexual attention or
advances
* Trolling, insulting/derogatory comments, and personal or political attacks
* Public or private harassment
* Publishing others' private information, such as a physical or electronic
  address, without explicit permission
* Other conduct which could reasonably be considered inappropriate in a
  professional setting

### Our Responsibilities

Project maintainers are responsible for clarifying the standards of acceptable
behavior and are expected to take appropriate and fair corrective action in
response to any instances of unacceptable behavior.

Project maintainers have the right and responsibility to remove, edit, or
reject comments, commits, code, wiki edits, issues, and other contributions
that are not aligned to this Code of Conduct, or to ban temporarily or
permanently any contributor for other behaviors that they deem inappropriate,
threatening, offensive, or harmful.

### Scope

This Code of Conduct applies both within project spaces and in public spaces
when an individual is representing the project or its community. Examples of
representing a project or community include using an official project e-mail
address, posting via an official social media account, or acting as an appointed
representative at an online or offline event. Representation of a project may be
further defined and clarified by project maintainers.

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be
reported by contacting the project team at [INSERT EMAIL ADDRESS]. All
complaints will be reviewed and investigated and will result in a response that
is deemed necessary and appropriate to the circumstances. The project team is
obligated to maintain confidentiality with regard to the reporter of an incident.
Further details of specific enforcement policies may be posted separately.

Project maintainers who do not follow or enforce the Code of Conduct in good
faith may face temporary or permanent repercussions as determined by other
members of the project's leadership.

### Attribution

This Code of Conduct is adapted from the [Contributor Covenant][homepage], version 1.4,
available at [http://contributor-covenant.org/version/1/4][version]

[homepage]: http://contributor-covenant.org
[version]: http://contributor-covenant.org/version/1/4/

### 作者
### 作者：juwubafff
