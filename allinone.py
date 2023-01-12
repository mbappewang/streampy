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
    sql = "select imdb_seid from imdb "
    mycursor.execute(sql)
    db_imdb_seid = mycursor.fetchall()
    for (x,) in db_imdb_seid:
        imdb_seid_list.append(x)

    imdb_sid_list = []
    sql = "select imdb_sid from mac_vod "
    mycursor.execute(sql)
    db_imdb_sid = mycursor.fetchall()
    for (z,) in db_imdb_sid:
        imdb_sid_list.append(z)

    sid_play_dict = {}
    sql = "select imdb_sid,play_url_1,play_url_2 from mac_vod "
    mycursor.execute(sql)
    db_sid_url = mycursor.fetchall()
    for (a,b,c) in db_sid_url:
        sid_play_dict[a] = [b,c]
#获取电影和电视剧的seid/sid/id，与副表的seid判断，只要不在副表的seid，及sid id等信息
    #请求json函数
    def get_vidsrc(url):
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
        requestsite = urllib.request.Request(url,headers=headers)
        data = urllib.request.urlopen(requestsite,timeout=15).read()
        vidsrc_dic = json.loads(data)
        return vidsrc_dic
    def get_ombd(url):
        omdb_info = urllib.request.urlopen(url,timeout=15)
        omdb_info_json = json.loads(omdb_info.read())
        return omdb_info_json
    #获取总页码
    try:
        vidsrc_dict = get_vidsrc("https://vidsrc.me/episodes/latest/page-1.json")
        vidsrc_result = vidsrc_dict["result"]
    except:
        pages = 6000
        print("妹读到页数了×","设定页面默认值为",pages,"页")
    else:
        pages = 6000
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
            vidsrc_dict = get_vidsrc("https://vidsrc.me/episodes/latest/page-" + str(x) + ".json")
        except:
            page_tout_count += 1
        else:
            if len(vidsrc_dict["result"]) != 0:
                no_data_page = 0
                for y in vidsrc_dict["result"]:
                    imdb_id = y["imdb_id"][1:20]
                    season = int(y["season"])
                    episode = int(y["episode"])
                    imdb_sid = imdb_id + str(season)
                    imdb_seid = imdb_id + str(season) + str(episode)
                    play_url_1 = "Episode"+str(episode)+"$"+y["embed_url"]
                    play_url_2 = "Episode"+str(episode)+"$"+"https://www.2embed.to/embed/imdb/tv?id="+"t"+imdb_id+"&s="+str(season)+"&e="+str(episode)
                    if imdb_seid in imdb_seid_list:
                        same_imdb_seid += 1
                    else:
                        same_imdb_seid = 0
                        dif_imdb_seid += 1
                        tv_item += 1
                        #请求OpenAPI拿到imdb信息
                        try:
                            ombd_info = get_ombd("http://www.omdbapi.com/?i="+y["imdb_id"]+"&apikey=57e932e4")
                        except:
                            pass
                        else:
                            #转换unix
                            if ombd_info.get("Released","1 Jan 1970") == "N/A":
                                Unixdate = 0
                            elif ombd_info.get("Released","1 Jan 1970") == "":
                                Unixdate = 0
                            else:
                                date=ombd_info.get("Released","1 Jan 1970")
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
                            if imdb_sid in imdb_sid_list:
                                print("更新season内的episode","目前已发现：",tv_item,"集电视剧")
                                play_url_1_before = (sid_play_dict[imdb_sid])[0]
                                play_url_2_before = (sid_play_dict[imdb_sid])[1]
                                play_url_1= play_url_1+"#"+play_url_1_before
                                play_url_2= play_url_2+"#"+play_url_2_before
                                sid_play_dict[imdb_sid] = [play_url_1,play_url_2]
                                same_sid_url_dict[imdb_sid] = [play_url_1,play_url_2]
                            else:
                                print("添加新season","目前已发现：",tv_item,"集电视剧")
                                vod_name = ombd_info.get("Title","")[0:255]
                                vod_year = ombd_info.get("Year","")[-4:]
                                vod_duration = ombd_info.get("Runtime","1970")[0:10]
                                type_genre = ombd_info.get("Genre","ungenre").split(",")[0][0:10]
                                vod_class = ombd_info.get("Genre","")[0:255]
                                vod_director = ombd_info.get("Director","")[0:255]
                                vod_writer = ombd_info.get("Writer","")[0:255]
                                vod_actor = ombd_info.get("Actors","")[0:255]
                                vod_blurb = vod_content = ombd_info.get("Plot","")[0:255]
                                vod_lang = ombd_info.get("Language","").split(",")[0][0:10]
                                vod_area = ombd_info.get("Country","").split(",")[0][0:20]
                                vod_pic = ombd_info.get("Poster","pic")[0:1024]
                                vod_remarks = "IMDb: " + ombd_info.get("imdbRating","")[0:100]
                                vod_douban_score = vod_score = ombd_info.get("imdbRating","")
                                vod_up = ombd_info.get("imdbVotes","")
                                type = ombd_info.get("Type","untype")
                                vod_pubdate = ombd_info.get("Released","1 Jan 1970")[0:100]
                                vod_time = Unixdate
                                vod_time_add = Unixdate
                                vod_total = ombd_info.get("totalSeasons","")
                                vod_isend = vod_status = 1
                                vod_hits = vod_hits_day = vod_hits_week = vod_hits_month = vod_score_num = random.random()*100
                                group_id = vod_lock = vod_level = vod_copyright = vod_points = vod_points_play = vod_points_down = vod_down = 0
                                vod_play_from_1 = "tpiframe"
                                vod_play_from_2 = "tpiframecopy"
                                vod_play_note = "$$$"
                                vod_play_from = vod_play_from_1+vod_play_note+vod_play_from_2
                                vod_play_server = "no$$$no"
                                mac_vod.append((imdb_id,imdb_sid,imdb_seid,season,play_url_1,play_url_2,vod_name,vod_year,vod_duration,type_genre,vod_class,vod_director,vod_writer,vod_actor,vod_blurb,vod_lang,vod_area,vod_pic,vod_remarks,vod_douban_score,vod_score,vod_up,type,vod_pubdate,vod_time,vod_time_add,vod_total,vod_isend,vod_status,vod_hits,vod_hits_day,vod_hits_week,vod_hits_month,vod_score_num,group_id,vod_lock,vod_play_from,vod_play_server))
                                sid_play_dict[imdb_sid] = [play_url_1,play_url_2]
                                imdb_sid_list.append(imdb_sid)
                        imdb_record.append((imdb_id,imdb_sid,imdb_seid,season,episode))
                        # print("TV爬取进程运行状态>>>","进度：",x/(pages+1)*100,"%","库内集数：",len(imdb_seid_list),"新发现集数：",dif_imdb_seid,"超时次数：",page_tout_count)
            else:
                no_data_page += 1
        if no_data_page == 10:
            print("TV已发现连续10个页面为空，已停止爬取")
            break
        if same_imdb_seid == 100:
            print("TV已发现连续10000条记录为空，已停止爬取")
            break
        endtime = datetime.datetime.now()
        print("TV爬取进程运行状态>>>","%4d" % x,"页已抓取完毕","进度：","%3.2f" % (x/(pages+1)*100),"%","库内TV+MOVIE集数：","%6d" % len(imdb_seid_list),"新发现TV+MOVIE集数：","%6d" % dif_imdb_seid,"超时次数：",page_tout_count)
    sql = "INSERT INTO imdb (imdb_id,imdb_sid,imdb_seid,season,episode) VALUES (%s,%s,%s,%s,%s)"
    val = imdb_record
    mycursor.executemany(sql, val)
    mydb.commit()
    sql = "INSERT INTO mac_vod (imdb_id,imdb_sid,imdb_seid,season,play_url_1,play_url_2,vod_name,vod_year,vod_duration,type_genre,vod_class,vod_director,vod_writer,vod_actor,vod_blurb,vod_lang,vod_area,vod_pic,vod_remarks,vod_douban_score,vod_score,vod_up,type,vod_pubdate,vod_time,vod_time_add,vod_total,vod_isend,vod_status,vod_hits,vod_hits_day,vod_hits_week,vod_hits_month,vod_score_num,group_id,vod_lock,vod_play_from,vod_play_server) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = mac_vod
    mycursor.executemany(sql, val)
    mydb.commit()
    print("TV搞完了，下面是MOVIE")
    for i in same_sid_url_dict:
        sid_url.append(((same_sid_url_dict[i])[0],(same_sid_url_dict[i])[0],i))
    sql = "update mac_vod set play_url_1 = %s,play_url_2 = %s where imdb_sid = %s"
    val = sid_url
    mycursor.executemany(sql, val)
    mydb.commit()
    print("TV搞完了，下面是MOVIE")



