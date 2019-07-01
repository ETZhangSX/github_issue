from config.database import PORT, USER, PASSWORD, HOST, DATABASE
from spiders import github_issue_spider
from models import model_issue
import pymysql

if __name__ == '__main__':
    github_tars_issue_url = 'https://github.com/TarsCloud/Tars/issues'
    print('开始爬虫...')
    print('开始爬取issue list')
    issue_list = github_issue_spider.get_issues(github_tars_issue_url)
    print('获取issue list结束，开始获取issue评论...')
    issue_detail = github_issue_spider.get_all_issues_detail(issue_list)
    print('获取评论信息完毕，正在保存到数据库...')
    print(issue_detail)
    db = pymysql.Connect(
        host=HOST,
        port=PORT,
        user=USER,
        passwd=PASSWORD,
        db=DATABASE,
        charset='utf8'
    )
    model_issue.save(issue_detail)
    # cursor = db.cursor()
    # for issue in issue_detail:
    #     sql = """INSERT INTO issue(title, type, No, time, content)
    #                  values ('%s', '%s', '%s', '%s', '%s')""" % (issue['title'], issue['type'], issue['id'], issue['time'], issue['content'])



    # try:
    #     cursor.execute(sql)
    #     db.commit()
    # except:
    #     db.rollback()
    #
    # db.close()

    # val = list()
    # for issue in issue_detail:
    #     val.append((issue['title'], issue['type'], issue['id'], issue['time'], issue['content']))
    #
    # sql = "INSERT INTO issue(title, type, No, time, content) \
    #                      values (%s, %s, %s, %s, %s)"
    #
    # try:
    #     cursor.executemany(sql, val)
    #     db.commit()
    #     print('保存完成!')
    # except:
    #     db.rollback()
    #     print('失败')
    #
    #
    # cursor.close()
    # db.close()

