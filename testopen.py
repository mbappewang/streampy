# # -*- coding: utf-8 -*-
# #导入模块
# import json
# import time
# import datetime
# import urllib.request
# import random
# #设定默认值
# item = page_tout_count = same = 0
# p = pages = 1
# vidsrc_vod_list=[]
# page_timeout_list=[]
# page_list=[]
# imdb_id_list=[]
# #获取历史爬取记录
# try:
#     openlist = open("vidsrc-infolist.txt","r")
#     vidsrc_vod_list = json.load(openlist)
#     openlist.close
#     for y in vidsrc_vod_list:
#         imdb_id = y.get("imdb_id","tt0")
#         imdb_id_list.append(imdb_id)
# except:
#     print("读取失败",imdb_id_list)
#     vidsrc_vod_list = []
# print(type(vidsrc_vod_list),vidsrc_vod_list)