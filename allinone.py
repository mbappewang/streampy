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
    database="localtest"
    )
    mycursor = mydb.cursor()
except:
    print("连接数据库失败")
else:
#获取副表的seid存一个tuple
    imdb_seid_list = []
    sql = "select imdb_seid from tv_imdb limit 50 "
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
        print("没有读到页码！！！！！！！！")
        pages = 5
    else:
        print("读到页数了")
        pages = 5

        # vidsrc_dict["pages"]+1
    print("总页数：",pages)
    #生成pagelist
    page_list = []
    page_timeout_list = []
    page_tout_count = 0
    item = 0
    vidsrc_vod_info_list = []
    del vidsrc_result
    vidsrc_result=[]
    for x in range(1,pages+1):
        print(">>>>>>>>>>>>>>>",x,"页遍历开始","<<<<<<<<<<<<<<<<")
        #避免程序超时，用try、except
        try:
            #请求函数获得接口页信息
            vidsrc_dict = get_vidsrc("https://vidsrc.me/episodes/latest/page-" + str(x) + ".json")
        except:
            page_tout_count += 1
            print("超时次数：",page_tout_count,"目前已爬条数：",item,"目前页数",x,"目前进度：",x/(pages+1)*100,"%","请求↓失败")
        else:
            #将接口的json文件中的result字段取出
            vidsrc_result += vidsrc_dict["result"]













#判断sid是否存在，存在的话去update重要信息，不存在的话去insert imdb信息
#如果不存在的话，还要用imdb获得imdb信息，然后用sid循环拼接重要信息和imdb信息，然后insert