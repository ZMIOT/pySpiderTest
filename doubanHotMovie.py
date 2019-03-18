import requests
from bs4 import BeautifulSoup

import pymysql
import json

class doubanMoiveSpider(object):
    def __init__(self,url):
        self.url=url
        self.headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
            'Referer': 'http://i.meizitu.net'
        }
    def getHtml(self):
        res=requests.get(self.url,headers=self.headers)
        soup=BeautifulSoup(res.text,'lxml')
        jsonstr=json.loads(soup.text,'utf-8')
        movies=jsonstr['subjects']
        for movie in movies:
            title=movie.get('title')
            score=movie.get('rate')
            imgurl=movie.get('cover')
            self.saveDb(title,score,imgurl)

    def saveDb(self,title,score,url):
        db=pymysql.connect('localhost','root','123456','pyData')
        cursor = db.cursor()
        sql = "insert into hotmovie(title,score,imgurl)" \
              "values ('%s','%s','%s')"%(title,score,url)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
        cursor.close()

def main():
    for i in range(0,160,20):
        base_url='https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start='+str(i)
        MoiveSpider=doubanMoiveSpider(base_url)
        MoiveSpider.getHtml()
if __name__ == '__main__':
    main()