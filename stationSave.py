import pymysql

import json


def saveDb(StationName,StationCode):
    db = pymysql.connect("localhost", "root", "123456", "pyData")

    cursor = db.cursor()
    sql = "insert into StationCodeInfo(StationName,StationCode)" \
          "values ('%s','%s')" % (StationName,StationCode)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    cursor.close()




def readJson():
    with open("C:\\Users\\Administrator\\Desktop\\name_code.json",'r') as f:
        data=json.load(f)
    return data


def main():
    #createDb()
    i=0
    data=readJson()
    for key in data:
        i=i+1
        print(i)
        #saveDb(key,data[key])

if __name__ == '__main__':
    main()