from config.database import HOST, PORT, USER, PASSWORD, DATABASE
import pymysql

db = pymysql.Connect(
        host=HOST,
        port=PORT,
        user=USER,
        passwd=PASSWORD,
        db=DATABASE,
        charset='utf8'
)