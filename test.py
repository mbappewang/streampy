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
    sql = "select distinct type_id,type_genre from mac_vod where type_id_1 =94 and type_id != 109"
    mycursor.execute(sql)
    imdb_8db = mycursor.fetchall()
    a=0
    movie_genre_dict = {}
    for (x,y) in imdb_8db:
        movie_genre_dict[y]=x
    print(movie_genre_dict)