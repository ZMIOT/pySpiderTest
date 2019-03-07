import requests
from bs4 import BeautifulSoup
import pymysql
import re

Headers={
    'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Referer':'http://www.mzitu.com'
}

bizhiurl='http://desk.zol.com.cn'
i=0

def getHtml(url):
    r=requests.get(url,headers=Headers)
    html=BeautifulSoup(r.text,'lxml')
    return html


def getImg_url(albumurls):
    response=getHtml(albumurls)
    html=BeautifulSoup(response.text,'lxml')
    reg=r'^bdPic			:.+\.jpg'
    img=html.find(reg)
    print(img)
    # print(html)
    alist=html.select('#showImg > li> a')
    for a in alist:
        url=a.get('bdPic')
        print(url)
        saveDb(url)

def get_album_urls(response):
    albumurls=response.select('body > div.wrapper.top-main.clearfix > div.main > ul:nth-child(3) > li > a')
    for albumurl in albumurls:
        alurl=albumurl.get('href')
        alurl=bizhiurl+alurl
        #print("zongde:"+alurl)
        getImg_url(alurl)

def saveDb(url):
    db=pymysql.connect("localhost","root","123456","pyData")
    cursor=db.cursor()
    sql="insert into DESKTOP(url)" \
        "values ('%s')"%url



def main():

    for page in range(1,2):
        url = 'http://desk.zol.com.cn/meinv/%s'%page+'.html'
        response=getHtml(url)
        albums=get_album_urls(response)


if __name__=="__main__":
    main()