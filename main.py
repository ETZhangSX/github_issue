# -*- coding: UTF-8 -*-
import sys
from urllib.parse import urlparse
from spiders import github_issues_spider, github_pulls_spider
from models.model_issue import Issue
from models.model_pull import Pull

github_source_url = [
            'https://github.com/TarsCloud/Tars',
            'https://github.com/TarsCloud/TarsDocker',
            'https://github.com/TarsCloud/TarsWeb',
            'https://github.com/TarsCloud/TarsCpp',
            'https://github.com/TarsCloud/TarsJava',
            'https://github.com/TarsCloud/TarsGo',
            'https://github.com/TarsCloud/TarsFramework',
            'https://github.com/TarsCloud/TarsProtocol',
            'https://github.com/TarsCloud/TarsTup',
            'https://github.com/TarsCloud/tars-unittest',
            'https://github.com/TarsCloud/plugins',
            'https://github.com/Tencent/TSeer',
            'https://github.com/Tencent/DCache',
]

def do():
    if len(sys.argv) == 1:
        help()
        return

    param = sys.argv[1]

    if "all" == param:
        crawl_and_scrape('issues')
        crawl_and_scrape('pulls')

    elif "issues" == param:
        crawl_and_scrape('issues')

    elif "pulls" == param:
        crawl_and_scrape('pulls')

    elif "info" == param:
        get_info()
        # issue = Issue()
        # for url in github_source_url:
        #     issue.issue_info("'%s'" % urlparse(url).path.split('/')[2])
    elif "help" == param:
        help()



def help():
    helpMsg = '''usage: python main.py [option]

Select an option parameter to run:
    all     : Get issues and pull requests from github
    issues  : Get issues from github
    pulls   : Get pull requests from github
    info    : Get data info
    help    : For help
    '''
    print(helpMsg)
    return


def crawl_and_scrape(part):
    if 'issues' == part:
        for source in github_source_url:
            url = source + "/" + part
            print('开始爬取%s list: %s' % (part, url))
            issue_list = github_issues_spider.get_issues(url)
            print('获取list结束，开始获取%s评论...' % part)
            issue_detail = github_issues_spider.get_all_issues_detail(issue_list)
            print('获取%s评论信息完毕' % part)

    elif 'pulls' == part:
        for source in github_source_url:
            url = source + "/" + part
            print('开始爬取%s list: %s' % (part, url))
            pull_list = github_pulls_spider.get_pulls(url)
            print('获取list结束，开始获取%s评论...' % part)
            pull_detail = github_pulls_spider.get_all_pulls_detail(pull_list)
            print('获取%s评论信息完毕' % part)


def get_info():
    issue = Issue()
    pull = Pull()
    issue_info = str()
    pulls_info = str()
    for url in github_source_url:
        issue_info += issue.issue_info("'%s'" % urlparse(url).path.split('/')[2]) + "\n\n"
        pulls_info += pull.pull_info("'%s'" % urlparse(url).path.split('/')[2]) + "\n\n"
    with open("issue_info.txt", "wt") as f:
        f.write(issue_info)
    with open("pulls_info.txt", "wt") as f:
        f.write(pulls_info)
    print("Get info successfully!")

if __name__ == '__main__':
    do()
    pass


    # else:
    #     paramError()
    #     return
    # return


    # issue = Issue()
    # res = issue.count('issue', "status='closed'")

    # issue.save_all(issue_detail)

