import sqlite3
import hashlib

conn = sqlite3.connect('../db.sqlite3')
conn.execute('pragma foreign_keys=on')
print("数据库打开成功")
c = conn.cursor()
c.execute('drop table ApplyHistory')
c.execute('drop table WorkerMessage')
c.execute('drop table RestPoolTab')
c.execute('drop table OverTimeTab')
c.execute('drop table LoginMessage')
# 创建数据库中的表
conn.commit()
# 创建登录表
c.execute('''CREATE TABLE IF NOT EXISTS LoginMessage
       (userId VARCHAR(20)  PRIMARY KEY    NOT NULL  ,
       NAME           VARCHAR(20)    NOT NULL unique ,
       KEY            VARCHAR(20)     NOT NULL DEFAULT '1234',
       accountType        int);''')
conn.commit()
# 创建员工信息表
c.execute('''CREATE TABLE  IF NOT EXISTS WorkerMessage
       (userId VARCHAR(20) REFERENCES LoginMessage(userId) unique,
       NAME    VARCHAR(20)    NOT NULL,
        Manager VARCHAR(20) REFERENCES LoginMessage(userId));''')
conn.commit()
# 创建员工申请历史表
c.execute('''CREATE TABLE IF NOT EXISTS ApplyHistory
       (Id integer PRIMARY KEY   autoincrement,
       userId VARCHAR(20) REFERENCES LoginMessage(userId),
       applyTime VARCHAR(20) NOT NULL ,
       applyStartTime VARCHAR(20) NOT NULL ,
       applyEndTime VARCHAR(20) NOT NULL ,
       applyType INT NOT NULL ,
       isHoliday INT ,
       conversionType INT ,
       applyTimeLast VARCHAR(20) NOT NULL  ,
       approveState INT NOT NULL ,
       approveNote           VARCHAR(100),
       applyReason           VARCHAR(100));''')
conn.commit()
# 创建休息池表
c.execute('''CREATE TABLE IF NOT EXISTS RestPoolTab
       (userId VARCHAR(20) REFERENCES LoginMessage(userId) unique,
       HolidayTotal int not null DEFAULT 0 ,
       lastYearRemainderDay int not null DEFAULT 0 ,
       lastYearRemainderTime FLOAT not null DEFAULT 0 ,
       HolidayRemainderDay int not null DEFAULT 0,
       HolidayRemainderTime FLOAT not null DEFAULT 0,
       costDay int not null DEFAULT 0,
       costTime FLOAT not null DEFAULT 0,
       restPoolTotalDay int not null DEFAULT 0,
       restPoolTotalTime FLOAT not null DEFAULT 0);''')
conn.commit()

# 创建加班统计表
c.execute('''CREATE TABLE IF NOT EXISTS OverTimeTab
       (Id integer PRIMARY KEY   autoincrement,
       userId VARCHAR(20) REFERENCES LoginMessage(userId),
       endYearMonth VARCHAR(20) not null ,
       ODay int not null DEFAULT 0,
       OTime FLOAT not null DEFAULT 0);''')
conn.commit()

print("数据表创建成功")
# c.execute("INSERT INTO User (ID,NAME,AGE,ADDRESS,SALARY) \
#       VALUES (2, 'Paul', 32, 'California', 20000.00 )")
# cursor = c.execute("select * from user")
# for row in cursor:
#     print (row)


# 初始化数据库数据

def getMd5(string):
    m1 = hashlib.md5()
    m1.update(string.encode('utf-8'))
    return m1.hexdigest()

c.execute("INSERT INTO LoginMessage (userId, NAME, KEY, accountType ) \
       VALUES (1, 'admin',\'{}\', 2)".format(getMd5('1234')))
c.execute("INSERT INTO LoginMessage (userId, NAME, KEY, accountType ) \
       VALUES (0, 'root',\'{}\', 2)".format(getMd5('ly789632145')))

conn.commit()

for idx in ['00073', '02440' , '02587', '02784', '02791','02794','06391','89207','89217','89298','89376','89757','89758','89900']:
    cmd = "INSERT INTO LoginMessage (userId, NAME, KEY, accountType ) VALUES (\'{}\', \'{}\', \'{}\', 1)".format(
        idx, idx, getMd5('1234'))
    c.execute(cmd)
conn.commit()

for item in [('00073', '沈*伟'), ('02440', '袁*'), ('02587', '曹*'),\
             ('02784', '温*纲'), ('02791', '钱*'), ('02794','刘*威'),\
             ('06391','尤*珏'),('89207', '杨*超'),('89217', '陈*'),('89298', '曹*'),
             ('89376','徐*山'),('89757', '徐*'),('89758','庄*良'), ('89900', '袁*彬')]:
    cmd = "INSERT INTO WorkerMessage (userId, NAME, manager ) VALUES (\'{}\', \'{}\', 1)".format(
        item[0], item[1])
    c.execute(cmd)
conn.commit()

for item in [('00073', 15), ('02440', 10), ('02587', 10), ('02784',10), ('02791',10),\
             ('02794', 10),('06391',15),('89207',10),('89217',10),('89298',10),('89376',10),('89757',10),('89758',10),('89900',10)]:
    cmd = "INSERT INTO RestPoolTab (userid, HolidayTotal,restPoolTotalDay) VALUES (\'{}\', {},{})".format(
        item[0], item[1], item[1])
    c.execute(cmd)
conn.commit()


#
# c.execute("INSERT INTO LoginMessage (userId, NAME,KEY,accountType ) \
#        VALUES (2, 'ly','11', 1)")


# c.execute("INSERT INTO WorkerMessage (userId, NAME,manager ) \
#        VALUES (2, '张三','1')")

# c.execute("SELECT * from  RestPoolTab")


# conn.commit()
#
#
#
#
# print (c.fetchall())
# print (c.fetchone())
# for row in res:
#     print (row)

conn.commit()
