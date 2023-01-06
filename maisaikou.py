# -*- coding: utf-8 -*-
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd='walc94511',
  database="localtest"
)
mycursor = mydb.cursor()
mycursor.execute("SHOW TABLES")

for x in mycursor:
  print(x)
mycursor.execute("CREATE TABLE `mac_vod` (`vod_id` int(10))")