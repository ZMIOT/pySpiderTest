import requests
from bs4 import BeautifulSoup
import pymysql

class bookSpider(object):
    def __init__(self,url):
        self.url=url;
        self.headers={
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
            'Referer': 'http://i.meizitu.net'
        }
    def getHtml(self):
        res=requests.get(self.url,self.headers)
        soup=BeautifulSoup(res.text,"lxml")
        tt=soup.select('body > div:nth-child(5) > div.firs.d.l.topk > div.topli > ul > li>a')
        for url in tt:
            dmurl="http://www.fengchedm.com"+url.get('href')
            title=url.get('title')
            print(dmurl,title)
            self.saveDb(dmurl,title)

    def saveDb(self, dmurl,title):
        db = pymysql.connect('localhost', 'root', '123456', 'pyData')
        cursor = db.cursor()
        sql = "insert into dmlist(dmurl,title)" \
              "values ('%s','%s')" % (dmurl,title)
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
    cursor.execute("DROP TABLE IF EXISTS dmlist")

    # 创建数据表SQL语句
    sql = """CREATE TABLE dmlist (
                 ID  integer (255) NOT NULL AUTO_INCREMENT primary key,
                 dmurl varchar (255),
                 titile varchar (255)
                 )"""

    cursor.execute(sql)

    # 关闭数据库连接
    db.close()

def main():
    base_url="http://www.fengchedm.com/paiming/137.html"
    bookspider=bookSpider(base_url)
    bookspider.getHtml()
if __name__ == '__main__':
    main()