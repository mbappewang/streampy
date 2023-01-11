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
    omdb_url_list = []
    omdb_url=""
    sql = "select distinct imdb_id from imdb order by imdb_id asc "
    mycursor.execute(sql)
    db_imdb_id = mycursor.fetchall()
    for (x,) in db_imdb_id:
        omdb_url="http://www.omdbapi.com/?i=tt"+x[1:20]+"&apikey=57e932e4"
        omdb_url_list.append(omdb_url)
        print(x[1:20],x)
    
    f = open("omdburl.txt", "w",encoding="utf-8")
    f.close()
    for i in omdb_url_list:
        f = open("omdburl.txt", "a",encoding="utf-8")
        f.write(i)
        f.write("\n")
    f.close()
    print("done")