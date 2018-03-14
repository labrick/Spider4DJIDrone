#!/usr/bin/python3
# coding=UTF-8

import os
import json

def getDeviceName():
    try:
        filep = open("deviceNickname.json")
    except:
        print("can't find deviceNickname.json")
        return None

    allText = filep.read()
    codeList = json.loads(allText)
    return codeList

# deviceDict is dict
# each element is a list
# each member of the list is a nickname of deviceName
# e.g. "晓spark": ["晓", "spark"]
def saveDeviceName(deviceDict):
    originDeviceDict = getDeviceName()
    for deviceName in deviceDict:
        if deviceName in originDeviceDict:
            continue
        else:
            print("new device " + deviceName + ", please add the nickname of the device")
            originDeviceDict[deviceName] = []

    filep = open("deviceNickname.json", 'w')
    js = json.dumps(originDeviceDict, ensure_ascii=False, indent = 4)
    filep.write(js)
    filep.close()

def getJsonContent(filename):
    try:
        filep = open(filename)
    except:
        print("can't find deviceSeries.json")
        return None

    theText = filep.read()
    content = json.loads(theText)
    return content 

def updateJsonContent(inputDict, filename):
    originDict = getJsonContent(filename)
    for item in inputDict:
        if item in originDict:
            list1 = originDict[item]
            list2 = inputDict[item]
            sumlist = list(set(list1) | set(list2))
            originDict[item] = sumlist
        else:
            print("new item " + item)
            originDict[item] = inputDict[item]
    filep = open(filename, 'w')
    js = json.dumps(originDict, ensure_ascii=False, indent = 4)
    filep.write(js)
    filep.close()

def createJson(inputDict, filename):
    filep = open(filename, 'w')
    js = json.dumps(inputDict, ensure_ascii=False, indent = 4)
    filep.write(js)
    filep.close()

def main():
    deviceDict = {
            "spark": ["晓", "晓spark"],
            "mavic pro": ["mavic"],
            "mavic air": [],
            "精灵": [],
            }
    newDict = {
            "Osmo Mobile":['osmo mobile','osmo mobile 2'],
            "Osmo":['osmo','osmo＋','osmo pro', 'osmo raw'],
            "Spark":['晓spark'],
            "Mavic Pro":['mavic pro', 'mavic pro 铂金版'],
            "Mavic Air":['mavic air'],
            "Phantom 4/4pro":['精灵4a','精灵4 pro','精灵4'],
            "Phantom 3/3se":['精灵3','精灵3 se'],
            "Inspire":['悟1','悟2','悟raw','悟pro'],
            "Other":['goggles','如影m','如影mx']
            }
    updateJsonContent(newDict, "deviceDict.json")
    #createJson(newDict, "deviceDict.json")

if __name__ == '__main__':
    main()
