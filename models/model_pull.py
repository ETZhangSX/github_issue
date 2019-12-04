from config.database import HOST, PORT, USER, PASSWORD, DATABASE
import pymysql
import datetime
import logging

utc_format = '%Y-%m-%dT%H:%M:%SZ'

class Pull(object):
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


    def save_all(self, pull_list):
        for pull in pull_list:
            sql = """INSERT INTO pull(title, source, type, No, opened_time, latest_time, answered, status, author, link, content)
                             values ('%s', '%s', '%s','%s', '%s', '%s', '%s', '%s','%s', '%s')""" % (
            pull['title'], pull['source'], pull['type'], pull['id'], pull['opened_time'], pull['latest_time'], pull['answered'], pull['status'], pull['link'], pull['content'])

            try:
                self.cursor.execute(sql)
                self.db.commit()
            except:
                try:  # 插入失败表示数据库存在次pull，转为update更新
                    sql_update = """UPDATE pull SET title='%s', type='%s', opened_time='%s', latest_time='%s', answered='%s', status='%s', content='%s' WHERE No='%s'""" % (
                    pull['title'], pull['type'], pull['opened_time'], pull['latest_time'], pull['answered'], pull['status'], pull['content'], pull['id'])
                    self.cursor.execute(sql_update)
                    self.db.commit()
                    print("更新完成")
                except Exception as e:
                    logging.error("update error:%s" % e)
                    self.db.rollback()

    def save_one(self, pull):
        sql = """INSERT INTO pull(title, source, type, No, opened_time, latest_time, answered, status, author, link, content)
                                         values('%s', '%s', '%s','%s', '%s', '%s', '%s', '%s','%s' ,'%s', '%s')""" % (
            pull['title'], pull['source'], pull['type'], pull['id'], pull['opened_time'], pull['latest_time'], pull['answered'], pull['status'], pull['author'], pull['link'], pull['content'])

        try:
            self.cursor.execute(sql)
            self.db.commit()
            print("%s : Insert successfully" % pull['id'])
        except Exception as e:
            try:  # 插入失败表示数据库存在次pull，转为update更新
                print("Exception: %s" % e)
                sql_update = """UPDATE pull SET title='%s', type='%s', opened_time='%s', latest_time='%s', answered='%s', status='%s', content='%s' WHERE No='%s'""" % (
                    pull['title'], pull['type'], pull['opened_time'], pull['latest_time'], pull['answered'], pull['status'], pull['content'], pull['id'])
                self.cursor.execute(sql_update)
                self.db.commit()
                print("%s : Update successfully" % pull['id'])
            except Exception as e:
                logging.error("update error:%s" % e)
                self.db.rollback()

    # 获取对应源的pull信息
    def pull_info(self, source):
        total_count = self.get_pull_count(source)
        closed_count = self.get_pull_count(source, "status='Closed'")
        opened_count = self.get_pull_count(source, "status='Open'")
        merged_count = self.get_pull_count(source, "status='Merged'")

        select_closed = self.select('pull', 'opened_time, latest_time', source, "status='Closed'")
        select_merged = self.select('pull', 'opened_time, latest_time', source, "status='Merged'")


        avg_time = datetime.timedelta()
        avg_time_merged = datetime.timedelta()

        for item in select_closed:
            opened_time = datetime.datetime.strptime(item[0], utc_format)
            closed_time = datetime.datetime.strptime(item[1], utc_format)

            avg_time += (closed_time - opened_time)

        for item in select_merged:
            opened_time = datetime.datetime.strptime(item[0], utc_format)
            closed_time = datetime.datetime.strptime(item[1], utc_format)
            temp = (closed_time - opened_time)
            avg_time += temp
            avg_time_merged += temp

        closed_len = (len(select_closed) + len(select_merged))
        merged_len = len(select_merged)

        if 0 == closed_len:
            avg_time = 0
        else:
            avg_time /= closed_len

        if 0 == merged_len:
            avg_time_merged = 0
        else:
            avg_time_merged /= merged_len


        return '''pulls Info of %s :
        Total count: %s
        Closed count: %s
        Opened count: %s
        Merged count: %s
        Average opening time: %s
        Average opening time(Merged): %s
        ''' % (source, total_count, closed_count, opened_count, merged_count, avg_time, avg_time_merged)


    def get_pull_count(self, source, condition=""):
        return self.count(table='pull', source=source, condition=condition)


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