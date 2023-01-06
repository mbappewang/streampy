import json
import urllib.request
import time
import datetime
import eventlet#导入eventlet这个模块
eventlet.monkey_patch()#必须加这条代码
starttime = datetime.datetime.now()
print("*************************")
mac_vod_list = []
b=0
p=1
imdb_id_list=[]
imdb_sid_list=[]
imdb_seid_list=[]
f = open("imdb_seid.txt", "r")
for l in f:
    imdb_seid_list.append(l[:-1])
f.close()
e = open("imdb_sid.txt", "r")
for l in e:
    imdb_sid_list.append(l[:-1])
e.close()
def get_imdb_id(rurl):#读json文件
    vidsrc_json_1={"result":[{"imdb_id":"tt15472320","show_title":"The Secret Life of Lighthouses 2020","season":"1","episode":"3","embed_url":"https:\/\/vidsrc.me\/embed\/tt15472320\/1-3\/"}],"pages":1}
    with eventlet.Timeout(14,False):#设置超时时间为2秒
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}#αװ����
        url = urllib.request.Request(url=rurl, headers=headers)
        vidsrc = urllib.request.urlopen(url,timeout=15).read()
        vidsrc_json_1 = json.loads(vidsrc)
        print("vidsrc未超时")
    return vidsrc_json_1
def get_omdb_info(url):
    omdb_info_json={}
    with eventlet.Timeout(14,False):#
        omdb_info = urllib.request.urlopen(url,timeout=15)
        omdb_info_json = json.loads(omdb_info.read())
        print("open未超时")
    return omdb_info_json#用imdbid�???omdb的imdb的信�???
