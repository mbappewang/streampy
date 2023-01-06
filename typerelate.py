# -*- coding: utf-8 -*-
#导入模块
import json
f=open("/Users/shareit1/Documents/pycode/type对应关系.json","r")
type_json = json.loads(f.read())
f.close
typedict1={}
typedict2={}
a=b=0
for x in type_json:
    type_info = x
    typename = type_info["type_name"]
    typeid = type_info["type_id"]
    typeid1 = type_info["type_pid"]
    if typeid1 == 93:
        typedict1[typename] = typeid
        a+=1
    elif typeid1 == 94:
        typedict2[typename] = typeid
        b+=1
print(a,"\n",typedict1,"\n",b,"\n",typedict2)

{'Romance': 125, 'Adventure': 124, 'Short': 123, 'Comedy': 122, 'Drama': 128, 'Action': 129, 'Crime': 130, 'Western': 131, 'Documentary': 132, 'Horror': 133, 'Fantasy': 134, 'Biography': 135, 'History': 136, 'Animation': 137, 'Mystery': 138, 'Music': 139, 'Other': 140, 'Musical': 141, 'Sci-Fi': 142, 'Family': 143, 'Film-Noir': 144, 'War': 145, 'Thriller': 146, 'Adult': 147, 'Reality-TV': 148, 'Game-Show': 149, 'Talk-Show': 150, 'News': 151, 'Sport': 152} 
{'Romance': 126, 'Sport': 121, 'News': 120, 'Talk-Show': 119, 'Music': 108, 'Other': 109, 'Musical': 110, 'Game-Show': 118, 'Reality-TV': 117, 'Adult': 116, 'Thriller': 115, 'War': 114, 'Film-Noir': 113, 'Family': 112, 'Sci-Fi': 111, 'Mystery': 107, 'Animation': 106, 'History': 105, 'Biography': 104, 'Fantasy': 103, 'Horror': 102, 'Documentary': 101, 'Western': 100, 'Crime': 99, 'Action': 98, 'Adventure': 97, 'Comedy': 95, 'Short': 96, 'Drama': 127}