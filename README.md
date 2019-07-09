# GitHub Issue


## 数据表结构
* 标题 *title*
* 源 *source*
* 链接 *link*
* 类别 *type*
* 编号 *No*
* 开启时间 *opened_time*
* 最近更新时间 *latest_time*
* 评论数量 *comment_number*
* 已回答 *answered*
* 状态 *status* 
	opened或closed
* 题主 *author*
* 评论内容 *content*

	- author
	- timestamp
	- header
	- comment
---
## 爬虫过程
因为issue的详细内容与issue列表是分开的，因此爬虫过程可分为两步

### 第一步：爬取issue列表页
#### 可爬取信息
* 标题 *title*
* 链接 *link*
* 类别 *type*
* 编号 *No*
* 题主 *author*
* 开启时间 *opened_time*

#### 爬取过程
1. 获取页面
2. 解析获取页面所有issue items
3. 获取next page按钮状态，enabled获取跳转链接回到1；disabled结束爬取

### 第二步：爬取issue详情
#### 可爬取信息
* 评论内容 *content*
* 已回答 *answered*
* 状态 *status*
* 评论数量 *comment_number*
* 最近更新时间 *latest_time*


#### 爬取过程
1. 获取issue item页面
2. 解析获取所有评论信息
3. 获取下一条issue的link，回到1；没有下一条则退出

## 使用
```bash
python main.py [option]

options:
	all         # 爬取issues和pulls信息
	issues      # 爬取issues信息
	pulls       # 爬取pull requests信息
	info        # 显示issues和pulls的统计信息
	help        # 显示帮助信息
```