page = 300000
while p <= page:
    rurl = "https://vidsrc.me/episodes/latest/page-" + str(p) + ".json"
    vidsrc_json_1 = get_imdb_id(rurl)
    vidsrc_json_2 = vidsrc_json_1.get("result","")
    b=0
    for x in vidsrc_json_2:
        endtime = datetime.datetime.now()
        b += 1
        print("翻页进度:",p,"/",page,"本页进度�?",b,"/",50,endtime - starttime)
        imdb_seid = x.get("imdb_id","")+x.get("season","")+x.get("episode","")
        imdb_sid = x.get("imdb_id","")+x.get("season","")
        imdb_id = x.get("imdb_id","")
        if imdb_seid in imdb_seid_list:
            print("------------------------------------------------------------------------------------有重复episode录入")
        else:
            print("------------------------无重复集录入")
            vidsrc_url = x.get("embed_url","")
            season = x.get("season","")
            episode = x.get("episode","")
            if imdb_sid in imdb_sid_list:
                print("******************************************************************有重复season")
                for a in mac_vod_list:
                    c = a["vod_id"]
                    if c == imdb_sid[2:16]:
                        url=url1=url2='bill'
                        url1=str(a["url1"])+"#episode"+episode+"$"+vidsrc_url
                        url2=str(a["url2"])+"#episode"+episode+"$"+"https://www.2embed.to/embed/imdb/tv?id="+imdb_id+"&s="+season+"&e="+episode
                        url=url1 + '$$$' + url2
                        a["url1"]=url1
                        a["url2"]=url2
                        a["vod_play_url"]=url
                        y=json.dumps(mac_vod_list,indent=4)
                        mac_vod={"code":1,"msg":"数据列表","page":1,"pagecount":1,"limit":"3","total":3}
                        mac_vod["list"]=mac_vod_list
                        y=json.dumps(mac_vod,indent=4)
                        f = open("tV.json", "w")
                        f.write(y)
                        f.close
                        f = open("tV.json","r")
                        print("录入了新的一集",url)
                        imdb_seid_list.append(imdb_seid)
                        f=open("imdb_seid.txt","w")
                        for line in imdb_seid_list:
                            f.write(line + "\n")
                        f.close()
            else:
                print("************************无重复季")
                omdb_url = "http://www.omdbapi.com/?i="+imdb_id+"&apikey=57e932e4"
                omdb_info_json = get_omdb_info(omdb_url)
                print("重复季集判断结束")
                if "Error" in omdb_info_json:
                    print("有error")
                else:
                    print("无error")
                    if omdb_info_json.get("Released","1 Jan 1970") == "N/A":
                        Unixdate = 0
                    else:
                        date=omdb_info_json.get("Released","1 Jan 1970")
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
                    print("录入了新的一季",imdb_id,omdb_info_json["Title"])
                    url=url1=url2='a'
                    url1="episode"+episode+"$"+vidsrc_url
                    url2="episode"+episode+"$"+"https://www.2embed.to/embed/imdb/tv?id="+imdb_id+"&s="+season+"&e="+episode
                    url=str(url1) + "$$$" + str(url2)
                    omdb_vod_info = {
                        "vod_id":imdb_sid[2:16],
                        "vod_name":omdb_info_json.get("Title","")[0:255],
                        "type_id":omdb_info_json["Genre"].split(",")[0][0:10],
                        "type_name":omdb_info_json["Genre"].split(",")[0][0:10],
                        "type_id_1":omdb_info_json["Type"][0:10],
                        "vod_blurb":omdb_info_json["Plot"][0:255],
                        "vod_en":omdb_info_json["Title"][0:255],
                        "vod_status":1,
                        "vod_letter":omdb_info_json["Title"][0:1],
                        "vod_color":"",
                        "vod_sub":"",
                        "vod_tag":"",
                        "vod_class":omdb_info_json["Genre"][0:255],
                        "vod_pic":omdb_info_json["Poster"][0:1024],
                        "vod_pic_thumb":"",
                        "vod_pic_slide":"",
                        "vod_pic_screenshot":"",
                        "vod_actor":omdb_info_json["Actors"][0:255],
                        "vod_director":omdb_info_json["Director"][0:255],
                        "vod_writer":omdb_info_json["Writer"][0:100],
                        "vod_behind":"",
                        "vod_remarks":"IMDb:"+omdb_info_json["imdbRating"][0:100],
                        "vod_pubdate":(omdb_info_json["Released"][0:100]),
                        "vod_total":"",
                        "vod_serial":"",
                        "vod_tv":"",
                        "vod_weekday":"",
                        "vod_area":omdb_info_json["Country"].split(",")[0][0:20],
                        "vod_lang":omdb_info_json["Language"].split(",")[0][0:10],
                        "vod_year":omdb_info_json["Year"][0:10],
                        "vod_version":"",
                        "vod_state":"",
                        "vod_author":"",
                        "vod_jumpurl":"",
                        "vod_tpl":"",
                        "vod_tpl_play": "",
                        "vod_tpl_down": "",
                        "vod_isend": 0,
                        "vod_lock": 0,
                        "vod_level": 0,
                        "vod_copyright": 0,
                        "vod_points": 0,
                        "vod_points_play": 0,
                        "vod_points_down": 0,
                        "vod_hits":omdb_info_json["imdbVotes"][0:8],
                        "vod_hits_day":omdb_info_json["imdbVotes"][0:8],
                        "vod_hits_week":omdb_info_json["imdbVotes"][0:8],
                        "vod_hits_month":omdb_info_json["imdbVotes"][0:8],
                        "vod_duration":omdb_info_json["Runtime"][0:10],
                        "vod_up":omdb_info_json["imdbVotes"][0:8],
                        "vod_down":"",
                        "vod_score":omdb_info_json["imdbRating"],
                        "vod_score_all":omdb_info_json["imdbVotes"][0:8],
                        "vod_score_num":omdb_info_json["imdbVotes"][0:8],
                        "vod_time":Unixdate,
                        "vod_time_add":Unixdate,
                        "vod_time_hits": 0,
                        "vod_time_make": 0,
                        "group_id": 0,
                        "vod_trysee": 0,
                        "vod_douban_id":"",
                        "vod_douban_score":omdb_info_json["imdbRating"],
                        "vod_reurl": "",
                        "vod_rel_vod": "",
                        "vod_rel_art": "",
                        "vod_pwd": "",
                        "vod_pwd_url": "",
                        "vod_pwd_play": "",
                        "vod_pwd_play_url": "",
                        "vod_pwd_down": "",
                        "vod_pwd_down_url": "",
                        "vod_content":omdb_info_json["Plot"][0:16777216],
                        "vod_play_server": "no$$$no",
                        "vod_play_note": "$$$",
                        "vod_down_from": "",
                        "vod_down_server": "",
                        "vod_down_note": "",
                        "vod_down_url": "",
                        "vod_plot": "",
                        "vod_plot_name": ""[0:16777216],
                        "vod_plot_detail": ""[0:16777216],
                        "vod_play_from": "tpiframe$$$tpiframecopy",
                        "url1":url1,
                        "url2":url2,
                        "vod_play_url":url
                        }
                    imdb_sid_list.append(imdb_sid)
                    e=open("imdb_sid.txt","w")
                    for line1 in imdb_sid_list:
                        e.write(line1 + "\n")
                    e.close()

                    imdb_seid_list.append(imdb_seid)
                    f=open("imdb_seid.txt","w")
                    for line in imdb_seid_list:
                        f.write(line + "\n")
                    f.close()

                    mac_vod_list.append(omdb_vod_info)#字典套字典，准�?�拼json
                    y=json.dumps(mac_vod_list,indent=4)#将python�??为json
                    mac_vod={"code":1,"msg":"数据列表","page":1,"pagecount":1,"limit":"3","total":3}
                    mac_vod["list"]=mac_vod_list
                    y=json.dumps(mac_vod,indent=4)#将python�??为json
                    f = open("tV.json", "w")
                    f.write(y)
                    f.close
        print("@@@@@@@@@@@@@@@@@@@@@本条结束")
    p += 1

