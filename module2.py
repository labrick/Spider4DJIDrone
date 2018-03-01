#!/usr/bin/python3

#variable passed by the first step
linkList = [
        "https://bbs.dji.com/thread-6833-1-1.html",
        "https://bbs.dji.com/thread-6833-1-1.html",
        "https://bbs.dji.com/thread-2832-1-1.html",
        "https://bbs.dji.com/thread-2832-1-1.html",
        "https://bbs.dji.com/thread-2832-1-1.html",
    ]
link2DeviceList = ["mavic pro", "mavic air", "","spark", "spark"]

#variable to be passed to next step
linkListUnident =[]

#get djiDevice
djiDevice = list(set(link2DeviceList))
djiDevice.remove("")

#reset 
djiDevicePopularity = {}
for element in djiDevice:
    djiDevicePopularity[element] = 0;

#calculate the popularity for now
for index in range(len(link2DeviceList)):
    if link2DeviceList[index] == "":
        linkListUnident.append(linkList[index])
    else:
        djiDevicePopularity[link2DeviceList[index]] += 1;

print(linkListUnident)
print(djiDevicePopularity)
print(djiDevice)
