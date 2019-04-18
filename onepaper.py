import requests
from bs4 import BeautifulSoup
import pymysql
import sys
import urllib

class onePaperSpider(object):
    def __init__(self,url):
        self.url=url;
        self.headers={
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
            'Referer': 'http://i.meizitu.net'
        }
    def getHtml(self):
        res=requests.get(self.url,headers=self.headers)
        res.encoding='utf-8'
        soup=BeautifulSoup(res.text,'lxml')
        entexts=soup.findAll(name='div',attrs={"class":"qh_en"})
        for en in entexts:
            self.saveDb(entexts[0].text,en.text)

    def saveDb(self,title,text):
        db = pymysql.connect('localhost', 'root', '123456', 'pyData')
        cursor = db.cursor()
        sql = "insert into article(title,text)" \
              "values ('%s','%s')" % (title, text)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
        cursor.close()


def createDb():
    db = pymysql.connect("localhost", "root", "123456", "pyData")

    cursor = db.cursor()
    # 如果数据表已经存在使用 execute() 方法删除表。
    cursor.execute("DROP TABLE IF EXISTS article")

    # 创建数据表SQL语句
    sql = """CREATE TABLE article (
             ID  integer (255) NOT NULL AUTO_INCREMENT primary key,
             title  varchar (255),
             text varchar (255)
             )"""

    cursor.execute(sql)

    # 关闭数据库连接
    db.close()

def main():
    createDb()
    url="http://www.kekenet.com/read/201902/578122.shtml"
    onepaperSpider=onePaperSpider(url)
    onepaperSpider.getHtml()


if __name__ == '__main__':
    main()