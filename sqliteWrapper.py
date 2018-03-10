#!/usr/bin/python3
# coding=UTF-8

import sys
import http.client as httplib
import sqlite3
from lxml import etree

# print(str(dbPointer))
# dbPointerr = common.getDBPointer()
# print(str(dbPointerr))

class SqliteWrapper:
    ''' docstring for SqliteWrapper '''
    def __init__(self, tableName):
        self.fundb = sqlite3.connect("./fund.db")
        self.fundb.text_factory = str
        self.dbPointer = self.fundb.cursor()
        self.tableName = tableName

    # save data to sqlite db
    def saveData(self, postDate, postBy, visitTimes, commentTimes, updateTime):
        # print("CREATE TABLE if the TABLE not exists")
        sql = "CREATE TABLE IF NOT EXISTS " + self.tableName + \
            " (postDate VARCHAR(20), postBy VARCHAR(20), visitTimes INT, commentTimes INT, updateTime VARCHAR(20))"
        self.dbPointer.execute(sql)

        # INSERT data
        # print("deal with: %s, tableName: %s" %(date, tableName))
        try:
            self.dbPointer.execute("INSERT INTO " + self.tableName + \
                    " VALUES (?, ?, ?, ?, ?)", (postDate, postBy, visitTimes, commentTimes, updateTime))
        except:
            pass
            # 修改已经存在的值

        self.fundb.commit()

    # dump data from db
    def dumpDb(self, tableName):
        pass
        self.dbPointer.execute("SELECT * FROM " + tableName)
        while(1):
            result = dbPointer.fetchone()
            if (result != None):
                print(result)
            else:
                break
