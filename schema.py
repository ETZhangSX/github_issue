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

sql = """
DROP TABLE IF EXISTS `issue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `issue` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `source` varchar(45) DEFAULT NULL,
  `type` varchar(45) DEFAULT NULL,
  `No` varchar(45) NOT NULL,
  `opened_time` varchar(45) DEFAULT NULL,
  `latest_time` varchar(45) DEFAULT NULL,
  `comment_number` varchar(255) DEFAULT NULL,
  `link` varchar(255) DEFAULT NULL,
  `answered` varchar(45) NOT NULL,
  `status` varchar(45) NOT NULL,
  `author` varchar(255) NOT NULL,
  `content` mediumtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `No_UNIQUE` (`No`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `pull`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pull` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `source` varchar(45) DEFAULT NULL,
  `type` varchar(45) DEFAULT NULL,
  `No` varchar(45) NOT NULL,
  `opened_time` varchar(45) DEFAULT NULL,
  `latest_time` varchar(45) DEFAULT NULL,
  `link` varchar(255) DEFAULT NULL,
  `answered` varchar(45) NOT NULL,
  `status` varchar(45) NOT NULL,
  `author` varchar(255) NOT NULL,
  `content` mediumtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `No_UNIQUE` (`No`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;"""

try:
    cursor.execute(sql)
    db.commit()
except Exception as e:
    print("Mysql create table error: %s" % e)

db.close()
