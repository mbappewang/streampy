# -*- coding: utf-8 -*-
#导入模块
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
#获取副表的seid存一个tuple
    imdb_seid_list = []
    sql = "select imdb_seid from tv_imdb "
    mycursor.execute(sql)
    db_imdb_seid = mycursor.fetchall()
    for (x,) in db_imdb_seid:
        imdb_seid_list.append(x)
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
        pages = 15
        print("妹读到页数了×","设定页面默认值为",pages,"页")
    else:
        pages = 15
        print("读到页数了✅","共",pages,"页")
    #生成pagelist
    page_tout_count = 0
    vidsrc_result=[]
    same_imdb_seid = 0
    no_data_page = 0
    dif_imdb_seid = 0
    for x in range(1,pages+1):
        #避免程序超时，用try、except
        try:
            #请求函数获得接口页信息
            vidsrc_dict = get_vidsrc("https://vidsrc.me/episodes/latest/page-" + str(x) + ".json")
        except:
            page_tout_count += 1
            # print("TV爬取进程运行状态>>>","进度：",x/(pages+1)*100,"%","库内集数：",len(imdb_seid_list),"新发现集数：",dif_imdb_seid,"超时次数：",page_tout_count)
        else:
            if len(vidsrc_dict["result"]) != 0:
                no_data_page = 0
                for y in vidsrc_dict["result"]:
                    imdb_id = y["imdb_id"][1:20]
                    season = int(y["season"])
                    episode = int(y["episode"])
                    imdb_sid = imdb_id + str(season)
                    imdb_seid = imdb_id + str(season) + str(episode)
                    play_url_1 = y["embed_url"]
                    play_url_2 = "https://www.2embed.to/embed/imdb/tv?id="+"t"+imdb_id+"&s="+str(season)+"&e="+str(episode)
                    if imdb_seid in imdb_seid_list:
                        same_imdb_seid += 1
                        # print("TV爬取进程运行状态>>>","进度：",x/(pages+1)*100,"%","库内集数：",len(imdb_seid_list),"新发现集数：",dif_imdb_seid,"超时次数：",page_tout_count)
                    else:
                        same_imdb_seid = 0
                        dif_imdb_seid += 1
                        vidsrc_result.append((imdb_id,imdb_sid,imdb_seid,season,episode,play_url_1,play_url_2))
                        # print("TV爬取进程运行状态>>>","进度：",x/(pages+1)*100,"%","库内集数：",len(imdb_seid_list),"新发现集数：",dif_imdb_seid,"超时次数：",page_tout_count)
            else:
                no_data_page += 1
        if no_data_page == 10:
            print("TV已发现连续10个页面为空，已停止爬取")
            break
        if same_imdb_seid == 500:
            print("TV已发现连续500条记录为空，已停止爬取")
            break
        endtime = datetime.datetime.now()
        print("TV爬取进程运行状态>>>","%4d" % x,"页已抓取完毕","进度：","%3.2f" % (x/(pages+1)*100),"%","库内集数：","%6d" % len(imdb_seid_list),"新发现集数：","%6d" % dif_imdb_seid,"超时次数：",page_tout_count,"已运行时间：",endtime - starttime)
    sql = "INSERT INTO tv_imdb (imdb_id,imdb_sid,imdb_seid,season,episode,play_url_1,play_url_2) VALUES (%s , %s, %s, %s, %s, %s, %s)"
    val = vidsrc_result
    mycursor.executemany(sql, val)
    mydb.commit()




#获取副表的seid存一个tuple
    imdb_seid_list = []
    sql = "select imdb_seid from tv_imdb "
    mycursor.execute(sql)
    db_imdb_seid = mycursor.fetchall()
    for (x,) in db_imdb_seid:
        imdb_seid_list.append(x)
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
        vidsrc_dict = get_vidsrc("https://vidsrc.me/movies/latest/page-1.json")
        vidsrc_result = vidsrc_dict["result"]
    except:
        pages = 15
        print("妹读到页数了×","设定页面默认值为",pages,"页")
    else:
        pages = 15
        print("读到页数了✅","共",pages,"页")
    #生成pagelist
    page_tout_count = 0
    vidsrc_result=[]
    same_imdb_seid = 0
    no_data_page = 0
    dif_imdb_seid = 0
    for x in range(1,pages+1):
        #避免程序超时，用try、except
        try:
            #请求函数获得接口页信息
            vidsrc_dict = get_vidsrc("https://vidsrc.me/episodes/latest/page-" + str(x) + ".json")
        except:
            page_tout_count += 1
            # print("TV爬取进程运行状态>>>","进度：",x/(pages+1)*100,"%","库内集数：",len(imdb_seid_list),"新发现集数：",dif_imdb_seid,"超时次数：",page_tout_count)
        else:
            if len(vidsrc_dict["result"]) != 0:
                no_data_page = 0
                for y in vidsrc_dict["result"]:
                    imdb_id = "m" + y["imdb_id"][2:20]
                    season = 0
                    episode = 0
                    imdb_sid = imdb_id + str(season)
                    imdb_seid = imdb_id + str(season) + str(episode)
                    play_url_1 = y["embed_url"]
                    play_url_2 = "https://www.2embed.to/embed/imdb/movie?id="+"tt"+imdb_id[1:20]
                    if imdb_seid in imdb_seid_list:
                        same_imdb_seid += 1
                        # print("TV爬取进程运行状态>>>","进度：",x/(pages+1)*100,"%","库内集数：",len(imdb_seid_list),"新发现集数：",dif_imdb_seid,"超时次数：",page_tout_count)
                    else:
                        same_imdb_seid = 0
                        dif_imdb_seid += 1
                        vidsrc_result.append((imdb_id,imdb_sid,imdb_seid,season,episode,play_url_1,play_url_2))
                        # print("TV爬取进程运行状态>>>","进度：",x/(pages+1)*100,"%","库内集数：",len(imdb_seid_list),"新发现集数：",dif_imdb_seid,"超时次数：",page_tout_count)
            else:
                no_data_page += 1
        if no_data_page == 10:
            print("Movie已发现连续10个页面为空，已停止爬取")
            break
        if same_imdb_seid == 500:
            print("Movie已发现连续500条记录为空，已停止爬取")
            break
        endtime = datetime.datetime.now()
        print("Movie爬取进程运行状态>>>","%4d" % x,"页已抓取完毕","进度：","%4.2f" % (x/(pages+1)*100),"%","库内集数：",len(imdb_seid_list),"新发现集数：",dif_imdb_seid,"超时次数：",page_tout_count,"已运行时间：",endtime - starttime)
    sql = "INSERT INTO tv_imdb (imdb_id,imdb_sid,imdb_seid,season,episode,play_url_1,play_url_2) VALUES (%s , %s, %s, %s, %s, %s, %s)"
    val = vidsrc_result
    mycursor.executemany(sql, val)
    mydb.commit()












#判断sid是否存在，存在的话去update重要信息，不存在的话去insert imdb信息
#如果不存在的话，还要用imdb获得imdb信息，然后用sid循环拼接重要信息和imdb信息，然后insert