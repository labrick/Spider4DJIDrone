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

def main():
    deviceDict = {
            "spark": ["晓", "晓spark"],
            "mavic pro": ["mavic"],
            "mavic air": [],
            "精灵": [],
            }
    saveDeviceName(deviceDict)

if __name__ == '__main__':
    main()
