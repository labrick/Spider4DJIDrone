#!/usr/bin/python3

import sys
import re
import time

import requests
from lxml import etree
from sqliteWrapper import SqliteWrapper

BASE_URL = 'https://bbs.dji.com/'
POST_URL = 'https://bbs.dji.com/forum-60-1.html'

linkList = []
link2DeviceList = []

def getHtml(html):
    page = requests.get(html).content.decode('utf-8')
    # print(page)
    return etree.HTML(page.lower())

# Get the maximum number of pages
def getMaxPageNum():
    pageGet = getHtml(POST_URL)
    numList = pageGet.xpath('//span[@id = "fd_page_bottom"]/div/label/span/text()')
    maxNum = int((re.findall(r"\d.*\d", numList[0]))[0])
    #print(maxNum)
    return maxNum

def updateData(sqliteWrapper, maxPage = None):
    if maxPage is None:
        maxPageNum = getMaxPageNum()
    else:
        maxPageNum = maxPage
    pageNum = 1
    while pageNum <= maxPageNum:
        pageUrl = BASE_URL + 'forum-60-' + str(pageNum) + '.html'
        sys.stdout.write("\ranalyse page:" + str(pageNum) + "/" + str(maxPageNum))
        html = getHtml(pageUrl)

        postLink = html.xpath('//tbody/tr/th/p[1]/a[1]/@href')
        postBy = html.xpath('//tbody/tr/th/p[2]/cite/a/text()[1]')

        # postDate = []
        # for url in postLink:
        #     subHtml = getHtml(BASE_URL + url)
        #     dateTime = subHtml.xpath('//*[@id="postlist"]/div[1]/table/tr[1]/td/div[1]/div/div[2]/div[5]/span[1]/span/@title')
        #     # print(dateTime)
        #     if len(dateTime) == 0:
        #         dateTime = subHtml.xpath('//*[@id="postlist"]/div[1]/table/tr[1]/td/div[1]/div/div[2]/div[5]/span[1]/text()[1]')
        #         # print("---------" + str(dateTime))
        #     postDate.append(dateTime[0])
        postDate = []
        index = 0
        itbody = 0
        while index < len(postLink):
            dateTime = html.xpath('//*[@id="threadlist"]/div/form/table/tbody[' + str(itbody+2) + ']/tr/th/p[2]/em[2]/span/span/@title')
            if len(dateTime) == 0:
                dateTime = html.xpath('//*[@id="threadlist"]/div/form/table/tbody[' + str(itbody+2) + ']/tr/th/p[2]/em[2]/span/text()[1]')
                # print("---------" + str(dateTime))
            itbody += 1
            if len(dateTime) == 0:
                continue
            index += 1
            postDate.append(dateTime[0])

        device = html.xpath('//tbody/tr/th/p[2]/em[2]/text()[1]')
        visitTimes = html.xpath('//tbody/tr/th/p[2]/em[2]/text()[2]')
        commentTimes = html.xpath('//tbody/tr/th/p[2]/a/text()[1]')

        # complex, need to simplify
        updateTime = []
        index = 0
        itbody = 0
        while index < len(postLink):
            dateTime = html.xpath('//*[@id="threadlist"]/div/form/table/tbody[' + str(itbody+2) + ']/tr/th/p[2]/em[3]/a/span/@title')
            if len(dateTime) == 0:
                dateTime = html.xpath('//*[@id="threadlist"]/div/form/table/tbody[' + str(itbody+2) + ']/tr/th/p[2]/em[3]/a/text()[1]')
                # print("---------" + str(dateTime))
            itbody += 1
            if len(dateTime) == 0:
                continue
            index += 1
            updateTime.append(dateTime[0])

        for i in range(len(postLink)):
            postLink[i] = BASE_URL + postLink[i]
            device[i] = device[i].replace("发表于", '').replace("用户", '').strip()
            visitTimes[i] =  visitTimes[i].replace("人查看", "").strip()
            commentTimes[i] = commentTimes[i].replace("条回复", "")
            # print("postDate: " + str(postDate[i]) + "\npostBy: " + str(postBy[i]) + "\ndevice: " + str(device[i]) + "\npostLink: " + \
            #         str(postLink[i]) + "\nvisitTimes: " + str(visitTimes[i]) + "\ncommentTimes: " + str(commentTimes[i]) + "\nupdateTime: " + str(updateTime[i]))
            # print("-----------")
            sqliteWrapper.saveData(str(postDate[i]), str(postBy[i]), str(device[i]), str(postLink[i]), int(visitTimes[i]), int(commentTimes[i]), str(updateTime[i]))
        pageNum += 1
    print()     # print \n

    print("link num:" + str(len(linkList)) + ", device Num:" + str(len(link2DeviceList)))

def main():
    sqliteWrapper = SqliteWrapper("C222")
    sqliteWrapper.saveData("2018-3-10", "YN", "spark", "https://111", 10, 10, "2018-3-10 12:32")
    sqliteWrapper.saveData("2018-3-7", "YN", "mavic", "https://122", 10, 10, "2018-3-10 12:32")
    item = sqliteWrapper.getNewstDate()
    if item is not None:
        print(item[0])

    updateData(sqliteWrapper)
    print("link num:" + str(len(linkList)) + ", device Num:" + str(len(link2DeviceList)))

    # for index in range(len(linkList)):
    #     print(str(index) + "\t" + linkList[index] + "\t" + link2DeviceList[index])

if __name__ == '__main__':
    main()
