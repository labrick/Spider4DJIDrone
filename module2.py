#!/usr/bin/python3

from module1 import linkList, link2DeviceList

linkListUnident = []
djiDevicePopularity = {}
djiDevice = []

def getUnidentLinkList(linkList, link2DeviceList):
    linkListUnident =[]

    djiDevice = list(set(link2DeviceList))
    djiDevice.remove("")

    djiDevicePopularity = {}
    for element in djiDevice:
        djiDevicePopularity[element] = 0;

    for index in range(len(link2DeviceList)):
        if link2DeviceList[index] == "":
            linkListUnident.append(linkList[index])
        else:
            djiDevicePopularity[link2DeviceList[index]] += 1

    return linkListUnident, djiDevicePopularity, djiDevice

def main():
    linkListUnident,djiDevicePopularity, djiDevice = getUnidentLinkList(linkList, link2DeviceList)
    print(linkListUnident)
    print(djiDevicePopularity)
    print(djiDevice)

if __name__ == '__main__':
    main()

