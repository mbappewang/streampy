# -*- coding: utf-8 -*-
#导入模块
import random
import json
import time
import datetime
import urllib.request
import mysql.connector
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
    sql = "select imdb_sid,group_concat(distinct imdb_id) imdb,group_concat(distinct season) season,group_concat(play_url_1 order by episode desc) play_url_1,group_concat(play_url_2 order by episode desc)play_url_2 from imdb group by imdb_sid"
    mycursor.execute(sql)
    db_imdb_id = mycursor.fetchall()
    sql = "INSERT INTO mac_vod (imdb_sid,imdb_id,season,play_url_1,play_url_2) VALUES (%s,%s,%s,%s,%s)"
    val = db_imdb_id
    mycursor.executemany(sql, val)
    mydb.commit()