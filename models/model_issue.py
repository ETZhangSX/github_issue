from config.database import HOST, PORT, USER, PASSWORD, DATABASE
import pymysql

def save(issue_list):
    db = pymysql.Connect(
        host=HOST,
        port=PORT,
        user=USER,
        passwd=PASSWORD,
        db=DATABASE,
        charset='utf8'
    )

    cursor = db.cursor()

    for issue in issue_list:
        sql = """INSERT INTO issue(title, type, No, time, content)
                         values ('%s', '%s', '%s', '%s', '%s')""" % (issue['title'], issue['type'], issue['id'], issue['time'], issue['content'])

        try:
            cursor.execute(sql)
            db.commit()
        except:
            try:
                sql_update = """UPDATE issue SET title='%s', type='%s', time='%s', content='%s' WHERE No='%s'""" % (issue['title'], issue['type'], issue['time'], issue['content'], issue['id'])
                cursor.execute(sql_update)
                db.commit()
                print("更新完成")
            except:
                db.rollback()
                print("更新失败")
    db.close()