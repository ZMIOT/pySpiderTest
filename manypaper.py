import requests
from bs4 import BeautifulSoup
import pymysql
import sys
import urllib

class manyPaperSpider(object):
    def __init__(self,url):
        self.url=url
        self.headers={
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
            'Referer': 'http://i.meizitu.net'
        }
    def getOneHtml(self,url,title):
        print(url)
        res=requests.get(url,headers=self.headers)
        res.encoding='utf-8'
        soup=BeautifulSoup(res.text,'lxml')
        entexts=soup.findAll(name='div',attrs={"class":"qh_en"})
        print(entexts)
        # for en in entexts:
        #     print(title,en.text)
            #self.saveDb(title,en.text)
    def getManyHtml(self):
        res1=requests.get(self.url,self.headers)
        res1.encoding='utf-8'
        soup1=BeautifulSoup(res1.text,'lxml')
        aurls=soup1.select('#menu-list > li > h2 > a:nth-child(2)')
        for aurl in aurls:
            self.getOneHtml(aurl.get("href"),aurl.get('title'))

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

    for num in range(1,100):
        urls="http://www.kekenet.com/read/ss/"+"List_"+str(num)+".shtml"
        manypaperSpider = manyPaperSpider(urls)
        manypaperSpider.getManyHtml()


if __name__ == '__main__':
    main()