#!/usr/bin/python3

import http.client as httplib
from lxml import etree

from module2 import dji_device_popularity
from module2 import link_list

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
    print(elements[0].text)
    print(elements[0].text.find("精灵"))
    print(elements[0].text.find("phantom"))

# print(dji_device_popularity)
# print(link_list)

def main():
    for url in link_list:
        getHtml(url)
        print("get " + url + " OK!!!")

if __name__ == '__main__':
    main()
