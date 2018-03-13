#!/usr/bin/python3
# coding=UTF-8

import sys
import time
import http.client as httplib
import sqlite3
from lxml import etree

# print(str(dbPointer))
# dbPointerr = common.getDBPointer()
# print(str(dbPointerr))

class SqliteWrapper:
    ''' docstring for SqliteWrapper '''
    def __init__(self, tableName):
        self.fundb = sqlite3.connect("./dji.db")
        self.fundb.text_factory = str
        self.dbPointer = self.fundb.cursor()
        self.tableName = tableName
        sql = "CREATE TABLE IF NOT EXISTS " + self.tableName + \
            " (postDate TEXT, postBy VARCHAR(20), device TEXT, postTitle TEXT, postLink TEXT UNIQUE, visitTimes INT, commentTimes INT, updateTime VARCHAR(20))"
        self.dbPointer.execute(sql)

    def fmtDate(self, dateStr):
        t = time.strptime(dateStr, "%Y-%m-%d")
        return time.strftime("%Y-%m-%d", t)


    def fmtDateTime(self, dateStr):
        t = time.strptime(dateStr, "%Y-%m-%d %H:%M")
        return time.strftime("%Y-%m-%d %H:%M", t)

    # save data to sqlite db
    def saveData(self, postDate, postBy, device, postTitle, postLink, visitTimes, commentTimes, updateTime):
        postDate = self.fmtDate(postDate)
        updateTime = self.fmtDateTime(updateTime)
        # sql = "CREATE TABLE IF NOT EXISTS " + self.tableName + \
        #     " (postDate TEXT, postBy VARCHAR(20), device TEXT, postTitle TEXT, postLink TEXT UNIQUE, visitTimes INT, commentTimes INT, updateTime VARCHAR(20))"
        # self.dbPointer.execute(sql)

        # INSERT data
        # print("deal with: %s, tableName: %s" %(date, tableName))
        try:
            self.dbPointer.execute("INSERT INTO " + self.tableName + \
                    # " VALUES (?, ?, ?, ?, ?)", (date(postDate), postBy, visitTimes, commentTimes, datetime(updateTime)))
                    " VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (postDate, postBy, device, postTitle, postLink, visitTimes, commentTimes, updateTime))
        except:
            pass
            # 修改已经存在的值

        self.fundb.commit()

    def getLastestDate(self):
        self.dbPointer.execute("SELECT * FROM " + self.tableName + " ORDER BY DATE(postDate) DESC")
        return self.dbPointer.fetchone()

    def getRowNum(self):
        self.dbPointer.execute("SELECT COUNT(*) FROM " + self.tableName)
        return self.dbPointer.fetchone()[0]

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
    def getPostLink(self, startDate, endDate):
        startDate = self.fmtDate(startDate + "-01")
        endDate = self.fmtDate(endDate + "-01")
        # print(startDate)
        # print(endDate)
        self.dbPointer.execute('SELECT postLink FROM ' + self.tableName + ' where postDate between "' \
                + startDate + '" and "' + endDate + '" ORDER BY postDate DESC')
        postLinks = list(self.dbPointer.fetchall())
        self.dbPointer.execute('SELECT postDate FROM ' + self.tableName + ' where postDate between "' \
                + startDate + '" and "' + endDate + '" ORDER BY postDate DESC')
        postDates = list(self.dbPointer.fetchall())
        for index in range(len(postDates)):
            if postDates[index][0] != endDate:
                break;
            del postLinks[0]

        result = []
        for postLink in postLinks:
            result.append(postLink[0])
        return result

    def getDevice(self, startDate, endDate):
        startDate = self.fmtDate(startDate + "-01")
        endDate = self.fmtDate(endDate + "-01")
        # print(startDate)
        # print(endDate)
        self.dbPointer.execute('SELECT device FROM ' + self.tableName + ' where postDate between "' \
                + startDate + '" and "' + endDate + '" ORDER BY postDate DESC')
        devices = list(self.dbPointer.fetchall())
        self.dbPointer.execute('SELECT postDate FROM ' + self.tableName + ' where postDate between "' \
                + startDate + '" and "' + endDate + '" ORDER BY postDate DESC')
        postDates = list(self.dbPointer.fetchall())

        for index in range(len(postDates)):
            if postDates[index][0] != endDate:
                break;
            del devices[0]

        result = []
        for device in devices:
            result.append(device[0])

        return result

