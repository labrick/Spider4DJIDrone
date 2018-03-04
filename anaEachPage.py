#!/usr/bin/python3

import http.client as httplib
from lxml import etree
from bs4 import BeautifulSoup

from module2 import getLinkPopularity
# from module2 import linkList
import common

# get data from html
def getHtmlContext(url):
    conn = httplib.HTTPConnection("bbs.dji.com")
    conn.request(method="GET", url = url)
    response = conn.getresponse()
    html = response.read()
    # print(html)
    # page = etree.HTML(html.lower().decode('utf-8'))

    # analyse html title
    # elements = page.xpath(u'''/html/head/title''')

    # all string need to search
    soup = BeautifulSoup(html, "html.parser")
    # print(soup.prettify())
    # print(soup.select("head > title")) = soup.title.text
    # print(soup.select("#postlist > div:nth-of-type(1) > table"))

    allStr = str(soup.select("#postlist > div:nth-of-type(1) > table > tr:nth-of-type(1)")[0])
    # print(allStr)
    return allStr

def modifyPopularity(allStr, djiDevicePopularity):
    deviceNames = common.getDeviceName()
    for deviceName, nicknameList in deviceNames.items():
        if allStr.find(deviceName) != -1:
            djiDevicePopularity[deviceName] += 1
            print("find " + deviceName)
            return      # analyse over, but really?
        for nickname in nicknameList:
            if allStr.find(nickname) != -1:
                print("find " + nickname)
                djiDevicePopularity[deviceName] += 1
                return
    print("find nothing")

    # print(elements[0].text)

def getPopularity():
    linkList, djiDevicePopularity = getLinkPopularity()
    for url in linkList:
        allStr = getHtmlContext(url)
        # print(allStr)
        print("get " + url + " OK!!!")
        modifyPopularity(allStr, djiDevicePopularity)
    return djiDevicePopularity


def main():
    linkList, djiDevicePopularity = getLinkPopularity()
    for url in linkList:
        allStr = getHtmlContext(url)
        # print(allStr)
        print("get " + url + " OK!!!")
        modifyPopularity(allStr, djiDevicePopularity)

    for djiDeviceKey, popularityValue in djiDevicePopularity.items():
        print("%12s:\t%d" % (djiDeviceKey, popularityValue))

if __name__ == '__main__':
    main()
