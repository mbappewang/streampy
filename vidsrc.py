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
    database="mydatabase"
    )
    mycursor = mydb.cursor()
except:
    print("连接msql失败")
else:
    # #读取mysql表中的vod_id列，存到元组，再转列表
    # mycursor.execute("SELECT imdb_id FROM mac_vod")
    # imbd_id_tuple = mycursor.fetchall()
    # imdb_id_list = []
    # for (x,) in imbd_id_tuple:
    #     imdb_id_list.append("tt"+x)
    # print("库内最新imdb数量：",len(imdb_id_list))
    #设置默认值
    item = page_tout_count = same = 0
    p = pages = 1
    vidsrc_vod_list=[]
    page_timeout_list=[]
    page_list=[]
    #请求json函数
    def get_vidsrc(url):
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
        requestsite = urllib.request.Request(url,headers=headers)
        data = urllib.request.urlopen(requestsite,timeout=15).read()
        vidsrc_dic = json.loads(data)
        return vidsrc_dic
    #获取初始页码值
    try:
        vidsrc_dict = get_vidsrc("https://vidsrc.me/movies/latest/page-1.json")
        vidsrc_result = vidsrc_dict["result"]
    except:
        print("没有读到页码！！！！！！！！")
        pages = 1201
    else:
        print("读到页数了")
        pages = vidsrc_dict["pages"]+1
        # vidsrc_dict["pages"]+1
    print("总页数：",pages)
    #生成pagelist
    while p <= pages:
        page_list.append(p)
        p += 1
    #不抓干净不停抓
    p=1
    while page_list != []:
        #翻页循环
        for p in page_list:
            print(">>>>>>>>>>>>>>>",p,"页遍历开始","<<<<<<<<<<<<<<<<")
            #避免程序超时，用try、except
            try:
                #请求函数获得接口页信息
                vidsrc_dict = get_vidsrc("https://vidsrc.me/movies/latest/page-" + str(p) + ".json")
            except:
                print("请求↓失败")
                page_tout_count += 1
                print("超时页记录：",page_timeout_list,"超时了","目前条数：",item,"目前页数",p,"超时次数：",page_tout_count,"库内最新imdb数量：",len(imbd_id_tuple))
                if p in page_timeout_list:
                    print("第",p,"页重试再次超时")
                else:
                    page_timeout_list.append(p)
            else:
                print("请求↑成功")
                #将接口的json文件中的result字段取出
                vidsrc_result = vidsrc_dict["result"]
                #读取mysql表中的vod_id列，存到元组，再转列表
                mycursor.execute("SELECT imdb_id FROM imdb")
                imbd_id_tuple = mycursor.fetchall()
                # imdb_id_list = []
                # for (x,) in imbd_id_tuple:
                #     imdb_id_list.append("tt"+x)
                # print("库内最新imdb数量：",len(imdb_id_list))
                for x in vidsrc_result:
                    item += 1
                    imdb_id = "m"+x.get("imdb_id","tm0")[2:10]
                    if (imdb_id,) in imbd_id_tuple:
                        same += 1
                        print("发现重复记录")
                    else:
                        # title_vidsrc = x.get("title","")
                        url_vidsrc = x.get("embed_url","")
                        vidsrc_vod_info = (imdb_id,url_vidsrc)
                        #将遍历的信息存储进列表中备用
                        sql = "INSERT INTO imdb (imdb_id,play_url_1) VALUES (%s,%s)"
                        val = vidsrc_vod_info
                        mycursor.execute(sql, val)
                        mydb.commit()
                        # vidsrc_vod_list.append(vidsrc_vod_info)
                #mysql入库
                # savelist = open("vidsrc-infolist.txt","w",encoding='utf-8')
                # savelist.write(json.dumps(vidsrc_vod_list))
                # savelist.close
                page_list.remove(p)
                print("超时页记录：",page_timeout_list,"没有超时","目前条数：",item,"目前页数",p,"超时次数：",page_tout_count,"已发现重复条数：",same,"库内最新imdb数量：",len(imbd_id_tuple))
                if p in page_timeout_list:
                    print("第",p,"页重试成功")
                    page_timeout_list.remove(p)



