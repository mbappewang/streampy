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
    mac_vod=[]
except:
    print("连接数据库失败×")
else:
    print("连接数据库成功✅")
    id_url_dict = {}
    movie_info_list=[]
    f = open("/Users/shareit1/streampy/odmb/新建任务RNVYXuJO(1).json","r")
    id_url_json = json.load(f)
    f.close()
    a=0
    for x in id_url_json:
        if x.get("Released","1 Jan 1970") == "N/A":
            Unixdate = 0
        elif x.get("Released","1 Jan 1970") == "":
            Unixdate = 0
        else:
            date=x.get("Released","1 Jan 1970")
            y=int(date[-4:])
            if y >= 1971:
                M=date.split(" ")[1]
                month_list = ['月份','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
                m=str(month_list.index(M))
                d=date[:2]
                Date=str(y)+"-"+m+"-"+d+" 00:00:00"
                Unixdate=int(time.mktime(time.strptime(Date,'%Y-%m-%d %H:%M:%S')))
            else:
                Unixdate = 0
        type = x.get("Type","untype")
        if type == "movie":
            imdb_id = "m"+x["imdbID"][2:20]
            vod_name = x.get("Title","")[0:255]
        else:
            imdb_id = "t"+x["imdbID"][2:20]
            vod_name = x.get("Title","")[0:255]
        vod_year = x.get("Year","")[0:10]
        vod_duration = x.get("Runtime","1970")[0:10]
        type_genre = x.get("Genre","ungenre").split(",")[0][0:10]
        vod_class = x.get("Genre","")[0:255]
        vod_director = x.get("Director","")[0:255]
        vod_writer = x.get("Writer","")[0:255]
        vod_actor = x.get("Actors","")[0:255]
        vod_blurb = vod_content = x.get("Plot","")[0:255]
        vod_lang = x.get("Language","").split(",")[0][0:10]
        vod_area = x.get("Country","").split(",")[0][0:20]
        vod_pic = x.get("Poster","pic")[0:1024]
        vod_remarks = "IMDb: " + x.get("imdbRating","")[0:100]
        if x.get("imdbRating","") == "N/A":
            vod_douban_score = vod_score = 0.0
        else:
            vod_douban_score = vod_score = x.get("imdbRating","")
        vod_up = x.get("imdbVotes","")
        type = x.get("Type","untype")
        vod_pubdate = x.get("Released","1 Jan 1970")[0:100]
        vod_time = Unixdate
        vod_time_add = Unixdate
        vod_total = x.get("totalSeasons","1")
        vod_isend = vod_status = 1
        vod_hits = vod_hits_day = vod_hits_week = vod_hits_month = vod_score_num = random.random()*100
        group_id = vod_lock = vod_level = vod_copyright = vod_points = vod_points_play = vod_points_down = vod_down = 0
        vod_play_from_1 = "tpiframe"
        vod_play_from_2 = "tpiframecopy"
        vod_play_note = "$$$"
        vod_play_from = vod_play_from_1+vod_play_note+vod_play_from_2
        vod_play_server = "no$$$no"
        vod_info = (vod_name,vod_year,vod_duration,type_genre,vod_class,vod_director,vod_writer,vod_actor,vod_blurb,vod_lang,vod_area,vod_pic,vod_remarks,vod_douban_score,vod_score,vod_up,type,vod_pubdate,vod_time,vod_time_add,vod_total,vod_isend,vod_status,vod_hits,vod_hits_day,vod_hits_week,vod_hits_month,vod_score_num,group_id,vod_lock,vod_play_from,vod_play_server,imdb_id)
        # mac_vod.append((vod_name,vod_year,vod_duration,type_genre,vod_class,vod_director,vod_writer,vod_actor,vod_blurb,vod_lang,vod_area,vod_pic,vod_remarks,vod_douban_score,vod_score,vod_up,type,vod_pubdate,vod_time,vod_time_add,vod_total,vod_isend,vod_status,vod_hits,vod_hits_day,vod_hits_week,vod_hits_month,vod_score_num,group_id,vod_lock,vod_play_from,vod_play_server,imdb_id))
        a+=1
        sql = "update mac_vod set vod_name=%s,vod_year=%s,vod_duration=%s,type_genre=%s,vod_class=%s,vod_director=%s,vod_writer=%s,vod_actor=%s,vod_blurb=%s,vod_lang=%s,vod_area=%s,vod_pic=%s,vod_remarks=%s,vod_douban_score=%s,vod_score=%s,vod_up=%s,type=%s,vod_pubdate=%s,vod_time=%s,vod_time_add=%s,vod_total=%s,vod_isend=%s,vod_status=%s,vod_hits=%s,vod_hits_day=%s,vod_hits_week=%s,vod_hits_month=%s,vod_score_num=%s,group_id=%s,vod_lock=%s,vod_play_from=%s,vod_play_server=%s where imdb_id = %s"
        val = vod_info
        mycursor.execute(sql, val)
        mydb.commit()
        endtime = datetime.datetime.now()
        print(a,"Done",endtime-starttime)
