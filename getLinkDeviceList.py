import requests
from lxml import etree

POST_URL = 'https://bbs.dji.com/'
linkList = []
link2DeviceList = []

def getHtml(html):
    page = requests.get(html).content.decode('utf-8')
    # print(page)
    return etree.HTML(page.lower())

def getLinkDeviceList(baseUrl):
    html = getHtml(baseUrl)
    linkList = html.xpath('//tbody/tr/th/p[1]/a[1]/@href')
    link2DeviceList = html.xpath('//tbody/tr/th/p[2]/em[2]/text()[1]')

    for index in range(len(linkList)):
        linkList[index] = POST_URL + linkList[index]

    for index in range(len(link2DeviceList)):
        link2DeviceList[index] = link2DeviceList[index].replace("发表于", '')
        link2DeviceList[index] = link2DeviceList[index].replace("用户", '')

    return linkList, link2DeviceList

def main():
    baseUrl = 'https://bbs.dji.com/forum-60-1.html'    # DJI社区
    linkList, link2DeviceList = getLinkDeviceList(baseUrl)

    for each in linkList:
        print(each)
    for each in link2DeviceList:
        print(each)

if __name__ == '__main__':
    main()

