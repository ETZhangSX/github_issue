# GitHub Issue


## 数据表结构
* 标题 *title*
* 链接 *link*
* 类别 *type*
* 编号 *No*
* 时间 *time*
* 评论内容 *content*

---
## 爬虫过程
因为issue的详细内容与issue列表是分开的，因此爬虫过程可分为两步

### 第一步：爬取issue列表页
#### 可爬取信息
* 标题 *title*
* 链接 *link*
* 类别 *type*
* 编号 *No*
* 发布时间 *time*

#### 爬取过程
1. 获取页面
2. 解析获取页面所有issue items
3. 获取next page按钮状态，enabled获取跳转链接回到1；disabled结束爬取

### 第二步：爬取issue详情
#### 可爬取信息
* 评论内容 *content*

#### 爬取过程
1. 获取issue item页面
2. 解析获取所有评论信息
3. 获取下一条issue的link，回到1；没有下一条则退出