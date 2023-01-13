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
try:
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd='walc94511',
    database="mac_vod"
    )
    mycursor = mydb.cursor()
except:
    print("连接数据库失败×")
else:
    print("连接数据库成功✅")
#根据主表记录，清掉副表所有的不存在于主表的sid
    sql = "select id,vod_name,play_url_1,season,episode from imdb_8t where imdb_sid is null"
    mycursor.execute(sql)
    imdb_8db = mycursor.fetchall()
    a=0
    basic_info=[]
    for (x,y,z,b,c) in imdb_8db:
        imdb_id = "t"+x[2:20]
        vod_name = y[:-4]
        season = b
        episode = c
        play_url_1 = "Episode"+str(c)+"$"+z
        imdb_sid = imdb_id+str(b)
        imdb_seid = imdb_sid+str(c)
        basic_info = [vod_name,play_url_1,imdb_sid,imdb_seid,x,b,c]
        sql = "update imdb_8t set vod_name = %s,play_url_1 = %s,imdb_sid = %s,imdb_seid = %s where id = %s and season =%s and episode =%s"
        val= basic_info
        mycursor.execute(sql, val)
        mydb.commit()
        a+=1
        print(a)

    sql = "select imdb_sid from mac_vod"
    mycursor.execute(sql)
    imdb_macvod = mycursor.fetchall()
    a=0
    sql = "SELECT distinct imdb_sid,group_concat(distinct vod_name),group_concat(distinct id),group_concat(play_url_1 order by episode desc separator '#') FROM imdb_8t where imdb_sid is not null group by imdb_sid"
    mycursor.execute(sql)
    imdb_8db = mycursor.fetchall()
    for (x,y,z,b) in imdb_8db:
        imdb_sid = x
        if (imdb_sid,) in imdb_macvod:
            a+=1
            print("已有",a)
        else:
            vod_name = y
            vod_play_url = b
            play_url_1 = b
            type_id_1=94
            type_id=109
            vod_status=1
            vod_isend=1
            group_id = vod_lock = vod_level = vod_copyright = vod_points = vod_points_play = vod_points_down = vod_down = 0
            vod_play_note = "$$$"
            vod_play_from = "tpiframe"
            vod_play_server = "no$$$no"
            try:
                ombd_info = get_ombd("http://www.omdbapi.com/?i="+z+"&apikey=57e932e4")
            except:
                pass
            else:
                #转换unix
                if ombd_info.get("Released","1 Jan 1970") == "N/A":
                    Unixdate = 0
                elif ombd_info.get("Released","1 Jan 1970") == "N":
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
                if ombd_info.get("Released","1 Jan 1970") == "N/A":
                    pass
                elif ombd_info.get("Released","1 Jan 1970") == "":
                    pass
                else:
                    vod_year = ombd_info.get("Released","1 Jan 1970")[-4:]
                vod_duration = ombd_info.get("Runtime","0")[0:10]
                type_genre = ombd_info.get("Genre","ungenre").split(",")[0][0:15]
                vod_class = ombd_info.get("Genre","")[0:255]
                vod_director = ombd_info.get("Director","")[0:255]
                vod_writer = ombd_info.get("Writer","")[0:255]
                vod_actor = ombd_info.get("Actors","")[0:255]
                vod_blurb = vod_content = ombd_info.get("Plot","")[0:255]
                vod_lang = ombd_info.get("Language","").split(",")[0][0:10]
                vod_area = ombd_info.get("Country","").split(",")[0][0:20]
                vod_pic = ombd_info.get("Poster","pic")[0:1024]
                vod_remarks = "IMDb: " + ombd_info.get("imdbRating","")[0:100]
                if ombd_info.get("imdbRating","") =="N/A":
                    vod_douban_score = vod_score = 0.0
                else:
                    vod_douban_score = vod_score = ombd_info.get("imdbRating",0.0)
                vod_up = ombd_info.get("imdbVotes","")
                vod_pubdate = ombd_info.get("Released","1 Jan 1970")[0:100]
                vod_time = Unixdate
                vod_time_add = Unixdate
                vod_hits = vod_hits_day = vod_hits_week = vod_hits_month = vod_score_num = random.random()*100
                basic_info = [vod_year,vod_duration,type_genre,vod_class,vod_director,vod_writer,vod_actor,vod_blurb,vod_content,vod_lang,vod_area,vod_pic,vod_remarks,vod_douban_score,vod_score,vod_up,vod_pubdate,vod_time,vod_time_add,vod_hits,vod_hits_day,vod_hits_week,vod_hits_month,vod_score_num,vod_play_url,imdb_sid,vod_name,play_url_1,type_id_1,type_id,vod_status,vod_isend,group_id,vod_lock,vod_level,vod_copyright,vod_points,vod_points_play,vod_points_down,vod_down,vod_play_note,vod_play_from,vod_play_server]
                sql = "insert into mac_vod (vod_year,vod_duration,type_genre,vod_class,vod_director,vod_writer,vod_actor,vod_blurb,vod_content,vod_lang,vod_area,vod_pic,vod_remarks,vod_douban_score,vod_score,vod_up,vod_pubdate,vod_time,vod_time_add,vod_hits,vod_hits_day,vod_hits_week,vod_hits_month,vod_score_num,vod_play_url,imdb_sid,vod_name,play_url_1,type_id_1,type_id,vod_status,vod_isend,group_id,vod_lock,vod_level,vod_copyright,vod_points,vod_points_play,vod_points_down,vod_down,vod_play_note,vod_play_from,vod_play_server) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                val= basic_info
                mycursor.execute(sql, val)
                mydb.commit()
                a+=1
                print(a,"记录添加中")

    sql = "select imdb_sid,vod_name from mac_vod where vod_letter is null"
    mycursor.execute(sql)
    imdb_8db = mycursor.fetchall()
    a=0
    for (x,y) in imdb_8db:
        vod_en=''.join(char for char in y if char.isalnum())
        vod_sub=''.join(char for char in y if char.isalnum())
        vod_letter=vod_en[0:1].upper()
        basic_info = [vod_en,vod_sub,vod_letter,x]
        sql = "update mac_vod set vod_en = %s,vod_sub = %s,vod_letter = %s where imdb_sid = %s"
        val= basic_info
        mycursor.execute(sql, val)
        mydb.commit()
        a+=1
        print(a,"首字母写入中")
    sql = "select imdb_sid,type_genre from mac_vod where type_id_1 =93 and type_id = 140"
    mycursor.execute(sql)
    imdb_8db = mycursor.fetchall()
    a=0
    movie_genre_dict={'Comedy': 122, 'Short': 123, 'Adventure': 124, 'Romance': 125, 'Drama': 128, 'Action': 129, 'Crime': 130, 'Western': 131, 'Documentary': 132, 'Horror': 133, 'Fantasy': 134, 'Biography': 135, 'History': 136, 'Animation': 137, 'Music': 139, 'N/A': 140, 'ungenre': 140, 'Mystery': 138, 'Musical': 141, 'Sci-Fi': 142, 'Family': 143, 'Film-Noir': 144, 'War': 145, 'Thriller': 146, 'Adult': 147, 'News': 151, 'Sport': 152, 'Talk-Show': 150, 'Reality-TV': 148, 'Game-Show': 149}
    for (x,y) in imdb_8db:
        type_id = movie_genre_dict[y]
        basic_info = [type_id,x]
        sql = "update mac_vod set type_id = %s where imdb_sid = %s"
        val= basic_info
        mycursor.execute(sql, val)
        mydb.commit()
        a+=1
        print(a,"分类中")





#访问vidsrc，添加进副表，获得新sid和旧sid

#新的sid进行sql语句合并insert到主表

#针对新的sid，去除其中的id，请求omdb获得信息update

#omdb无法覆盖的信息，sub genre记入other，名字保留vidsrc的名字

#旧的sid进行sql语句合并uodate到主表