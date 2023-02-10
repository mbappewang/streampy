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
def get_vidsrc(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
    requestsite = urllib.request.Request(url,headers=headers)
    data = urllib.request.urlopen(requestsite,timeout=15).read()
    vidsrc_dic = json.loads(data)
    return vidsrc_dic
try:
    mydb = mysql.connector.connect(
    host="139.84.165.93",
    user="v49me",
    passwd='622DaweMYJ4wKpX6',
    database="v49me")
    mycursor = mydb.cursor()
except:
    print("连接数据库失败×")
else:
    print("连接数据库成功✅")
    try:
        vidsrc_dict = get_vidsrc("https://vidsrc.me/movies/latest/page-1.json")
        vidsrc_result = vidsrc_dict["result"]
    except:
        pages = 1300
        print("没有读到页数","设定页面默认值为",pages,"页")
    else:
        sql = "select imdb_id from movie"
        mycursor.execute(sql)
        imdb_8db = mycursor.fetchall()
        pages = vidsrc_dict["pages"]
        print("读到页数了✅","共",pages,"页")
    for page in range(1,pages+1):
        try:
            vidsrc_dict = get_vidsrc("https://vidsrc.me/movies/latest/page-" + str(page) + ".json")
            vidsrc_result = vidsrc_dict["result"]
        except:
            print(page,"超时")
        else:
            print(page,"正常")
            for info in vidsrc_result:
                if (info["imdb_id"],) in imdb_8db:
                    print("已存在",info["imdb_id"],info["title"])
                    pass
                else:
                    basic_info=[info["imdb_id"],info["title"],info["embed_url"]]
                    sql = "insert into movie (imdb_id,vod_name,play_url_1) values (%s,%s,%s)"
                    val= basic_info
                    mycursor.execute(sql, val)
                    mydb.commit()
                    print("新加入",info["imdb_id"],info["title"])