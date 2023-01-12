# -*- coding: utf-8 -*-
#导入模块
import random
import json
import time
import datetime
import urllib.request
import mysql.connector
import eventlet #导入eventlet这个模块
eventlet.monkey_patch()#必须加这条代码
starttime = datetime.datetime.now()
#连接数据库
try:
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd='walc94511',
    database="mydatabase"
    )
    mycursor = mydb.cursor()
except:
    print("连接数据库失败×")
else:
    print("连接数据库成功✅")
#获取副表的seid转存成一个list
    imdb_id_list = []
    sql = "SELECT distinct imdb_id FROM mydatabase.mac_vod where vod_pic='N/A' and vod_year > 2020 "
    mycursor.execute(sql)
    db_imdb_id = mycursor.fetchall()
    for (x,) in db_imdb_id:
        url="https://www.imdb.com/title/tt"+x[1:20]
        print(url)