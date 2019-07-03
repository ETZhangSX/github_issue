from spiders import github_issue_spider
from models.model_issue import Issue

if __name__ == '__main__':
    github_tars_issue_url = 'https://github.com/TarsCloud/Tars/issues'
    print('开始爬虫...')
    print('开始爬取issue list')
    issue_list = github_issue_spider.get_issues(github_tars_issue_url)
    print('获取issue list结束，开始获取issue评论...')
    issue_detail = github_issue_spider.get_all_issues_detail(issue_list)
    print('获取issue评论信息完毕')
    # issue = Issue()
    # issue.save_all(issue_detail)

