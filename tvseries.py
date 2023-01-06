import json
# with open('study.json','r') as vidsrc:
#     vid = json.load(vidsrc)
# for x in vid:
#     imdb_id=x.get("imdb_id")
#     print(imdb_id)
print("*************************")
# mac_vod = {
#     "imdb_id":"tt0"
# }
# import urllib.request
# def get_imdb_id(url):
#     vidsrc = urllib.request.urlopen(url,verify=False)
#     vidsrc_json = json.loads(vidsrc.read())
#     return vidsrc_json
# vidsrc_json = get_imdb_id("https://v49.me/study.json")
# for vid_info in vidsrc_json:
#     print(vid_info)
import urllib.request
mac_vod_list = []
def get_imdb_id(url):#读json文件
    vidsrc = urllib.request.urlopen(url)
    vidsrc_json = json.loads(vidsrc.read())
    return vidsrc_json
vidsrc_json = get_imdb_id("http://139.84.165.93:8888/down/TZ84SpxbWx4S.json")
print("-------------------------")
for x in vidsrc_json:
    imdb_id = x["imdb_id"]#通过json文件查询imdb
    vidsrc_url = x["embed_url"]
    omdb_url = "http://www.omdbapi.com/?i="+imdb_id+"&apikey=57e932e4"#拼omdb查询url
    print("$$$$$$$$$$$$$$$$$$$$$$$$$")
    def get_omdb_info(url):
        omdb_info = urllib.request.urlopen(url)
        omdb_info_json = json.loads(omdb_info.read())
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%")
        return omdb_info_json#用imdbid查omdb的imdb的信息
    omdb_info_json = get_omdb_info(omdb_url)#获得imdb的信息
    #新建字典，键的名字同mysql表的键名，然后将imdb信息传给字典
    omdb_vod_info = {
        "vod_id":omdb_info_json["imdbID"][2:10],
        "vod_name":omdb_info_json["Title"][0:30],
        "type_id":omdb_info_json["Genre"].split(",")[0][0:10],
        "type_id_1":omdb_info_json["Type"],
        "vod_blurb":omdb_info_json["Plot"][0:255],
        "vod_en":omdb_info_json["Title"][0:30],
        "vod_status":1,
        "vod_letter":omdb_info_json["Title"][0:30],
        "vod_color":"",
        "vod_tag":"",
        "vod_class":omdb_info_json["Genre"],
        "vod_pic":omdb_info_json["Poster"],
        "vod_pic_thumb":"",
        "vod_pic_slide":"",
        "vod_pic_screenshot":"",
        "vod_actor":omdb_info_json["Actors"],
        "vod_director":omdb_info_json["Director"],
        "vod_writer":omdb_info_json["Writer"],
        "vod_behind":"",
        "vod_remarks":"IMDb:"+omdb_info_json["imdbRating"]+"☆",
        "vod_pubdate":omdb_info_json["Released"],
        "vod_total":"",
        "vod_serial":"",
        "vod_tv":"",
        "vod_weekday":"",
        "vod_area":omdb_info_json["Country"],
        "vod_lang":omdb_info_json["Language"],
        "vod_year":omdb_info_json["Year"],
        "vod_version":omdb_info_json["Production"],
        "vod_state":"",
        "vod_author":omdb_info_json["Production"],
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
        "vod_hits":omdb_info_json["imdbVotes"],
        "vod_hits_day":omdb_info_json["imdbVotes"],
        "vod_hits_week":omdb_info_json["imdbVotes"],
        "vod_hits_month":omdb_info_json["imdbVotes"],
        "vod_duration":omdb_info_json["Runtime"],
        "vod_up": 16,
        "vod_down": 52,
        "vod_score": "0.0",
        "vod_score_all":omdb_info_json["Metascore"],
        "vod_score_num":omdb_info_json["imdbVotes"],
        "vod_time":omdb_info_json["Released"],
        "vod_time_add":omdb_info_json["Released"],
        "vod_time_hits": 0,
        "vod_time_make": 0,
        "vod_trysee": 0,
        "vod_douban_id": 34792434,
        "vod_douban_score":omdb_info_json["Metascore"],
        "vod_reurl": "",
        "vod_rel_vod": "",
        "vod_rel_art": "",
        "vod_pwd": "",
        "vod_pwd_url": "",
        "vod_pwd_play": "",
        "vod_pwd_play_url": "",
        "vod_pwd_down": "",
        "vod_pwd_down_url": "",
        "vod_content":omdb_info_json["Plot"][0:255],
        "vod_play_server": "no$$$no",
        "vod_play_note": "$$$",
        "vod_down_from": "",
        "vod_down_server": "",
        "vod_down_note": "",
        "vod_down_url": "",
        "vod_plot": "",
        "vod_plot_name": "",
        "vod_plot_detail": "",
        "vod_play_from": "tpiframe$$$tpiframecopy",
        "vod_play_url":"HD$"+vidsrc_url+"$$$"+"HD$https://www.2embed.to/embed/imdb/movie?id="+omdb_info_json["imdbID"][2:10]
    }
    mac_vod_list.append(omdb_vod_info)#字典套字典，准备拼json
y=json.dumps(mac_vod_list)#将python转为json
f = open("test.json", "w")
f.write(y)
f.close
f = open("test.json","r")
print(f.read())