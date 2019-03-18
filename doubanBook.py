import requests
from bs4 import BeautifulSoup

import pymysql
import re

class doubanMoiveSpider(object):

    def __init__(self,url):
        self.url=url
        self.headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
            'Referer': 'http://i.meizitu.net'
        }
        self.taglist={}

    #这里抓取书籍的分类tag
    def getHtml(self):
        res=requests.get(self.url,headers=self.headers)
        soup=BeautifulSoup(res.text,'lxml')
        tags=soup.select('#content > div > div.article > div:nth-child(2) > div > table > tbody > tr>td>a')
        for tag in tags:
            booktag=tag.get('href')
            markname=tag.text
            if(self.table_exists('booktag')==1):
                self.savehtmlDb(booktag,markname)
            else:
               print("表不存在")

    #这里抓取各个类别下的书籍进行存取
    def getBook(self):
        base_url='https://book.douban.com'
        self.getTag('booktag')
        base_tag=""
        tags=""
        print(self.taglist)
        for urltag in self.taglist:
            url=base_url+urltag
            tags=urltag.split('/')[2]
            res=requests.get(url,headers=self.headers)
            soup=BeautifulSoup(res.text,'lxml')
            books=soup.select('#subject_list > ul > li')
            for book in books:
                imgurlzz=r'^https://.+\.jpg$'#获取书籍图片的正则
                bookzz=r'.+'
                scorezz=r'rating_nums'
                bookname=book.find(name='a',attrs={'title':re.compile(bookzz)})
                bookname=bookname.get('title')
                imgurl=book.find(name='img',attrs={"src":re.compile(imgurlzz)})
                imgurl=imgurl.get('src')
                score=book.find(name='span',attrs={"class":"rating_nums"})
                author=book.find(name="div",attrs={"class":'pub'})
                author=author.text.strip().split('/')[0]
                if(self.table_exists('booklist')==1):
                    self.saveDb(bookname,author,score,imgurl,tags)
                else:
                    createDb()
                    self.saveDb(bookname,author,score,imgurl,tags)

    def table_exists(self,table_name):
        #这个函数用来判断表是否存在
        db = pymysql.connect('localhost', 'root', '123456', 'pyData')
        sql = "show tables;"
        cursor=db.cursor()
        cursor.execute(sql)
        tables = [cursor.fetchall()]
        table_list = re.findall('(\'.*?\')', str(tables))
        table_list = [re.sub("'", '', each) for each in table_list]
        if table_name in table_list:
            return 1 # 存在返回1
        else:
            return 0 # 不存在返回0
    def getTag(self,dbname):
        db=pymysql.connect('localhost','root','123456','pyData')
        cursor=db.cursor()
        sql="select markname,mark from %s"%dbname
        cursor.execute(sql)
        dbresult=cursor.fetchall()
        for booktag in dbresult:
            self.taglist[booktag[0]]=booktag[1]
    def saveDb(self,bookname,author,score,imgurl,mark):
        db=pymysql.connect('localhost','root','123456','pyData')
        cursor = db.cursor()
        sql = "insert into booklist(bookname,author,score,discription,imgurl,mark)" \
              "values ('%s','%s','%s','%s','%s','%s')"%(bookname,author,score,"",imgurl,mark)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
        cursor.close()
    def savehtmlDb(self,markname,mark):
        db=pymysql.connect('localhost','root','123456','pyData')
        cursor = db.cursor()
        sql = "insert into booktag(markname,mark)" \
              "values ('%s','%s')"%(markname,mark)
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
    cursor.execute("DROP TABLE IF EXISTS booklist")

    # 创建数据表SQL语句
    sql = """CREATE TABLE booklist (
             ID  integer (255) NOT NULL AUTO_INCREMENT primary key,
             bookname  varchar (255),
             author varchar (255),
             score varchar (255),
             discription varchar (255),
             imgurl varchar (255),
             mark varchar (255)
             )"""

    cursor.execute(sql)

    # 关闭数据库连接
    db.close()

def main():
    base_url='https://book.douban.com/tag/?view=cloud'
    MoiveSpider=doubanMoiveSpider(base_url)
    MoiveSpider.getHtml()
    MoiveSpider.getBook()
if __name__ == '__main__':
    main()
