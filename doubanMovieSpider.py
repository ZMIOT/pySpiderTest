import requests
from bs4 import BeautifulSoup

import pymysql

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
        movies=soup.select('#nowplaying > div.mod-bd > ul>li')
        for movie in movies:
            title=movie.get('data-title')
            score=movie.get('data-score')
            director=movie.get('data-director')
            actors=movie.get('data-actors')
            self.saveDb(title,score,director,actors)
    def saveDb(self,title,score,director,actors):
        db=pymysql.connect('localhost','root','123456','pyData')
        cursor = db.cursor()
        sql = "insert into nowplayingMovie(title,score,director,actors)" \
              "values ('%s','%s','%s','%s')"  %(title,score,director,actors)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
        cursor.close()

def main():
    base_url='https://movie.douban.com/cinema/nowplaying/guilin/'
    MoiveSpider=doubanMoiveSpider(base_url)
    MoiveSpider.getHtml()
    pass
if __name__ == '__main__':
    main()