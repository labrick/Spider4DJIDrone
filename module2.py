#!/usr/bin/python3

from getLinkDeviceList import getLinkDevice
import common

linkListUnident = []
djiDevicePopularity = {}

def writeDevice2Json(djiDevice):
    deviceDict = {}
    for each in djiDevice:
        deviceDict[each] = []
    common.saveDeviceName(deviceDict)

def getUnidentLinkList(linkList, link2DeviceList):
    linkListUnident =[]

    djiDevice = list(set(link2DeviceList))
    djiDevice.remove("")

    writeDevice2Json(djiDevice)

    djiDevicePopularity = {}
    for element in djiDevice:
        djiDevicePopularity[element] = 0;

    for index in range(len(link2DeviceList)):
        if link2DeviceList[index] == "":
            linkListUnident.append(linkList[index])
        else:
            djiDevicePopularity[link2DeviceList[index]] += 1

    print("unident link num:" + str((len(linkListUnident))))

    return linkListUnident, djiDevicePopularity

def getLinkPopularity():
    linkList, link2DeviceList = getLinkDevice()
    linkListUnident, djiDevicePopularity = getUnidentLinkList(linkList, link2DeviceList)

def main():
    linkList, link2DeviceList = getLinkDevice()
    linkListUnident, djiDevicePopularity = getUnidentLinkList(linkList, link2DeviceList)

    for each in linkListUnident:
        print(each)
    for djiDeviceKey, popularityValue in djiDevicePopularity.items():
        print("%12s:\t%d" % (djiDeviceKey, popularityValue))

if __name__ == '__main__':
    main()

