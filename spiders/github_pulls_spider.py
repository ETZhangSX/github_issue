import logging
import re
import requests
import json
import pickle
from pyquery import PyQuery
from urllib.parse import urljoin, urlparse
from models.model_pull import Pull

# 获取html页面文本
def get_url_page(url):
    response = requests.get(url)
    logging.info(response.status_code)

    if response.status_code == 200:
        return response.text


# 解析issue页，爬取页面的issue列表
def parse_pull_page(html, url, status):
    # 用于存储所有issue信息
    pull_list_per_page = list()

    # 实例化PyQuery对象
    document = PyQuery(html)

    # 过滤获取issue所有标签
    pull_all = document('div').filter('.js-issue-row')

    # items() 转化为list
    pull_items = pull_all.items()

    # 获取每一个issue
    for item in pull_items:
        head = item('a').filter('.h4')
        # issue信息项
        id     = re.findall(r"\d+", item.attr('id'))[0]
        title  = head.text()
        type   = item('.IssueLabel').text()
        link   = urljoin(url, head.attr('href'))
        time   = item('.opened-by relative-time').attr('datetime')
        author = item('.opened-by a').text()
        # 没有添加标签的类别，使用default代替
        if type == '':
            type = 'default'

        path = urlparse(url).path.split('/')[2]
        # 使用json类型保存
        item_info = {
            'id'         :  path + "#" + id,
            'source'     :  path,
            'title'      :  title.replace("'", "''"),
            'type'       :  type,
            'link'       :  link,
            'answered'   :  'no',
            'status'     :  status,
            'latest_time':  time,
            'author'     :  author,
            'content'    :  ''
        }
        pull_list_per_page.append(item_info)

    logging.info(pull_list_per_page)

    # 下一页链接
    next_page_link = document('.next_page').attr('href')
    logging.info(next_page_link)

    # 判断下一页链接是否disabled
    if next_page_link != None:
        next_page_link = urljoin(url, next_page_link)

    return pull_list_per_page, next_page_link


# 循环获取所有issue页面获取所有issue项, 返回issue list
def get_pulls(url):
    html = get_url_page(url)
    pull_list, next_page = parse_pull_page(html, url, 'opened')

    while next_page != None:
        html = get_url_page(next_page)
        pull_list_per_page, next_page = parse_pull_page(html, url, 'opened')
        pull_list += pull_list_per_page

    document = PyQuery(html)
    closed_url = urljoin(url, document('#js-issues-toolbar .table-list-header-toggle.states a').not_('.selected').attr('href'))

    # 爬取已关闭的issue
    html = get_url_page(closed_url)
    temp_list, next_page = parse_pull_page(html, closed_url, 'closed')

    pull_list += temp_list

    while next_page != None:
        html = get_url_page(next_page)
        pull_list_per_page, next_page = parse_pull_page(html, closed_url, 'closed')
        pull_list += pull_list_per_page


    logging.info(pull_list)
    return pull_list


# 获取单个issue的详情页评论信息
def get_pull_detail(pull_url):
    answered = 'no'
    html = get_url_page(pull_url)

    document = PyQuery(html)
    # 获取该PR状态
    status = document('#partial-discussion-header .State').attr('title').split(' ')[1]

    # 获取PR提交者
    pull_author = document('.TableObject-item.TableObject-item--primary .author.text-bold.link-gray').text()

    timeline = list()
    comments = document('.timeline-comment').items()


    for comment in comments:
        author = comment('a').filter('.author').text()
        header = comment('.timeline-comment-header').text().replace("'", "''")
        timestamp = comment('.timeline-comment-header h3 a').children('relative-time').attr('datetime')
        comment_text = comment('table').text()

        comment_item = {
            'author'    : author,
            'header'    : header,
            'timestamp' : timestamp,
            'comment'   : comment_text
        }

        timeline.append(comment_item)

        if author != pull_author:
            answered = 'yes'

    closed_time = str()
    if 'Merged' == status:
        closed_time = document('#partial-discussion-header .TableObject-item--primary relative-time').attr('datetime')
    elif 'Closed' == status:
        closed_time = document('.discussion-item-closed relative-time').attr('datetime')

    comment_item = {
        'author': pull_author,
        'header': "Record Merged or Closed time",
        'timestamp': closed_time,
    }
    timeline.append(comment_item)

    logging.info(timeline)
    return timeline, answered, status


# 获取所有issue评论信息
def get_all_pulls_detail(pull_list):
    pull_db = Pull()
    for pull in pull_list:
        timeline, answered, status = get_pull_detail(pull['link'])
        opened_time = timeline[0]['timestamp']
        if pull['status'] != 'closed':
            pull['latest_time'] = timeline[-1]['timestamp']
        pull['opened_time'] = opened_time
        pull['answered'] = answered
        pull['status'] = status
        # pull['content'] = pickle.dumps(timeline)
        # print(issue)
        pull_db.save_one(pull)

    logging.info(pull_list)
    return pull_list
