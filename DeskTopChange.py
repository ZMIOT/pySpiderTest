import pymysql

db=pymysql.connect("localhost","root","123456","pyData")

#使用cursor()方法创建一个游标对象cursor()

cursor=db.cursor()

#使用execute()方法执行sql查询
cursor.execute("SELECT VERSION()")

#使用fetchone()方法获取单条数据
data=cursor.fetchone()

print("Database version :%s"%data)

#关闭数据库连接
db.close()


