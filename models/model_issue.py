from config.database import HOST, PORT, USER, PASSWORD, DATABASE
import pymysql
import datetime
import logging

utc_format = '%Y-%m-%dT%H:%M:%SZ'

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
            sql = """INSERT INTO issue(title, source, type, No, opened_time, latest_time, answered, status, author, link, content)
                             values ('%s', '%s', '%s','%s', '%s', '%s', '%s', '%s','%s', '%s')""" % (
            issue['title'], issue['source'], issue['type'], issue['id'], issue['opened_time'], issue['latest_time'], issue['answered'], issue['status'], issue['link'], issue['content'])

            try:
                self.cursor.execute(sql)
                self.db.commit()
            except:
                try:  # 插入失败表示数据库存在次issue，转为update更新
                    sql_update = """UPDATE issue SET title='%s', type='%s', opened_time='%s', latest_time='%s', answered='%s', status='%s', content='%s' WHERE No='%s'""" % (
                    issue['title'], issue['type'], issue['opened_time'], issue['latest_time'], issue['answered'], issue['status'], issue['content'], issue['id'])
                    self.cursor.execute(sql_update)
                    self.db.commit()
                    print("更新完成")
                except Exception as e:
                    logging.error("update error:%s" % e)
                    self.db.rollback()

    def save_one(self, issue):
        sql = """INSERT INTO issue(title, source, type, No, opened_time, latest_time, answered, status, author, link, content)
                                         values('%s', '%s', '%s','%s', '%s', '%s', '%s', '%s','%s' ,'%s', '%s')""" % (
            issue['title'], issue['source'], issue['type'], issue['id'], issue['opened_time'], issue['latest_time'], issue['answered'], issue['status'], issue['author'], issue['link'], issue['content'])

        try:
            self.cursor.execute(sql)
            self.db.commit()
            print("%s : Insert successfully" % issue['id'])
        except Exception as e:
            try:  # 插入失败表示数据库存在次issue，转为update更新
                print("Exception: %s" % e)
                sql_update = """UPDATE issue SET title='%s', type='%s', opened_time='%s', latest_time='%s', answered='%s', status='%s', content='%s' WHERE No='%s'""" % (
                    issue['title'], issue['type'], issue['opened_time'], issue['latest_time'], issue['answered'], issue['status'], issue['content'], issue['id'])
                self.cursor.execute(sql_update)
                self.db.commit()
                print("%s : Update successfully" % issue['id'])
            except Exception as e:
                logging.error("update error:%s" % e)
                self.db.rollback()

    # 获取对应源的issue信息
    def issue_info(self, source):
        total_count = self.get_issue_count(source)
        closed_count = self.get_issue_count(source, "status='closed'")
        select_results = self.select('issue', 'opened_time, latest_time', source, "status='closed'")



        avg_time = datetime.timedelta()

        for item in select_results:
            opened_time = datetime.datetime.strptime(item[0], utc_format)
            closed_time = datetime.datetime.strptime(item[1], utc_format)

            avg_time += (closed_time - opened_time)

        avg_time /= len(select_results)

        print('''
Issues Info of %s :
        total count: %s
        closed count: %s
        average opening time: %s
        ''' % (source, total_count, closed_count, avg_time))


    def get_issue_count(self, source, condition=""):
        return self.count(table='issue', source=source, condition=condition)


    def select(self, table, column, source, condition):
        if condition == "":
            sql = "SELECT %s FROM %s WHERE source=%s" % (column, table, source)
        else:
            sql = "SELECT %s FROM %s WHERE source=%s and %s" % (column, table, source, condition)

        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print("Error occur: %s" % e)


    def count(self, table, source, condition=""):
        if condition == "":
            sql = "SELECT count(1) FROM %s WHERE source=%s" % (table, source)
        else:
            sql = "SELECT count(1) FROM %s WHERE source=%s and %s" % (table, source, condition)
        res = 0

        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            res = result[0][0]
        except Exception as e:
            print("Error: fetch data error with message: %s" % e)

        return res