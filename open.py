# -*- coding: utf-8 -*-
#导入模块
import json
import time
import datetime
import urllib.request
import random
import mysql.connector
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
    #设置默认值
    item = page_tout_count = same = 0
    p = pages = 1
    vidsrc_vod_list=[]
    page_timeout_list=[]
    page_list=[]
    #请求json函数
    def get_ombd(url):
        omdb_info = urllib.request.urlopen(url,timeout=15)
        omdb_info_json = json.loads(omdb_info.read())
        return omdb_info_json
    #查询mysql，获得imdb_id
    mycursor.execute("SELECT imdb_id FROM mac_vod")
    movie_imdb_tuple = mycursor.fetchall()
    movie_imdb_list = []
    for (a,) in movie_imdb_tuple:
        movie_imdb_list.append("tt"+a)
    while movie_imdb_list != []:
        for movie_imdb in movie_imdb_list:
            try:
                movie_info_json = get_ombd("http://www.omdbapi.com/?i="+movie_imdb+"&apikey=57e932e4")
            except:
                print("获取info失败")
            else:
                if "Error" in movie_info_json:
                    print("有error")
                else:
                    print("无error")
                    if movie_info_json.get("Released","1 Jan 1970") == "N/A":
                        Unixdate = 0
                    else:
                        date=movie_info_json.get("Released","1 Jan 1970")
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
                    vod_name = movie_info_json.get("Title","")[0:255]
                    vod_year = movie_info_json.get("Year","")[0:10]
                    vod_duration = movie_info_json.get("Runtime","1970")[0:10]
                    type_genre = movie_info_json.get("Genre","ungenre").split(",")[0][0:10]
                    vod_class = movie_info_json.get("Genre","")[0:255]
                    vod_director = movie_info_json.get("Director","")[0:255]
                    vod_writer = movie_info_json.get("Writer","")[0:255]
                    vod_actor = movie_info_json.get("Actors","")[0:255]
                    vod_blurb = vod_content = movie_info_json.get("Plot","")[0:255]
                    vod_lang = movie_info_json.get("Language","").split(",")[0][0:10]
                    vod_area = movie_info_json.get("Country","").split(",")[0][0:20]
                    vod_pic = movie_info_json.get("Poster","pic")[0:1024]
                    vod_remarks = "IMDb: " + movie_info_json.get("imdbRating")[0:100]
                    vod_douban_score = vod_score = movie_info_json.get("imdbRating")
                    vod_up = movie_info_json.get("imdbVotes","")
                    type = movie_info_json.get("Type","untype")
                    vod_pubdate = movie_info_json.get("Released","1 Jan 1970")[0:100]
                    vod_time = Unixdate
                    vod_time_add = Unixdate
                    vod_total = movie_info_json.get("totalSeasons","")
                    vod_isend = vod_status = 1
                    vod_hits = vod_hits_day = vod_hits_week = vod_hits_month = vod_score_num = random.random()*100
                    group_id = vod_lock = vod_level = vod_copyright = vod_points = vod_points_play = vod_points_down = vod_down = 0
                    vod_play_from_1 = "tpiframe"
                    vod_play_from_2 = "tpiframecopy"
                    vod_play_note = "$$$"
                    vod_play_from = vod_play_from_1+vod_play_note+vod_play_from_2
                    vod_play_server = "no$$$no"
                    if movie_info_json["Type"] == "movie":
                        moviegenredict = {'Romance': 125, 'Adventure': 124, 'Short': 123, 'Comedy': 122, 'Drama': 128, 'Action': 129, 'Crime': 130, 'Western': 131, 'Documentary': 132, 'Horror': 133, 'Fantasy': 134, 'Biography': 135, 'History': 136, 'Animation': 137, 'Mystery': 138, 'Music': 139, 'Other': 140, 'Musical': 141, 'Sci-Fi': 142, 'Family': 143, 'Film-Noir': 144, 'War': 145, 'Thriller': 146, 'Adult': 147, 'Reality-TV': 148, 'Game-Show': 149, 'Talk-Show': 150, 'News': 151, 'Sport': 152} 
                        type_id = moviegenredict[type_genre]
                        type_id_1 = 93
                    else:
                        tvgenredict = {'Romance': 126, 'Sport': 121, 'News': 120, 'Talk-Show': 119, 'Music': 108, 'Other': 109, 'Musical': 110, 'Game-Show': 118, 'Reality-TV': 117, 'Adult': 116, 'Thriller': 115, 'War': 114, 'Film-Noir': 113, 'Family': 112, 'Sci-Fi': 111, 'Mystery': 107, 'Animation': 106, 'History': 105, 'Biography': 104, 'Fantasy': 103, 'Horror': 102, 'Documentary': 101, 'Western': 100, 'Crime': 99, 'Action': 98, 'Adventure': 97, 'Comedy': 95, 'Short': 96, 'Drama': 127}
                        type_id = tvgenredict[type_genre]
                        type_id_1 = 94
                    movie_info_tuple = (
                        vod_name,
                        vod_year,
                        vod_duration,
                        type_id,
                        vod_class,
                        vod_director,
                        vod_writer,
                        vod_actor,
                        vod_blurb,
                        vod_lang,
                        vod_area,
                        vod_pic,
                        vod_remarks,
                        vod_douban_score,
                        vod_score,
                        vod_up,
                        type_id_1,
                        vod_pubdate,
                        vod_time,
                        vod_time_add,
                        vod_total,
                        vod_isend,
                        vod_status,
                        vod_hits,
                        vod_hits_day,
                        vod_hits_week,
                        vod_hits_month,
                        vod_score_num,
                        group_id,
                        vod_lock,
                        vod_play_from
                    )
                    sql = "INSERT INTO mac_vod (vod_name,vod_year,vod_duration,type_id,vod_class,vod_director,vod_writer,vod_actor,vod_blurb,vod_lang,vod_area,vod_pic,vod_remarks,vod_douban_score,vod_score,vod_up,type_id_1,vod_pubdate,vod_time,vod_time_add,vod_total,vod_isend,vod_status,vod_hits,vod_hits_day,vod_hits_week,vod_hits_month,vod_score_num,group_id,vod_lock,vod_play_from) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    val = movie_info_tuple
                    mycursor.execute(sql, val)
                    mydb.commit()
                    