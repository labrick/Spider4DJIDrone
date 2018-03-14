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

    def onSale(self, startDate, endDate, onSaleTime):
        if (startDate < onSaleTime) and (onSaleTime < endDate):
            return True
        else:
            return False

    def getNoAirItem(self, itemName, startDate, endDate):
        # self.dbPointer.execute('SELECT * FROM ' + self.tableName + ' where postDate between "' \
        self.dbPointer.execute('SELECT ' + itemName + ' FROM ' + self.tableName + ' where postDate between "' \
                + startDate + '" and "' + endDate + '" and postDate != "' + endDate +  '" and device != "mavic air" ORDER BY postDate DESC')
        itemNames = list(self.dbPointer.fetchall())

        result = []
        for item in itemNames:
            result.append(item[0])
            # result.append(item)
        return result

    def getItem(self, itemName, startDate, endDate):
        # self.dbPointer.execute('SELECT * FROM ' + self.tableName + ' where postDate between "' \
        self.dbPointer.execute('SELECT ' + itemName + ' FROM ' + self.tableName + ' where postDate between "' \
                + startDate + '" and "' + endDate + '" and postDate != "' + endDate +  '" ORDER BY postDate DESC')
        itemNames = list(self.dbPointer.fetchall())

        result = []
        for item in itemNames:
            result.append(item[0])
            # result.append(item)
        return result


    def getDevice(self, startDate, endDate):
        startDate = self.fmtDate(startDate + "-01")
        endDate = self.fmtDate(endDate + "-01")
        # print(startDate)
        # print(endDate)
        airOnSaleTime = "2018-02-01"
        result = []
        if(self.onSale(startDate, endDate, airOnSaleTime)):
            result.extend(self.getNoAirItem("device", startDate, airOnSaleTime))
            result.extend(self.getItem("device", airOnSaleTime, endDate))
        elif (endDate < airOnSaleTime):
            result.extend(self.getNoAirItem("device", startDate, airOnSaleTime))
        else:
            result.extend(self.getItem("device", startDate, endDate))

        return result

    def getPostLink(self, startDate, endDate):
        startDate = self.fmtDate(startDate + "-01")
        endDate = self.fmtDate(endDate + "-01")
        # print(startDate)
        # print(endDate)
        airOnSaleTime = "2018-02-01"
        result = []
        if(self.onSale(startDate, endDate, airOnSaleTime)):
            result.extend(self.getNoAirItem("postLink", startDate, airOnSaleTime))
            result.extend(self.getItem("postLink", airOnSaleTime, endDate))
        elif (endDate < airOnSaleTime):
            result.extend(self.getNoAirItem("postLink", startDate, airOnSaleTime))
        else:
            result.extend(self.getItem("postLink", startDate, endDate))

        return result

