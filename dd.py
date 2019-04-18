import requests
from urllib.parse import urlencode

def get_info_single_way(From, To, Date):
    """
    获取单程票信息
    :param From: 起点
    :param To: 终点
    :param Date: 出发日期
    :return:
    """
    base_url = 'http://trains.ctrip.com/TrainBooking/Search.aspx?'
    params1 = {
        'day': Date,
        'number': '',
        'fromDn': From.encode('gb2312'),
        'toCn': To.encode('gb2312')
    }
    Referer = base_url + urlencode(params1)

    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept - Language': 'zh-CN,zh;q=0.9',
        'Cache - Control': 'max-age = 0',
        'Connection': 'keep-alive',
        'Content-Length': '62',
        'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
        'Cookie': 'Cookie: searchlist=searchlisttop=1600; _abtest_userid=284ec01c-8af2-4134-934b-ee13ba282aba; _RSG=J4a4rpx_VlAMFx_tq1s.RA; _RDG=28c49f4a6901d72b36368238aa2e187df1; _RGUID=abdfffbc-f512-4113-a6fe-d81d37ffb3d6; _ga=GA1.2.576637053.1522582993; _RF1=118.112.104.116; Union=SID=155952&AllianceID=4897&OUID=baidu81|index|||; Session=SmartLinkCode=U155952&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=&SmartLinkLanguage=zh; _gid=GA1.2.377537266.1535591623; traceExt=campaign=CHNbaidu81&adid=index; MKT_Pagesource=PC; ASP.NET_SessionSvc=MTAuMTQuMy4xODB8OTA5MHxvdXlhbmd8ZGVmYXVsdHwxNTM1MDIxMzU5ODIz; appFloatCnt=1; manualclose=1; _jzqco=%7C%7C%7C%7C1522582993587%7C1.936207270.1522582993497.1535591806663.1535592162398.1535591806663.1535592162398.0.0.0.4.4; _gat=1; Mkt_UnionRecord=%5B%7B%22aid%22%3A%224897%22%2C%22timestamp%22%3A1535599600235%7D%5D; _bfi=p1%3D0%26p2%3D108002%26v1%3D27%26v2%3D26; __zpspc=9.6.1535599600.1535599600.1%231%7Cbaidu%7Ccpc%7Cbaidu81%7C%25E6%2590%25BA%25E7%25A8%258B%7C%23; _bfa=1.1522582990697.3so118.1.1535594396209.1535599596947.8.28; _bfs=1.2',
        'Host': 'trains.ctrip.com',
        'If-Modified-Since': 'Thu, 01 Jan 1970 00:00:00 GMT',
        'Origin': 'http://trains.ctrip.com',
        'Referer': Referer,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3528.4 Safari/537.36'
    }
    data = {
        'value': {"dname": From, "aname": To, "ddate": Date}
    }
    params2 = {'Action': 'searchColudTickets'}
    url = 'http://trains.ctrip.com/TrainBooking/Ajax/SearchListHandler.ashx?' + urlencode(params2)
    response = requests.post(url, data=data, headers=headers)
    print(response.text)

if __name__ == '__main__':
    get_info_single_way('成都', '上海', '2019-03-31')