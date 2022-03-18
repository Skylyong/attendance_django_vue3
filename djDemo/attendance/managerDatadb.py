import sqlite3

conn = sqlite3.connect('../db.sqlite3')
conn.execute('pragma foreign_keys=on')
print("数据库打开成功")
c = conn.cursor()
c.execute('drop table ApplyHistory')
c.execute('drop table WorkerMessage')
c.execute('drop table RestPoolTab')
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
       holidayType INT NOT NULL ,
       applyTimeLast VARCHAR(20) NOT NULL  ,
       approveState INT NOT NULL ,
       approveNote           VARCHAR(100),
       applyReason           VARCHAR(100));''')
conn.commit()
# 创建休息池表
c.execute('''CREATE TABLE IF NOT EXISTS RestPoolTab
       (userId VARCHAR(20) REFERENCES LoginMessage(userId) unique,
       generalHolidayTotal int not null DEFAULT 0 ,
       generalHolidayRemainderDays int DEFAULT 0,
       generalHolidayRemainderTime FLOAT DEFAULT 0,
       accumulateHolidayRemainderDays int DEFAULT 0,
       accumulateHolidayRemainderTime FLOAT DEFAULT 0,
       accumulateHolidayUsedDays int DEFAULT 0 ,
       accumulateHolidayUsedTime FLOAT DEFAULT 0,
       barterAccumulateHolidayDays int DEFAULT 0,
       barterAccumulateHolidayTime FLOAT DEFAULT 0,
       restPoolTotalDays int  DEFAULT 0,
       restPoolTotalTime FLOAT DEFAULT 0);''')
conn.commit()

print("数据表创建成功")
# c.execute("INSERT INTO User (ID,NAME,AGE,ADDRESS,SALARY) \
#       VALUES (2, 'Paul', 32, 'California', 20000.00 )")
# cursor = c.execute("select * from user")
# for row in cursor:
#     print (row)

c.execute("INSERT INTO LoginMessage (userId, NAME, KEY, accountType ) \
       VALUES (1, 'admin','admin1234', 2)")
conn.commit()

for item in [[73, '00073'], [2440, '02440'], [2587, '02587']]:
    cmd = "INSERT INTO LoginMessage (userId, NAME, KEY, accountType ) VALUES ({}, \'user{}\', 1234, 1)".format(
        item[0], item[1])
    c.execute(cmd)
conn.commit()

for item in [(73, '张三'), (2440, '李四'), (2587, '王五二')]:
    cmd = "INSERT INTO WorkerMessage (userId, NAME, manager ) VALUES ({}, \'{}\', 1)".format(
        item[0], item[1])
    c.execute(cmd)
conn.commit()

for item in [(73, 15), (2440, 10), (2587, 10)]:
    cmd = "INSERT INTO RestPoolTab (userid, generalHolidayTotal) VALUES ({}, {})".format(
        item[0], item[1])
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
