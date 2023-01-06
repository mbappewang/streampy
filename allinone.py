# -*- coding: utf-8 -*-
#导入模块
import json
import time
import datetime
import urllib.request
import random
import mysql.connector
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
    print("连接数据库失败")
else:
#获取副表的seid存一个tuple
    sql = "select imdb_seid from tv_imdb limit 50 "
    mycursor.execute(sql)
    db_imdb_seid = mycursor.fetchall()
#获取电影和电视剧的seid/sid/id，与副表的seid判断，只要不在副表的seid，及sid id等信息
    #请求json函数
    def get_vidsrc(url):
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
        requestsite = urllib.request.Request(url,headers=headers)
        data = urllib.request.urlopen(requestsite,timeout=15).read()
        vidsrc_dic = json.loads(data)
        return vidsrc_dic
    #获取总页码
    try:
        vidsrc_dict = get_vidsrc("https://vidsrc.me/episodes/latest/page-1.json")
        vidsrc_result = vidsrc_dict["result"]
    except:
        print("没有读到页码！！！！！！！！")
        pages = 10
    else:
        print("读到页数了")
        pages = 10

        # vidsrc_dict["pages"]+1
    print("总页数：",pages)
    #生成pagelist
    page_list = []
    page_timeout_list = []
    page_tout_count = 0
    item = 0
    vidsrc_vod_info_list = []
    for x in range(1,pages+1):
        print(">>>>>>>>>>>>>>>",x,"页遍历开始","<<<<<<<<<<<<<<<<")
        #避免程序超时，用try、except
        try:
            #请求函数获得接口页信息
            vidsrc_dict = get_vidsrc("https://vidsrc.me/episodes/latest/page-" + str(x) + ".json")
        except:
            print("请求↓失败")
            page_tout_count += 1
            print("超时次数：",page_tout_count,"目前已爬条数：",item,"目前页数",x,"\n","目前进度：",x/(pages+1)*100,"%")
        else:
            print("请求↑成功")
            #将接口的json文件中的result字段取出
            vidsrc_result = vidsrc_dict["result"]
            for z in vidsrc_result:
                imdb_id = z.get("imdb_id","tt0")[1:15]
                episode_vidsrc = z.get("episode","")
                season_vidsrc = z.get("season","")
                imdb_seid = imdb_id+season_vidsrc+episode_vidsrc
                imdb_sid = imdb_id+season_vidsrc
                #与副表读到的元组，判断是否重复"episode"
                if (imdb_seid,) in db_imdb_seid:
                    pass
                else:
                    url_vidsrc =z.get("embed_url","")
                    vidsrc_vod_info = (imdb_id,imdb_seid,imdb_sid,season_vidsrc,episode_vidsrc,url_vidsrc)
                    #将遍历的信息存储进列表中备用
                    vidsrc_vod_info_list.append(vidsrc_vod_info)
                    item += 1
            print("超时次数：",page_tout_count,"目前已爬到条数：",item,"目前页数",x,"\n","目前进度：",x/(pages+1)*100,"%")
    sql = "INSERT INTO tv_imdb (imdb_id,imdb_seid,imdb_sid,season,episode,play_url_1) VALUES (%s , %s, %s, %s, %s, %s)"
    val = vidsrc_vod_info_list
    mycursor.executemany(sql, val)
    mydb.commit()
    print("完成")











#判断sid是否存在，存在的话去update重要信息，不存在的话去insert imdb信息
#如果不存在的话，还要用imdb获得imdb信息，然后用sid循环拼接重要信息和imdb信息，然后insert