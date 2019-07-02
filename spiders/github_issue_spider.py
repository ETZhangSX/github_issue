import logging
import re
import requests
import json
from pyquery import PyQuery
from urllib.parse import urljoin
from models.model_issue import Issue

# 获取html页面文本
def get_url_page(url):
    response = requests.get(url)
    logging.info(response.status_code)

    if response.status_code == 200:
        return response.text


# 解析issue页，爬取页面的issue列表
def parse_issue_page(html, url):
    # 用于存储所有issue信息
    issue_list_per_page = list()

    # 实例化PyQuery对象
    document = PyQuery(html)

    # 过滤获取issue所有标签
    issue_all = document('div').filter('.js-issue-row')

    # items() 转化为list
    issue_items = issue_all.items()


    # 获取每一个issue
    for item in issue_items:
        head = item('a').filter('.h4')

        # issue信息项
        id    = re.findall(r"\d+", item.attr('id'))[0]
        title = head.text()
        type  = item('.IssueLabel').text()
        link  = urljoin(url, head.attr('href'))
        time  = item('span').filter('.opened-by').children('relative-time').attr('datetime')

        # 没有添加标签的类别，使用default代替
        if type == '':
            type = 'default'

        # 使用json类型保存
        item_info = {
            'id'      :  id,
            'title'   :  title,
            'type'    :  type,
            'link'    :  link,
            'time'    :  time,
            'content' :  ''
        }
        issue_list_per_page.append(item_info)

    logging.info(issue_list_per_page)

    # 下一页链接
    next_page_link = document('.next_page').attr('href')
    logging.info(next_page_link)

    # 判断下一页链接是否disabled
    if next_page_link != None:
        next_page_link = urljoin(url, next_page_link)

    return issue_list_per_page, next_page_link


# 循环获取所有issue页面获取所有issue项, 返回issue list
def get_issues(url):
    html = get_url_page(url)
    issue_list, next_page = parse_issue_page(html, url)

    while next_page != None:
        html = get_url_page(next_page)
        issue_list_per_page, next_page = parse_issue_page(html, url)
        issue_list += issue_list_per_page

    logging.info(issue_list)
    # print(issue_list)
    return issue_list


# 获取单个issue的详情页评论信息
def get_issue_detail(issue_url):
    html = get_url_page(issue_url)
    document = PyQuery(html)

    timeline = list()
    comments = document('.timeline-comment').items()

    for comment in comments:
        header = comment('.timeline-comment-header').text()
        comment_text = comment('table').text()
        comment_item = {
            'header' : header,
            'comment': comment_text
        }
        timeline.append(comment_item)

    logging.info(timeline)
    return timeline


# 获取所有issue评论信息
def get_all_issues_detail(issue_list):
    issue_db = Issue()
    for issue in issue_list:
        timeline = get_issue_detail(issue['link'])
        issue['content'] = json.dumps(timeline, ensure_ascii=False)
        print(issue)
        issue_db.save_one(issue)
    logging.info(issue_list)
    return issue_list
