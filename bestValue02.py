import requests
from bs4 import BeautifulSoup
import pymysql


class bestValueSpider(object):
    def __init__(self,url):
        self.url=url
        self.headers={
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
            'Referer': 'http://i.meizitu.net'
        }

    def savehtmlDb(self, title, url):
        db = pymysql.connect('localhost', 'root', '123456', 'pyData')
        cursor = db.cursor()
        sql = "insert into bestvalue(title,url)" \
              "values ('%s','%s')" % (title, url)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
        cursor.close()

    def geturl(self):
        response=requests.get(self.url)
        soup=BeautifulSoup(response.text,'lxml')
        sout=soup.select("div.main-bd >  h2>a")
        bookurls=soup.select('a.subject-img')
        for tt in sout:
            print(tt.extract().get('href'))
        for url in bookurls:
            print(url.extract().get('href'))


    def getbookInfo(self):
        url=""
        res=requests.get(self.url,self.headers)
        soupBook=BeautifulSoup(res.text,'lxml')



def createDb():
    db = pymysql.connect("localhost", "root", "123456", "pyData")

    cursor = db.cursor()
    # 如果数据表已经存在使用 execute() 方法删除表。
    cursor.execute("DROP TABLE IF EXISTS bestvalue")

    # 创建数据表SQL语句
    sql = """CREATE TABLE bestvalue (
             ID  integer (255) NOT NULL AUTO_INCREMENT primary key,
             title  varchar (255),
             url varchar (255),
             )"""

    cursor.execute(sql)

    # 关闭数据库连接
    db.close()

def main():
    for i in (0,50,20):
        base_url="https://movie.douban.com/review/best/?start="+str(i)
        baseSpider=bestValueSpider(base_url)
        baseSpider.geturl();

if __name__ == '__main__':
    main()