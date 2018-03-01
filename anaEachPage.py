#!/usr/bin/python3

import http.client as httplib
from lxml import etree
from bs4 import BeautifulSoup

from module2 import djiDevicePopularity
from module2 import linkList
import common

# device other name dict
# dict["stdName"] = nick name list
deviceNickname = {}

# get data from html
def getHtml(url):
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

    allStr = str(soup.select("#postlist > div:nth-of-type(1) > table")[0])
    print(allStr)

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

    # print(elements[0].text)

def main():
    for url in linkList:
        getHtml(url)
        print("get " + url + " OK!!!")

if __name__ == '__main__':
    main()
