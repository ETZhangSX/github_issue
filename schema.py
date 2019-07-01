import pymysql
from config.database import HOST, PORT, PASSWORD, USER, DATABASE


'''
数据库迁移脚本，一键建表
'''

db = pymysql.Connect(
    host=HOST,
    port=PORT,
    user=USER,
    passwd=PASSWORD,
    db=DATABASE,
    charset='utf8'
)

cursor = db.cursor()

sql = """CREATE TABLE IF NOT EXISTS issue(
         id INT(11) NOT NULL AUTO_INCREMENT,
         title CHAR(255),
         type CHAR(18),
         No CHAR(11) NOT NULL unique,
         time CHAR(18) ,
         content mediumtext,
         PRIMARY KEY (`id`),
         UNIQUE KEY `No_UNIQUE` (`No`))"""

cursor.execute(sql)

db.close()