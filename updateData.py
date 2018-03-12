#!/usr/bin/python3

import sys
import re
import time
import getopt

import requests
from lxml import etree
from sqliteWrapper import SqliteWrapper

BASE_URL = 'https://bbs.dji.com/'
# POST_URL = 'https://bbs.dji.com/forum-60-1.html'
POST_URL = 'https://bbs.dji.com/forum.php?mod=forumdisplay&fid=60&orderby=dateline&orderby=dateline&filter=typeid&page=612'

def getHtml(url):
    page = requests.get(url).content.decode('utf-8')
    # print(page)
    return etree.HTML(page.lower())

def cleanData(html):
    postLink = html.xpath('//tbody/tr/th/p[1]/a[1]/@href')

    # postTitle = html.xpath('//*[@id="threadlisttableid"]/tbody[6]/tr/th/p[1]/a/text()')
    # bad method
    # postTitle = list(filter(lambda t: t!='new', postTitle))
    # solve empty title problem
    postTitle = []
    index = 0
    itbody = 0
    while index < len(postLink):
        postitle = html.xpath('//*[@id="threadlisttableid"]/tbody[' + str(itbody+2) + ']/tr/th/p[1]/a/text()[1]')
        postlink = html.xpath('//*[@id="threadlisttableid"]/tbody[' + str(itbody+2) + ']/tr/th/p[1]/a/@href')
        # print(postitle)
        # print(postlink)
        # print("-----" + str(index))
        itbody += 1

        if (len(postlink) == 0) and (len(postitle) == 0):
            continue
        index += 1
        if (len(postitle)) == 0:
            postTitle.append("")
        else:
            postTitle.append(postitle[0])

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

    if (len(postLink) != len(postDate)) or \
        (len(postLink) != len(postBy)) or \
        (len(postLink) != len(postTitle)) or \
        (len(postLink) != len(device)) or \
        (len(postLink) != len(visitTimes)) or \
        (len(postLink) != len(commentTimes)) or \
        (len(postLink) != len(updateTime)):
        print(len(postLink))
        print(len(postDate))
        print(len(postBy))
        print(len(postTitle))
        print(len(device))
        print(len(visitTimes))
        print(len(commentTimes))
        print(len(updateTime))
        print("ERROR in cleanData!!!")

    return postDate, postBy, device, postTitle, postLink, \
                visitTimes, commentTimes, updateTime

# Get the maximum number of pages
def getMaxPageNum():
    pageGet = getHtml(POST_URL)
    numList = pageGet.xpath('//span[@id = "fd_page_bottom"]/div/label/span/text()')
    maxNum = int((re.findall(r"\d.*\d", numList[0]))[0])
    #print(maxNum)
    return maxNum

def updateData(sqliteWrapper):
    sqlRowNum = int(sqliteWrapper.getRowNum())
    # 60 items of each page
    sqlPageNum = int(sqlRowNum / 60)

    maxPageNum = getMaxPageNum()
    pageNum = maxPageNum - sqlPageNum
    print("all pages:" + str(maxPageNum) + ", pages in sql:" + str(sqlPageNum) + ", updating pages:" + str(pageNum))
    while pageNum > 0:
        pageUrl = BASE_URL + 'forum.php?mod=forumdisplay&fid=60&orderby=dateline&orderby=dateline&filter=typeid&page=' + str(pageNum)
        # pageUrl = BASE_URL + 'forum-60-' + str(pageNum) + '.html'
        sys.stdout.write("\ranalyse page:" + str(pageNum) + "/" + str(maxPageNum))
        html = getHtml(pageUrl)

        postDate, postBy, device, postTitle, postLink, \
                visitTimes, commentTimes, updateTime = cleanData(html)
        for i in range(len(postLink)):
            postLink[i] = BASE_URL + postLink[i]
            device[i] = device[i].replace("发表于", '').replace("用户", '').strip()
            visitTimes[i] =  visitTimes[i].replace("人查看", "").strip()
            commentTimes[i] = commentTimes[i].replace("条回复", "")
            # print("postDate: " + str(postDate[i]) + "\npostBy: " + str(postBy[i]) + "\ndevice: " + \
            #     str(device[i]) + "\npostTitle: " + postTitle[i] + "\npostLink: " + str(postLink[i]) + \
            #     "\nvisitTimes: " + str(visitTimes[i]) + "\ncommentTimes: " + str(commentTimes[i]) + \
            #     "\nupdateTime: " + str(updateTime[i]))
            # print("-----------")
            sqliteWrapper.saveData(str(postDate[i]), str(postBy[i]), str(device[i]), str(postTitle[i]), \
                    str(postLink[i]), int(visitTimes[i]), int(commentTimes[i]), str(updateTime[i]))
        pageNum -= 1
    print()     # print \n

def main():
    sqliteWrapper = SqliteWrapper("C222")
    updateData(sqliteWrapper)

if __name__ == '__main__':
    main()
