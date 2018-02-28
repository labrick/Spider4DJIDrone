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

#----------------------------------------------------------------------------
def saveDeviceName(deviceDict):
    filep = open("deviceNickname.json", 'w')
    js = json.dumps(deviceDict, ensure_ascii=False, indent = 4)
    filep.write(js)
    filep.close()

