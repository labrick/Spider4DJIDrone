#! /usr/bin/python3
#-*- coding: utf8 -*-

import common
import sys
import getopt

from sqliteWrapper import SqliteWrapper

def writeDevice2Json(djiDevice):
    deviceDict = {}
    for each in djiDevice:
        deviceDict[each] = []
    common.saveDeviceName(deviceDict)

def getPopularity(argv):
    linkList, link2DeviceList = getLinkDevice(argv)
    num = len(link2DeviceList)
    djiDevicePopularity = []
    for i in rang(num):
        tmpPolularity = {}
        djiDevice = list(set(link2DeviceList[i]))
        djiDevice.remove("")
        writeDevice2Json(djiDevice)

        for element in djiDevice:
            tmpPolularity[element] = 0;

        for index in range(len(link2DeviceList[0])):
            tmpPolularity[link2DeviceList[i][index]] += 1
        djiDevicePopularity.append(tmpPolularity)
    return djiDevicePopularity

def checkInputVlidation(argv):
    if len(argv) > 3:
        print("Too many months!!!")
        sys.exit()
    num = len(argv)
    for i in range(num):
        date = argv[i]
        if len(date) != 6 or (date.isdigit() == False):
            print("Invalid Arguments!!!")
            sys.exit()
        year,month =int(date[:4]), int(date[4:6]);
        if year < 2010 or month <=0 or month >=13:
            print("Invalid Arguments")
            sys.exit()

def parseParam(argv):
    checkInputVlidation(argv)
    period = ''
    try:
        opts, args = getopt.getopt(argv, "hp",["period="])
    except getopt.GetoptError:
        print("spider4DJIDrone.py -p <period> month1 month2 month3")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("spider4DJIDrone.py -p <period> month1 month2 month3")
        elif opt == '-p':
            period = arg

    return period, argv[2:]

def getLinkDevice(argv):
    period, months = parseParam(argv)
    num = len(months)

    #Add code here
    sqliteWrapper = SqliteWrapper("C222")
    linkList = sqliteWrapper.getPostLink("2018-02", "2018-03")
    link2DeviceList = sqliteWrapper.getDevice("2018-02", "2018-03")
    #end

    #link2DeviceList is a list of list
    return linkList, link2DeviceList
def getResult(argv):
    djiDevicePopularity = getPopularity(argv)
    num = len(djiDevicePopularity)
    valueListPlot = []
    for i in rang(num):
        # init values
        nameList = []
        valueList = []
        deviceSeries = {'Osmo':0, 'Osmo Mobile':0, 'Spark':0, 'Mavic Pro':0, 'Mavic Air':0, 'Phantom 4/4Pro':0, 'Phantom 3/3SE':0, 'Inspire':0, 'Other':0}
        # Make sure the initial value is zero
        for key in deviceSeries:
            deviceSeries[key] = 0
        # Classify the devices
        for key in djiDevicePopularity[i]:
            if key == 'osmo mobile' or key == 'osmo mobile 2':
                deviceSeries['Osmo Mobile'] += djiDevicePopularity[i][key]
            elif key == 'osmo' or key == 'osmo＋' or key == 'osmo pro' or key == 'osmo raw':
                deviceSeries['Osmo'] += djiDevicePopularity[i][key]
            elif key == '晓spark':
                deviceSeries['Spark'] += djiDevicePopularity[i][key]
            elif key == 'mavic pro' or key == 'mavic pro 铂金版':
                deviceSeries['Mavic Pro'] += djiDevicePopularity[i][key]
            elif key == 'mavic air':
                deviceSeries['Mavic Air'] += djiDevicePopularity[i][key]
            elif key == '精灵4a' or key == '精灵4 pro' or key == '精灵4':
                deviceSeries['Phantom 4/4Pro'] += djiDevicePopularity[i][key]
            elif key == '精灵3' or key == '精灵3 se':
                deviceSeries['Phantom 3/3SE'] += djiDevicePopularity[i][key]
            elif key == '悟1' or key == '悟2' or key == '悟raw' or key == '悟pro':
                deviceSeries['Inspire'] += djiDevicePopularity[i][key]
            else:
                deviceSeries['Other'] += djiDevicePopularity[i][key];
        deviceSerieSorted = sorted(deviceSeries.items(), key = lambda deviceSeries:deviceSeries[0]);
        for index in deviceSerieSorted:
            if index[1] == 0:
                continue
            nameList.append(index[0]);
            valueList.append(index[1])
        valueListPlot.append(valueList)
    return nameList, valueListPlot

def main(argv):
    getResult(argv)

if __name__ == "__main__":
    main(sys.argv[1:])