# #获取副表的seid存一个tuple
#     imdb_seid_list = []
#     sql = "select imdb_seid from tv_imdb "
#     mycursor.execute(sql)
#     db_imdb_seid = mycursor.fetchall()
#     for (x,) in db_imdb_seid:
#         imdb_seid_list.append(x)
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
        pages = 1200
        print("妹读到页数了×","设定页面默认值为",pages,"页")
    else:
        pages = vidsrc_dict["pages"]
        print("读到页数了✅","共",pages,"页")
    #生成pagelist
    page_tout_count = 0
    vidsrc_result=[]
    same_imdb_seid = 0
    no_data_page = 0
    del mac_vod
    del imdb_record
    dif_imdb_seid = 0
    mac_vod = []
    imdb_record=[]
    movie_item = 0
    for x in range(1,pages+1):
        #避免程序超时，用try、except
        try:
            #请求函数获得接口页信息
            vidsrc_dict = get_vidsrc("https://vidsrc.me/movies/latest/page-" + str(x) + ".json")
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
                    play_url_1 = "Source-1"+"$"+y["embed_url"]
                    play_url_2 = "Source-2"+"$"+"https://www.2embed.to/embed/imdb/movie?id="+"tt"+imdb_id[1:20]
                    if imdb_seid in imdb_seid_list:
                        same_imdb_seid += 1
                        # print("TV爬取进程运行状态>>>","进度：",x/(pages+1)*100,"%","库内集数：",len(imdb_seid_list),"新发现集数：",dif_imdb_seid,"超时次数：",page_tout_count)
                    else:
                        same_imdb_seid = 0
                        dif_imdb_seid += 1
                        movie_item += 1
                        #请求OpenAPI拿到imdb信息
                        try:
                            ombd_info = get_ombd("http://www.omdbapi.com/?i="+y["imdb_id"]+"&apikey=57e932e4")
                        except:
                            pass
                        else:
                            #转换unix
                            if ombd_info.get("Released","1 Jan 1970") == "N/A":
                                Unixdate = 0
                            else:
                                date=ombd_info.get("Released","1 Jan 1970")
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
                            if imdb_sid in imdb_sid_list:
                                print("更新了movie","目前已发现：",movie_item,"部电影")
                                play_url_1_before = (sid_play_dict[imdb_sid])[0]
                                play_url_2_before = (sid_play_dict[imdb_sid])[1]
                                play_url_1= play_url_1+"#"+play_url_1_before
                                play_url_2= play_url_2+"#"+play_url_2_before
                                sid_play_dict[imdb_sid] = [play_url_1,play_url_2]
                                same_sid_url_dict[imdb_sid] = [play_url_1,play_url_2]
                            else:
                                print("添加新movie","目前已发现：",movie_item,"部电影")
                                vod_name = ombd_info.get("Title","")[0:255]
                                vod_year = ombd_info.get("Year","")[-4:]
                                vod_duration = ombd_info.get("Runtime","1970")[0:10]
                                type_genre = ombd_info.get("Genre","ungenre").split(",")[0][0:10]
                                vod_class = ombd_info.get("Genre","")[0:255]
                                vod_director = ombd_info.get("Director","")[0:255]
                                vod_writer = ombd_info.get("Writer","")[0:255]
                                vod_actor = ombd_info.get("Actors","")[0:255]
                                vod_blurb = vod_content = ombd_info.get("Plot","")[0:255]
                                vod_lang = ombd_info.get("Language","").split(",")[0][0:10]
                                vod_area = ombd_info.get("Country","").split(",")[0][0:20]
                                vod_pic = ombd_info.get("Poster","pic")[0:1024]
                                vod_remarks = "IMDb: " + ombd_info.get("imdbRating","")[0:100]
                                vod_douban_score = vod_score = ombd_info.get("imdbRating","")
                                vod_up = ombd_info.get("imdbVotes","")
                                type = ombd_info.get("Type","untype")
                                vod_pubdate = ombd_info.get("Released","1 Jan 1970")[0:100]
                                vod_time = Unixdate
                                vod_time_add = Unixdate
                                vod_total = ombd_info.get("totalSeasons","")
                                vod_isend = vod_status = 1
                                vod_hits = vod_hits_day = vod_hits_week = vod_hits_month = vod_score_num = random.random()*100
                                group_id = vod_lock = vod_level = vod_copyright = vod_points = vod_points_play = vod_points_down = vod_down = 0
                                vod_play_from_1 = "tpiframe"
                                vod_play_from_2 = "tpiframecopy"
                                vod_play_note = "$$$"
                                vod_play_from = vod_play_from_1+vod_play_note+vod_play_from_2
                                vod_play_server = "no$$$no"
                                mac_vod.append((imdb_id,imdb_sid,imdb_seid,season,play_url_1,play_url_2,vod_name,vod_year,vod_duration,type_genre,vod_class,vod_director,vod_writer,vod_actor,vod_blurb,vod_lang,vod_area,vod_pic,vod_remarks,vod_douban_score,vod_score,vod_up,type,vod_pubdate,vod_time,vod_time_add,vod_total,vod_isend,vod_status,vod_hits,vod_hits_day,vod_hits_week,vod_hits_month,vod_score_num,group_id,vod_lock,vod_play_from,vod_play_server))
                                sid_play_dict[imdb_sid] = [play_url_1,play_url_2]
                                imdb_sid_list.append(imdb_sid)
                        imdb_record.append((imdb_id,imdb_sid,imdb_seid,season,episode))
                        # print("TV爬取进程运行状态>>>","进度：",x/(pages+1)*100,"%","库内集数：",len(imdb_seid_list),"新发现集数：",dif_imdb_seid,"超时次数：",page_tout_count)
            else:
                no_data_page += 1
        if no_data_page == 10:
            print("Movie已发现连续10个页面为空，已停止爬取")
            break
        if same_imdb_seid == 100:
            print("Movie已发现连续10000条记录为空，已停止爬取")
            break
        endtime = datetime.datetime.now()
        print("Movie爬取进程运行状态>>>","%4d" % x,"页已抓取完毕","进度：","%4.2f" % (x/(pages+1)*100),"%","库内TV+MOVIE集数：",len(imdb_seid_list),"新发现TV+MOVIE集数：",dif_imdb_seid,"超时次数：",page_tout_count,"已运行时间：",endtime - starttime)
    sql = "INSERT INTO imdb (imdb_id,imdb_sid,imdb_seid,season,episode) VALUES (%s,%s,%s,%s,%s)"
    val = imdb_record
    mycursor.executemany(sql, val)
    mydb.commit()
    sql = "INSERT INTO mac_vod (imdb_id,imdb_sid,imdb_seid,season,play_url_1,play_url_2,vod_name,vod_year,vod_duration,type_genre,vod_class,vod_director,vod_writer,vod_actor,vod_blurb,vod_lang,vod_area,vod_pic,vod_remarks,vod_douban_score,vod_score,vod_up,type,vod_pubdate,vod_time,vod_time_add,vod_total,vod_isend,vod_status,vod_hits,vod_hits_day,vod_hits_week,vod_hits_month,vod_score_num,group_id,vod_lock,vod_play_from,vod_play_server) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = mac_vod
    mycursor.executemany(sql, val)
    mydb.commit()


    # #获取副表有而主表没有的sid，进行insert into 主表操作
    # dif_imdb_sid_list = []
    # sql = "select imdb_sid,imdb_id,season,GROUP_CONCAT(play_url_1 order by imdb_sid asc separator '#') from mydatabase.tv_imdb group by imdb_sid where imdb_sid "
    # mycursor.execute(sql)
    # db_imdb_seid = mycursor.fetchall()
    # for (z,) in db_imdb_seid:
    #     dif_imdb_sid_list.append(z)

    # sql = "update mac_vod, " 










#判断sid是否存在，存在的话去update重要信息，不存在的话去insert imdb信息
#如果不存在的话，还要用imdb获得imdb信息，然后用sid循环拼接重要信息和imdb信息，然后insert