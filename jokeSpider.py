# encoding:utf-8
import requests

from bs4 import BeautifulSoup

import re

import pymysql

baseurl = 'http://xiaohua.zol.com.cn'


class jokeSpider(object):
    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
            'Referer': 'http://i.meizitu.net'
        }

    def gethtml(self, url):
        url = baseurl + url
        response = requests.get(url, headers=self.headers)
        soup1 = BeautifulSoup(response.text, 'lxml')
        [x.extract() for x in soup1.find_all('script')]
        # print(soup1)
        divlist = soup1.select('div.article-text')
        for te in divlist:
            content = te.prettify()
            reg1 = re.compile("<[^>]*>")
            content = reg1.sub('', te.prettify())

            print(content)

    def parsehtml(self):
        res = requests.get(self.url, headers=self.headers)
        cont=res.content.decode('utf-8')
        soup=BeautifulSoup(cont,'lxml')
        # bt=soup.xpath('//*[@id="1857646"]/dl/dd/div[2]/text()')
        # print(bt)
        burl = soup.select('body > div.w960.clearfix > div.w645.fl>div.list-item.bg1.b1.boxshadow>dl.clearfix.dl-con>dd>div.content-img.clearfix.pt10.relative')
        for t in burl:
            self.saveDb(t.text.strip())



    def saveDb(self,str):
        db = pymysql.connect("localhost", "root", "123456", "pyData")
        cursor = db.cursor()
        sql = "insert into jokelist(text)" \
              "values ('%s')" % (str)
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
    cursor.execute("DROP TABLE IF EXISTS jokelist")

    # 创建数据表SQL语句
    sql = """CREATE TABLE jokelist (
         ID  integer (255) NOT NULL AUTO_INCREMENT primary key,
         TEXT  varchar (255))"""

    cursor.execute(sql)

    # 关闭数据库连接
    db.close()

def main():
    createDb()
    for i in range(1,51):
        base_url = 'https://www.pengfue.com/index_'+str(i)+'.html'
        jokes = jokeSpider(base_url)
        jokes.parsehtml()
        print('\n')

if __name__ == '__main__':
    main()
