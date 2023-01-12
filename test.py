# -*- coding: utf-8 -*-
#导入模块
import random
import json
import time
import datetime
import urllib.request
import mysql.connector
# import eventlet #导入eventlet这个模块
# eventlet.monkey_patch()#必须加这条代码
# starttime = datetime.datetime.now()
#连接数据库
def get_ombd(url):
    omdb_info = urllib.request.urlopen(url,timeout=15)
    omdb_info_json = json.loads(omdb_info.read())
    return omdb_info_json
try:
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd='walc94511',
    database="mac_vod"
    )
    mycursor = mydb.cursor()
except:
    print("连接数据库失败×")
else:
    print("连接数据库成功✅")
    sql = "select imdb_sid,vod_pubdate from mac_vod"
    mycursor.execute(sql)
    imdb_8db = mycursor.fetchall()
    a=0
    for (x,y) in imdb_8db:
        if y == "N/A":
            pass
        else:
            vod_year=y[-4:]
        basic_info = [vod_year,x]
        sql = "update mac_vod set vod_year = %s where imdb_sid = %s"
        val= basic_info
        mycursor.execute(sql, val)
        mydb.commit()
        a+=1
        print(a,vod_year,"<<<<<<<<<")