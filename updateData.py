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

def getLinkDevice(maxPage = None):
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
        print(postLink)
        print(len(postLink))
        postBy = html.xpath('//tbody/tr/th/p[2]/cite/a/text()[1]')
        print(postBy)
        print(len(postBy))

        postDate = []
        for index in range(len(postLink)):
            date = html.xpath('//tbody[' + str(index+2) + ']/tr/th/p[2]/em[2]/span/span/@title')
            if len(date) == 0:
                print("get")
                date = html.xpath('//tbody[' + str(index+2) + ']/tr/th/p[2]/em[2]/span/text()[1]')
            if len(date) == 0:
                continue
            print("---------" + str(date))
            postDate.append(date)
            # if postDate[index] is None:
            #     postDate[index] = html.xpath('//tbody/tr/th/p[2]/em[2]/span/text()[1]')
            # print(postDate[index])
        print(postDate)
        print(len(postDate))
        device = html.xpath('//tbody/tr/th/p[2]/em[2]/text()[1]')
        print(device)
        print(len(device))
        commentTimes = html.xpath('//tbody/tr/th/p[2]/a/text()[1]')
        print(commentTimes)
        print(len(commentTimes))
        updateTime = html.xpath('//tbody/tr/th/p[2]/em[3]/a/span/@title')
        print(updateTime)
        print(len(updateTime))
        return
        # linkList.extend(html.xpath('//tbody/tr/th/p[1]/a[1]/@href'))
        # link2DeviceList.extend(html.xpath('//tbody/tr/th/p[2]/em[2]/text()[1]'))
        pageNum += 1
    print()     # print \n

    for index in range(len(linkList)):
        linkList[index] = BASE_URL + linkList[index]

    for index in range(len(link2DeviceList)):
        link2DeviceList[index] = link2DeviceList[index].replace("发表于", '')
        link2DeviceList[index] = link2DeviceList[index].replace("用户", '')
        link2DeviceList[index] = link2DeviceList[index].rstrip()

    print("link num:" + str(len(linkList)) + ", device Num:" + str(len(link2DeviceList)))
    return linkList, link2DeviceList

def main():
    sqliteWrapper = SqliteWrapper("C222")
    sqliteWrapper.saveData("2018-3-10", "YN", "spark", "https://111", 10, 10, "2018-3-10 12:32")
    sqliteWrapper.saveData("2018-3-7", "YN", "mavic", "https://122", 10, 10, "2018-3-10 12:32")
    item = sqliteWrapper.getNewstDate()
    if item is not None:
        print(item[0])

    linkList, link2DeviceList = getLinkDevice()
    print("link num:" + str(len(linkList)) + ", device Num:" + str(len(link2DeviceList)))

    # for index in range(len(linkList)):
    #     print(str(index) + "\t" + linkList[index] + "\t" + link2DeviceList[index])

if __name__ == '__main__':
    main()