# for x in vidsrc_json_2:
#     imdb_id = x["imdb_id"]#通过json文件查imdbid
#     vidsrc_url = x["embed_url"]
#     season = x["season"]
#     episode = x["episode"]
#     omdb_url = "http://www.omdbapi.com/?i="+imdb_id+"&apikey=57e932e4"#拼omdb查url
#     def get_omdb_info(url):
#         omdb_info = urllib.request.urlopen(url)
#         omdb_info_json = json.loads(omdb_info.read())
#         return omdb_info_json#用imdbid查omdb的imdb的信�?
#     omdb_info_json = get_omdb_info(omdb_url)#获得imdb的信�?
#     #新建字典，键的名字同mysql表的名，然后将imdb信息传给字典
#     # print(omdb_info_json)
#     if omdb_info_json["Released"] != "N/A":
#         date=omdb_info_json["Released"]
#         y=date[-4:]
#         M=date.split(" ")[1]
#         month_list = ['月份','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
#         m=str(month_list.index(M))
#         d=date[:2]
#         Date=y+"-"+m+"-"+d+" 00:00:00"
#         Unixdate=int(time.mktime(time.strptime(Date,'%Y-%m-%d %H:%M:%S')))
#         # print("")
#     else:
#         Unixdate = ""
#     if imdb_sid in imdb_sid_list:
#         for a in mac_vod_list:
#             c = a["vod_id"]
#             if c == imdb_sid[2:16]:
#                 url=url1=url2='a'
#                 url1=str(a["url1"])+"#episode"+episode+"$"+vidsrc_url
#                 url2=str(a["url2"])+"#episode"+episode+"$"+"https://www.2embed.to/embed/imdb/tv?id="+imdb_id+"&s="+season+"&e="+episode
#                 url=url1 + '$$$' + url2
#                 a["vod_play_url"]=url
#     else:
#         url=url1=url2='a'
#         url1="episode"+episode+"$"+vidsrc_url
#         url2="episode"+episode+"$"+"https://www.2embed.to/embed/imdb/tv?id="+imdb_id+"&s="+season+"&e="+episode
#         url=str(url1) + "$$$" + str(url2)
#         omdb_vod_info = {
#             "vod_id":imdb_sid[2:16],
#             "vod_name":omdb_info_json["Title"][0:255],
#             "type_id":omdb_info_json["Genre"].split(",")[0][0:10],
#             "type_name":omdb_info_json["Genre"].split(",")[0][0:10],
#             "type_id_1":omdb_info_json["Type"][0:10],
#             "vod_blurb":omdb_info_json["Plot"][0:255],
#             "vod_en":omdb_info_json["Title"][0:255],
#             "vod_status":1,
#             "vod_letter":omdb_info_json["Title"][0:1],
#             "vod_color":"",
#             "vod_sub":"",
#             "vod_tag":"",
#             "vod_class":omdb_info_json["Genre"][0:255],
#             "vod_pic":omdb_info_json["Poster"][0:1024],
#             "vod_pic_thumb":"",
#             "vod_pic_slide":"",
#             "vod_pic_screenshot":"",
#             "vod_actor":omdb_info_json["Actors"][0:255],
#             "vod_director":omdb_info_json["Director"][0:255],
#             "vod_writer":omdb_info_json["Writer"][0:100],
#             "vod_behind":"",
#             "vod_remarks":"IMDb:"+omdb_info_json["imdbRating"][0:100],
#             "vod_pubdate":(omdb_info_json["Released"][0:100]),
#             "vod_total":"",
#             "vod_serial":"",
#             "vod_tv":"",
#             "vod_weekday":"",
#             "vod_area":omdb_info_json["Country"].split(",")[0][0:20],
#             "vod_lang":omdb_info_json["Language"].split(",")[0][0:10],
#             "vod_year":omdb_info_json["Year"][0:10],
#             "vod_version":"",
#             "vod_state":"",
#             "vod_author":"",
#             "vod_jumpurl":"",
#             "vod_tpl":"",
#             "vod_tpl_play": "",
#             "vod_tpl_down": "",
#             "vod_isend": 0,
#             "vod_lock": 0,
#             "vod_level": 0,
#             "vod_copyright": 0,
#             "vod_points": 0,
#             "vod_points_play": 0,
#             "vod_points_down": 0,
#             "vod_hits":omdb_info_json["imdbVotes"][0:8],
#             "vod_hits_day":omdb_info_json["imdbVotes"][0:8],
#             "vod_hits_week":omdb_info_json["imdbVotes"][0:8],
#             "vod_hits_month":omdb_info_json["imdbVotes"][0:8],
#             "vod_duration":omdb_info_json["Runtime"][0:10],
#             "vod_up":omdb_info_json["imdbVotes"][0:8],
#             "vod_down":"",
#             "vod_score":omdb_info_json["imdbRating"],
#             "vod_score_all":omdb_info_json["imdbVotes"][0:8],
#             "vod_score_num":omdb_info_json["imdbVotes"][0:8],
#             "vod_time":Unixdate,
#             "vod_time_add":Unixdate,
#             "vod_time_hits": 0,
#             "vod_time_make": 0,
#             "group_id": 0,
#             "vod_trysee": 0,
#             "vod_douban_id":"",
#             "vod_douban_score":omdb_info_json["imdbRating"],
#             "vod_reurl": "",
#             "vod_rel_vod": "",
#             "vod_rel_art": "",
#             "vod_pwd": "",
#             "vod_pwd_url": "",
#             "vod_pwd_play": "",
#             "vod_pwd_play_url": "",
#             "vod_pwd_down": "",
#             "vod_pwd_down_url": "",
#             "vod_content":omdb_info_json["Plot"][0:16777216],
#             "vod_play_server": "no$$$no",
#             "vod_play_note": "$$$",
#             "vod_down_from": "",
#             "vod_down_server": "",
#             "vod_down_note": "",
#             "vod_down_url": "",
#             "vod_plot": "",
#             "vod_plot_name": ""[0:16777216],
#             "vod_plot_detail": ""[0:16777216],
#             "vod_play_from": "tpiframe$$$tpiframecopy",
#             "url1":url1,
#             "url2":url2,
#             "vod_play_url":url

#             # https://www.2embed.to/embed/imdb/tv?id=IMDB ID&s=SEASON NUMBER&e=EPISODE NUMBER
#         }
#         mac_vod_list.append(omdb_vod_info)#字典套字典，准�?�拼json
#     imdb_sid_list.append(imdb_sid)
# y=json.dumps(mac_vod_list,indent=4)#将python�??为json
# mac_vod={"code":1,"msg":"数据列表","page":1,"pagecount":1,"limit":"3","total":3}
# mac_vod["list"]=mac_vod_list
# y=json.dumps(mac_vod,indent=4)#将python�??为json
# f = open("tV.json", "w")
# f.write(y)
# f.close
# f = open("tV.json","r")
# print(f.read())