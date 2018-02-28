#!/usr/bin/python3

import http.client as httplib
from lxml import etree

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
    page = etree.HTML(html.lower().decode('utf-8'))

    # analyse html title
    elements = page.xpath(u'''/html/head/title''')

    # all string need to search
    allStr = elements[0].text

    deviceNames = common.getDeviceName()
    for deviceName, nicknameList in deviceNames.items():
        if allStr.find(deviceName) != -1:
            djiDevicePopularity[deviceName] += 1
            return      # analyse over, but really?
        for nickname in nicknameList:
            if allStr.find(nickname) != -1:
                djiDevicePopularity[deviceName] += 1
                return

    # print(elements[0].text)

def main():
    for url in linkList:
        getHtml(url)
        print("get " + url + " OK!!!")

if __name__ == '__main__':
    main()
