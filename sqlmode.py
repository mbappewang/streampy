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
#根据主表记录，清掉副表所有的不存在于主表的sid
    sql = "select imdb_sid from mac_vod"
    mycursor.execute(sql)
    mac_sid = mycursor.fetchall()

    sql = "delete from imdb where imdb_sid not in %s"
    val= mac_sid
    mycursor.executemany(sql, val)
    mydb.commit()



#访问vidsrc，添加进副表，获得新sid和旧sid

#新的sid进行sql语句合并insert到主表

#针对新的sid，去除其中的id，请求omdb获得信息update

#omdb无法覆盖的信息，sub genre记入other，名字保留vidsrc的名字

#旧的sid进行sql语句合并uodate到主表