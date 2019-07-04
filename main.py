import sys
from urllib.parse import urlparse
from spiders import github_issue_spider
from models.model_issue import Issue

github_issue_url = [
            'https://github.com/TarsCloud/Tars/issues',
            'https://github.com/Tencent/TSeer/issues',
            'https://github.com/Tencent/DCache/issues',
]

def help():
    helpMsg = '''This
    '''
    print(helpMsg)
    return

if __name__ == '__main__':
    # if len(sys.argv) == 1:
    #     help()
    #     return
    param = sys.argv[1]
    if "spider" == param:

        print('开始爬虫...')
        for url in github_issue_url:
            print('开始爬取issue list: %s' % url)
            issue_list = github_issue_spider.get_issues(url)
            print('获取issue list结束，开始获取issue评论...')
            issue_detail = github_issue_spider.get_all_issues_detail(issue_list)
            print('获取issue评论信息完毕')

    elif "info" == param:
        issue = Issue()
        for url in github_issue_url:
            issue.issue_info("'%s'" % urlparse(url).path.split('/')[2])


    # else:
    #     paramError()
    #     return
    # return


    # issue = Issue()
    # res = issue.count('issue', "status='closed'")

    # issue.save_all(issue_detail)

