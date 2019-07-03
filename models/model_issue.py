from config.database import HOST, PORT, USER, PASSWORD, DATABASE
import pymysql
import logging



class Issue(object):
    def __del__(self):
        self.cursor.close()
        self.db.close()

    def __init__(self, Flevel=logging.DEBUG):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        fh = logging.FileHandler(__name__)
        fh.setFormatter(fmt)
        fh.setLevel(Flevel)
        self.logger.addHandler(fh)
        try:
            self.db = pymysql.Connect(
                host=HOST,
                port=PORT,
                user=USER,
                passwd=PASSWORD,
                db=DATABASE,
                charset='utf8')
            self.cursor = self.db.cursor()
        except Exception as e:
            logging.error("Database connect error:%s" % e)

    def save_all(self, issue_list):

        for issue in issue_list:
            sql = """INSERT INTO issue(title, source, type, No, time, answered, status, author, link, content)
                             values ('%s', '%s', '%s','%s', '%s', '%s', '%s','%s', '%s')""" % (
            issue['title'], issue['source'], issue['type'], issue['id'], issue['time'], issue['answered'], issue['status'], issue['link'], issue['content'])

            try:
                self.cursor.execute(sql)
                self.db.commit()
            except:
                try:  # 插入失败表示数据库存在次issue，转为update更新
                    sql_update = """UPDATE issue SET title='%s', type='%s', time='%s', answered='%s', status='%s', content='%s' WHERE No='%s'""" % (
                    issue['title'], issue['type'], issue['time'], issue['answered'], issue['status'], issue['content'], issue['id'])
                    self.cursor.execute(sql_update)
                    self.db.commit()
                    print("更新完成")
                except Exception as e:
                    logging.error("update error:%s" % e)
                    self.db.rollback()

    def save_one(self, issue):
        sql = """INSERT INTO issue(title, source, type, No, time, answered, status, author, link, content)
                                         values ('%s', '%s', '%s','%s', '%s', '%s', '%s','%s', '%s')""" % (
            issue['title'], issue['source'], issue['type'], issue['id'], issue['time'], issue['answered'], issue['status'], issue['link'], issue['content'])

        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            try:  # 插入失败表示数据库存在次issue，转为update更新
                sql_update = """UPDATE issue SET title='%s', type='%s', time='%s', answered='%s', status='%s', content='%s' WHERE No='%s'""" % (
                    issue['title'], issue['type'], issue['time'], issue['answered'], issue['status'], issue['content'], issue['id'])
                self.cursor.execute(sql_update)
                self.db.commit()
                print("更新完成")
            except Exception as e:
                logging.error("update error:%s" % e)
                self.db.rollback()