#鐠佹儳鐣炬妯款吇閸婏拷
# item = page_tout_count = same = 0
# p = pages = 1
# vidsrc_vod_list=[]
# page_timeout_list=[]
# page_list=[]
# imdb_id_list=[]
#閼惧嘲褰囬崢鍡楀蕉閻栴剙褰囩拋鏉跨秿
# try:
#     openlist = open("vidsrc-infolist.txt","r")
#     vidsrc_vod_list = json.load(openlist)
#     openlist.close
#     for y in vidsrc_vod_list:
#         imdb_id = y.get("imdb_id","tt0")
#         imdb_id_list.append(imdb_id)
# except:
#     print("鐠囪褰囨径杈Е",imdb_id_list)
#     vidsrc_vod_list = []
# print(type(vidsrc_vod_list))
# #鐠囬攱鐪癹son閸戣姤鏆�
# def get_vidsrc(url):
#     headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
#     requestsite = urllib.request.Request(url,headers=headers)
#     data = urllib.request.urlopen(requestsite,timeout=15).read()
#     vidsrc_dic = json.loads(data)
#     return vidsrc_dic
#閼惧嘲褰囬崚婵嗩潗妞ょ數鐖滈崐锟�
# try:
#     vidsrc_dict = get_vidsrc("https://vidsrc.me/movies/latest/page-1.json")
#     vidsrc_result = vidsrc_dict["result"]
# except:
#     print("濞屸剝婀佺拠璇插煂妞ょ數鐖滈敍渚婄磼閿涗緤绱掗敍渚婄磼閿涗緤绱�")
#     pages = 1210
# else:
#     print("鐠囪鍩屾い鍨殶娴滐拷")
#     pages = vidsrc_dict["pages"]+1
# print("閹銆夐弫甯窗",pages)
# #閻㈢喐鍨歱agelist
# while p <= pages:
#     page_list.append(p)
#     p += 1

# while page_list != []:
#     #缂堝銆夊顏嗗箚
#     for p in page_list:
#         sleeptime = random.random() * 2 + 1
#         print(">>>>>>>>>>>>>>>","闂呭繑婧€娴兼垶浼呴敍锟�",round(sleeptime,2),"<<<<<<<<<<<<<<<<")
#         time.sleep(sleeptime)
#         #闁灝鍘ょ粙瀣碍鐡掑懏妞傞敍宀€鏁ry except
#         try:
#             #鐠囬攱鐪伴崙鑺ユ殶閼惧嘲绶遍幒銉ュ經妞ゅ吀淇婇幁锟�
#             vidsrc_dict = get_vidsrc("https://vidsrc.me/movies/latest/page-" + str(p) + ".json")
#         except:
#             print("鐠囬攱鐪伴埆鎾炽亼鐠愶拷")
#             page_tout_count += 1
#             print("鐡掑懏妞傛い浣冾唶瑜版洩绱�",page_timeout_list,"鐡掑懏妞傛禍锟�","閻╊喖澧犻弶鈩冩殶閿涳拷",item,"閻╊喖澧犳い鍨殶",p,"鐡掑懏妞傚▎鈩冩殶閿涳拷",page_tout_count)
#             if p in page_timeout_list:
#                 print("缁楋拷",p,"妞ょ敻鍣哥拠鏇炲晙濞喡ょТ閺冿拷")
#             else:
#                 page_timeout_list.append(p)
#         else:
#             print("鐠囬攱鐪伴埆鎴炲灇閸旓拷")
#             #鐏忓棙甯撮崣锝囨畱json閺傚洣娆㈡稉顓犳畱result鐎涙顔岄崣鏍у毉
#             vidsrc_result = vidsrc_dict["result"]
#             #闁秴宸籿idsrc_result閸掓銆�
#             for x in vidsrc_result:
#                 item += 1
#                 imdb_id = x.get("imdb_id","tt0")
#                 if imdb_id in imdb_id_list:
#                     same += 1
#                     print("閸欐垹骞囬柌宥咁槻鐠佹澘缍�")
#                 else:
#                     title_vidsrc = x.get("title","")
#                     url_vidsrc = x.get("embed_url","")
#                     vidsrc_vod_info = {
#                     "imdb_id":imdb_id,
#                     "title":title_vidsrc,
#                     "url":url_vidsrc
#                     }
#                     #鐏忓棝浜堕崢鍡欐畱娣団剝浼呯€涙ê鍋嶆潻娑樺灙鐞涖劋鑵戞径鍥╂暏
#                     vidsrc_vod_list.append(vidsrc_vod_info)
#             savelist = open("vidsrc-infolist.txt","w",encoding='utf-8')
#             savelist.write(json.dumps(vidsrc_vod_list))
#             savelist.close
#             page_list.remove(p)
#             print("鐡掑懏妞傛い浣冾唶瑜版洩绱�",page_timeout_list,"濞屸剝婀佺搾鍛","閻╊喖澧犻弶鈩冩殶閿涳拷",item,"閻╊喖澧犳い鍨殶",p,"鐡掑懏妞傚▎鈩冩殶閿涳拷",page_tout_count,"瀹告彃褰傞崣鎴犲箛闁插秴顦查弶鈩冩殶閿涳拷",same)
#             if p in page_timeout_list:
#                 print("缁楋拷",p,"妞ょ敻鍣哥拠鏇熷灇閸旓拷")
#                 page_timeout_list.remove(p)