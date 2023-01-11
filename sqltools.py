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
    # movie_info_list = []
    # sql = "select imdb_id,play_url_1 from imdb order by imdb_id"
    # mycursor.execute(sql)
    # db_imdb_id = mycursor.fetchall()
    id_url_dict = {}
    movie_info_list=[]
    f = open("/Users/shareit1/streampy/新建任务P2e8qEhN(15).json","r")
    id_url_json = json.load(f)
    f.close()
    for x in id_url_json:
        imdb_id = "t"+x["imdb_id"][2:20]
        season = x["season"]
        episode = x["episode"]
        imdb_sid = imdb_id+season
        imdb_seid = imdb_sid + episode
        play_url_1 = "Episode"+ episode + "$"+x["embed_url"]
        play_url_2 = "Episode"+episode+"$https://www.2embed.to/embed/imdb/tv?id="+"tt"+imdb_id[2:20]+"&s="+season+"&e="+episode
        movie_info = (imdb_sid,imdb_seid,play_url_1,play_url_2,imdb_id,season,episode)
        movie_info_list.append(movie_info)

    sql = "insert into imdb (imdb_sid,imdb_seid,play_url_1,play_url_2,imdb_id,season,episode) values (%s,%s,%s,%s,%s,%s,%s)"
    val = movie_info_list
    mycursor.executemany(sql, val)
    mydb.commit()
    endtime = datetime.datetime.now()
    print("Done",endtime-starttime)