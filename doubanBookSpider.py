import requests

from bs4 import BeautifulSoup

import json

class DongManSpider(object):
    def __init__(self,url):
        self.url=url
        self.headers={
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
            'Referer': 'https://ebb.io/anime/498x833'
        }
        pass
    def getHtml(self):
        res=requests.get(self.url,headers=self.headers)
        soup=BeautifulSoup(res.text,'lxml')
        alist=soup.select('body > div.list > dl > dt > a')
        nameList=soup.select('body > div.list > dl> dd > a')
        print(alist)
        print(nameList)

def main():
    base_url="http://m.fengchedm.com/"
    dongManSpi=DongManSpider(base_url)
    dongManSpi.getHtml()


if __name__ == '__main__':
    main()