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

def getPopularity(period, months):
    linkList, link2DeviceList = getLinkDevice(period, months)
    djiDevicePopularity = []
    num = len(link2DeviceList)
    combineDevices = set()
    for i in range(num):
        combineDevices |= set(link2DeviceList[i])
    djiDevice = list(combineDevices)
    djiDevice.remove("")
    writeDevice2Json(djiDevice)
    for i in range(num):
        tmpPolularity = {}

        for element in djiDevice:
            tmpPolularity[element] = 0;

        for index in range(len(link2DeviceList[0])):
            if link2DeviceList[i][index] != '':
                tmpPolularity[link2DeviceList[i][index]] += 1
        djiDevicePopularity.append(tmpPolularity)
    return djiDevicePopularity

#convert 201801 to 2018-01
def formatMonth(month):
    tmpList = list(month)
    tmpList.insert(4,'-')
    monthFormated = "".join(tmpList)
    return monthFormated 

#get start and end month to fetch data form database
def getStartEndMonth(start,period):
    startYearInt = int(start[:4])
    startMonthInt = int(start[4:6])
    endYearInt = startYearInt 
    endMonthInt = startMonthInt + period 
    if endMonthInt > 12:
        endYearInt += endMonthInt // 12
        endMonthInt = endMonthInt % 12
    end = str(endYearInt) + str(endMonthInt)
    startMonth = formatMonth(start)
    endMonth = formatMonth(end)
    return startMonth, endMonth 

def getLinkDevice(period, months):
   # checkDateValidation(months)
    linkList = []
    link2DeviceList = []
    sqliteWrapper = SqliteWrapper("C222")
    for i in range(len(months)):
        startMonth, endMonth = getStartEndMonth(months[i],period)
        tmpLinkList = sqliteWrapper.getPostLink(startMonth, endMonth)
        if len(tmpLinkList) == 0:
            print("Can't get the data you require from the database")
            sys.exit()
        linkList.append(tmpLinkList)
        tmpLink2DeviceList = sqliteWrapper.getDevice(startMonth, endMonth)
        link2DeviceList.append(tmpLink2DeviceList)
    return linkList, link2DeviceList

def getResult(period,months):
    djiDevicePopularity = getPopularity(period, months)
    num = len(djiDevicePopularity)
    valueListPlot = []
    for i in range(num):
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
            #if index[1] == 0:
            #    continue
            nameList.append(index[0]);
            valueList.append(index[1])
        valueListPlot.append(valueList)
    return nameList, valueListPlot

def main(argv):
    name, value = getResult(argv)
    print(len(name))

if __name__ == "__main__":
    main(sys.argv[1:])
