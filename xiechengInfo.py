import requests
from bs4 import BeautifulSoup
import json
import pymysql
import re

class xcSpider(object):
    def __init__(self,url):
        self.url=url;
        self.headers={
            'referer':'http://www.12306.com/',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
        }
    def gethtml(self):
        res=requests.get(self.url,headers=self.headers)

        jsonstr=json.loads(res.text,'utf-8')
        trainInfos=jsonstr['data']['trainInfos']

        for trainInfo in trainInfos:
            deptDate=trainInfo['deptDate']
            deptTime=trainInfo['deptTime']
            seatList=trainInfo['seatList']
            arrTime=trainInfo['arrTime']
            deptStationName=trainInfo['deptStationName']
            trainCode=trainInfo['trainCode']
            arrStationName=trainInfo['arrStationName']
            arrDate=trainInfo['arrDate']
            runTime=trainInfo['runTime']
            seatName = []
            seatPrice = []
            seatNum = []
            for seatType in seatList:
                seatName.append(seatType['seatName'])
                seatPrice.append(seatType['seatPrice'])
                seatNum.append(seatType['seatNum'])
            self.saveDb(deptDate,trainCode,deptTime,arrTime,deptStationName,arrStationName,arrDate,runTime,seatName,seatPrice,seatNum)


            # else:
            #     createDb()
            #     self.saveDb(trainCode,deptTime,arrTime,deptStationName,arrStationName, runTime, seatName, seatPrice,seatNum)


    def saveDb(self,deptDate,trainCode,deptTime,arrTime,deptStationName,arrStationName,arrDate,runTime,seatName,seatPrice,seatNum):
        if(len(seatName)<3):
            seatName.append("无")
            seatPrice.append("无")
            seatNum.append("无")
        print(trainCode, deptTime, arrTime, deptStationName, arrStationName, runTime, seatName[0], seatName[1],
              seatName[2], seatPrice[0], seatPrice[1], seatPrice[2], seatNum[0], seatNum[1], seatNum[2])
        db = pymysql.connect("localhost", "root", "123456", "pyData")

        cursor = db.cursor()
        sql = "insert into trainInfo(deptDate,trainCode,deptTime,arrTime,deptStationName,arrStationName,arrDate,runTime,seatNameSoftSleeper,seatNameHardSleeper,seatNameHard,seatPriceSoftSleeper,seatPriceHardSleeper,seatPriceHard,seatNumSoftSleeper,seatNumHardSleeper,seatNumHard)" \
              "values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (deptDate,trainCode,deptTime,arrTime,deptStationName,arrStationName,arrDate,runTime,seatName[0],seatName[1],seatName[2],seatPrice[0],seatPrice[1],seatPrice[2],seatNum[0],seatNum[1],seatNum[2])
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
        cursor.close()

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
def createDb():
    db = pymysql.connect("localhost", "root", "123456", "pyData")

    cursor = db.cursor()
    # 如果数据表已经存在使用 execute() 方法删除表。
    cursor.execute("DROP TABLE IF EXISTS trainInfo")

    # 创建数据表SQL语句
    sql = """CREATE TABLE trainInfo (
         ID  integer (255) NOT NULL AUTO_INCREMENT primary key,
         deptDate varchar (255),
         trainCode  varchar (255),
         deptTime varchar(255),
         arrTime varchar (255),
         deptStationName varchar (255),
         arrStationName varchar (255),
         arrDate varchar (255),
         runTime varchar (255),
         seatNameSoftSleeper varchar (255),
         seatNameHardSleeper varchar (255),
         seatNameHard varchar (255),
         seatPriceSoftSleeper varchar (255),
         seatPriceHardSleeper varchar (255),
         seatPriceHard varchar (255),
         seatNumSoftSleeper varchar (255),
         seatNumHardSleeper varchar (255),
         seatNumHard varchar (255)
         )"""

    cursor.execute(sql)

    # 关闭数据库连接
    db.close()

def main():
    createDb()
    base_url="http://api.12306.com/v1/train/trainInfos?arrStationCode=CSQ&deptDate=2019-04-01&deptStationCode=GBZ&findGD=false"
    xcS=xcSpider(base_url)
    xcS.gethtml()

if __name__ == '__main__':
    main()