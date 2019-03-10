import requests
import pymysql
import random
import os
import platform
from threading import Timer
import time
import sys

sys.setrecursionlimit(10000)  # 例如这里设置为一百万


Headers={
    'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Referer':'http://www.mzitu.com'
}

is_windows = False
if -1 != platform.platform().upper().find('WINDOWS'):
    is_windows = True

def sqlsearch(count):
    print(count)
    str=''
    db=pymysql.connect("localhost","root","123456","pyData")

    cursor=db.cursor()

    sql="select url from DESKTOPTABLE" \
        " where id=%s"%(count)
    try:
        cursor.execute(sql)
        result=cursor.fetchone()
        str=result[0]
    except:
        db.rollback()
    db.close()
    return str

def saveImg(strurl,count):
    root = 'D:\DesktopImg/'
    if not os.path.exists(root):
        os.mkdir(root)
    path=root+str(count)+'.jpg'

    res=requests.get(strurl,headers=Headers)
    with open(path,'wb') as f:
        f.write(res.content)


# windows设置壁纸
if is_windows:
    import win32gui,win32con,win32api

def set_desktop_windows(imagepath):
    k=win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(k,"WallpaperStyle",0,win32con.REG_SZ,"2")#2拉伸适应桌面，0桌面居中
    win32api.RegSetValueEx(k,"TileWallpaper",0,win32con.REG_SZ,"0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER,imagepath,1+2)


def main():

    count=random.randint(1,341)
    strurl=sqlsearch(count)

    saveImg(strurl,count)
    imagepath = 'D:\\DesktopImg\\' +str(count)+'.jpg'
    set_desktop_windows(imagepath)

if __name__=="__main__":
    timer_interval=1
    def delayrun():
        print('')
    t=Timer(timer_interval,delayrun())
    t.start()
    while True:
        time.sleep(1000)
        main()
