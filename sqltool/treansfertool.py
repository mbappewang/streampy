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
    imdb_seid_list = []
    sql = "select group_concat(play_url_1 order by episode desc  separator '#') play_url_1,group_concat(play_url_2 order by episode desc separator '#') play_url_2,imdb_sid from imdb where imdb_sid like 't%' group by imdb_sid"
    mycursor.execute(sql)
    db_imdb_seid = mycursor.fetchall()
    a=0
    for (x,y,z) in db_imdb_seid:
        a+=1
        basic_info=(x,y,z)
        sql = "update mac_vod set play_url_1 = %s , play_url_2 = %s where imdb_sid = %s"
        val = basic_info
        mycursor.execute(sql, val)
        mydb.commit()
    print("done")