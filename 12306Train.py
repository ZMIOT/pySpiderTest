import requests
from bs4 import BeautifulSoup
import json

class xcSpider(object):
    def __init__(self,url):
        self.url=url;
        self.headers={
            'Referer': 'https://www.12306.cn/index/',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
        }
    def gethtml(self):

        res=requests.get(self.url,headers=self.headers)
        jsonstr = json.loads(res.text, 'utf-8')
        str=jsonstr['data']['result']
        print(str)


def main():
    base_url="https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2019-03-28&leftTicketDTO.from_station=GBZ&leftTicketDTO.to_station=CSQ&purpose_codes=ADULT"
    xcS=xcSpider(base_url)
    xcS.gethtml()

if __name__ == '__main__':
    main()