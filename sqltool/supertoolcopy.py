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
    imdb_seid_list = []
    sql = "SELECT imdb_seid FROM imdb"
    mycursor.execute(sql)
    db_imdb_seid = mycursor.fetchall()
    for (x,) in db_imdb_seid:
        imdb_seid_list.append(x)
    def get_vidsrc(url):
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
        requestsite = urllib.request.Request(url,headers=headers)
        data = urllib.request.urlopen(requestsite,timeout=15).read()
        vidsrc_dic = json.loads(data)
        return vidsrc_dic
    try:
        vidsrc_dict = get_vidsrc("https://vidsrc.me/movies/latest/page-1.json")
        vidsrc_result = vidsrc_dict["result"]
    except:
        pages = 1210
        print("妹读到页数了×","设定页面默认值为",pages,"页")
    else:
        pages = 1210
        print("读到页数了✅","共",pages,"页")
        #生成pagelist
        page_tout_count = 0
        vidsrc_result=[]
        same_imdb_seid = 0
        no_data_page = 0
        dif_imdb_seid = 0
        mac_vod = []
        sid_url = []
        same_sid_url_dict = {}
        imdb_record=[]
        tv_item=0
        for x in range(1,pages+1):
            #避免程序超时，用try、except
            try:
                #请求函数获得接口页信息
                vidsrc_dict = get_vidsrc("https://vidsrc.me/movies/latest/page-" + str(x) + ".json")
            except:
                page_tout_count += 1
            else:
                if len(vidsrc_dict["result"]) != 0:
                    no_data_page = 0
                    for y in vidsrc_dict["result"]:
                        imdb_id = "m"+y["imdb_id"][2:20]
                        imdb_sid = imdb_id + "0"
                        imdb_seid = imdb_id + "00"
                        play_url_1 = "HD"+"$"+y["embed_url"]
                        play_url_2 = "HD"+"$"+"https://www.2embed.to/embed/imdb/tv?id="+"tt"+imdb_id[1:20]
                        if imdb_seid in imdb_seid_list:
                            same_imdb_seid += 1
                            print(">>>>>>>>>>>>>>>>>>>>>>>","重复了",same_imdb_seid)
                        else:
                            imdb_record = (imdb_id,imdb_sid,imdb_seid,play_url_1,play_url_2)
                            same_imdb_seid = 0
                            dif_imdb_seid += 1
                            sql = "INSERT INTO imdb (imdb_id,imdb_sid,imdb_seid,play_url_1,play_url_2) VALUES (%s,%s,%s,%s,%s)"
                            val = imdb_record
                            mycursor.execute(sql, val)
                            mydb.commit()
                            endtime = datetime.datetime.now()
                            print(dif_imdb_seid,endtime-starttime)
            if same_imdb_seid == 1000:
                print("TV已发现连续1000条记录为空，已停止爬取")
                break