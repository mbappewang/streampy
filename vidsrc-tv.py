# -*- coding: utf-8 -*-
#导入模块
import json
import time
import datetime
import urllib.request
import random
import mysql.connector
#尝试连接mysql
try:
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd='walc94511',
    database="localtest"
    )
    mycursor = mydb.cursor()
except:
    print("连接msql失败")
else:
    #设定默认值
    item = page_tout_count = same_season = same_episode = 0
    p = pages = 1
    vidsrc_vod_list=[]
    page_timeout_list=[]
    page_list=[]
    imdb_seid_list=[]
    elist=[]
    #请求json函数
    def get_vidsrc(url):
        headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
        requestsite = urllib.request.Request(url,headers=headers)
        data = urllib.request.urlopen(requestsite,timeout=15).read()
        vidsrc_dic = json.loads(data)
        return vidsrc_dic
    #获取初始页码值
    try:
        vidsrc_dict = get_vidsrc("https://vidsrc.me/episodes/latest/page-1.json")
        vidsrc_result = vidsrc_dict["result"]
    except:
        print("没有读到页码！！！！！！！！")
        pages = 6000
    else:
        print("读到页数了")
        pages = 6000
    print("总页数：",pages)
    #生成pagelist
    while p <= pages:
        page_list.append(p)
        p += 1
    #不抓干净不停抓
    while page_list != []:
        #翻页循环
        for p in page_list:
            sleeptime = random.random() * 2 + 1
            print(">>>>>>>>>>>>>>>","随喜休息：",round(sleeptime,2),"<<<<<<<<<<<<<<<<")
            time.sleep(sleeptime)
            #避免程序超时，用try、except
            try:
                #请求函数获得接口页信息
                vidsrc_dict = get_vidsrc("https://vidsrc.me/episodes/latest/page-" + str(p) + ".json")
            except:
                mycursor.execute("SELECT imdb_sid FROM mac_vod_tv")
                imbd_sid_tuple = mycursor.fetchall()
                imdb_sid_list = []
                for (y,) in imbd_sid_tuple:
                    imdb_sid_list.append("tt"+y)
                print("请求↓失败")
                page_tout_count += 1
                print("超时页记录：",page_timeout_list,"超时了","目前条数：",item,"目前页数",p,"超时次数：",page_tout_count,"已发现重复season：",same_season,"已发现重复episode：",same_episode,"库内最新季数：",len(imdb_sid_list),"库内最新集数：",len(imdb_seid_list))
                if p in page_timeout_list:
                    print("第",p,"页重试再次超时")
                else:
                    page_timeout_list.append(p)
            else:
                print("请求↑成功")
                #将接口的json文件中的result字段取出
                vidsrc_result = vidsrc_dict["result"]
                for z in vidsrc_result:
                    item += 1
                    imdb_id = z.get("imdb_id","tt0")
                    episode_vidsrc = z.get("episode","")
                    season_vidsrc = z.get("season","")
                    imdb_seid = imdb_id+season_vidsrc+episode_vidsrc
                    imdb_sid = imdb_id+season_vidsrc
                    mycursor.execute("SELECT imdb_sid FROM mac_vod_tv")
                    imbd_sid_tuple = mycursor.fetchall()
                    imdb_sid_list = []
                    for (y,) in imbd_sid_tuple:
                        imdb_sid_list.append("tt"+y)
                    #读imdb表，获取imdb_seid信息
                    mycursor.execute("SELECT imdb_seid FROM imdb")
                    etuple = mycursor.fetchall()
                    elist = []
                    for (a,) in etuple:
                        elist.append("tt"+a)
                    if imdb_seid in elist:#判断是否重复"episode"
                        same_episode += 1
                        print("发现重复episode记录，不录入")
                    else:
                        if imdb_sid in imdb_sid_list:#判断是否重复season
                            same_season += 1
                            print("同季发现新的一集")
                            mycursor.execute('SELECT play_url_1 FROM mac_vod_tv WHERE imdb_sid ="'+imdb_sid[2:20]+'"')
                            url = mycursor.fetchall()
                            url_vidsrc = "Episode" + episode_vidsrc + "$" + z.get("embed_url","")
                            for (d,) in url:
                                url1 = d
                            play_url_1 = url1 + "#" + url_vidsrc
                            sql = "UPDATE mac_vod_tv SET play_url_1 = %s WHERE imdb_sid = %s"
                            val = (play_url_1, imdb_sid[2:20])
                            mycursor.execute(sql, val)
                            mydb.commit()
                            sql = "INSERT INTO imdb (imdb_sid,imdb_seid) VALUES (%s ,%s)"
                            val = (imdb_sid[2:20],imdb_seid[2:20])
                            mycursor.execute(sql, val)
                            mydb.commit()
                        else:
                            print("新的一季的新的一集")
                            title_vidsrc = z.get("show_title","")
                            url_vidsrc = "Episode" + episode_vidsrc + "$" + z.get("embed_url","")
                            vidsrc_vod_info = (imdb_id[2:20],imdb_seid[2:20],imdb_sid[2:20],title_vidsrc,season_vidsrc,url_vidsrc)
                            #将遍历的信息存储进列表中备用
                            sql = "INSERT INTO mac_vod_tv (imdb_id,imdb_seid,imdb_sid,vod_name,vod_serial,play_url_1) VALUES (%s ,%s , %s, %s, %s, %s)"
                            val = vidsrc_vod_info
                            mycursor.execute(sql, val)
                            mydb.commit()
                            sql = "INSERT INTO imdb (imdb_sid,imdb_seid) VALUES (%s ,%s)"
                            val = (imdb_sid[2:20],imdb_seid[2:20])
                            mycursor.execute(sql, val)
                            mydb.commit()

                        # vidsrc_vod_list.append(vidsrc_vod_info)
                # savelist = open("vidsrc-TV-infolist.txt","w",encoding='utf-8')
                # savelist.write(json.dumps(vidsrc_vod_list))
                # savelist.close
                mycursor.execute("SELECT imdb_sid FROM mac_vod_tv")
                imbd_sid_tuple = mycursor.fetchall()
                imdb_sid_list = []
                for (y,) in imbd_sid_tuple:
                    imdb_sid_list.append("tt"+y)
                page_list.remove(p)
                print("超时页记录：",page_timeout_list,"没有超时","目前条数：",item,"目前页数",p,"超时次数：",page_tout_count,"已发现重复season：",same_season,"已发现重复episode：",same_episode,"库内最新季数：",len(imdb_sid_list),"库内最新集数：",len(elist))
                if p in page_timeout_list:
                    print("第",p,"页重试成功")
                    page_timeout_list.remove(p)