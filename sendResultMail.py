#!/usr/bin/python3
#-*- coding: UTF-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import parseaddr, formataddr
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from anaEachPage import getPopularity

zhfont = mpl.font_manager.FontProperties(fname='/usr/share/fonts/truetype/arphic/uming.ttc')

def getResult():
    # init values
    nameList = []
    valueList = []
    deviceSeries = {'Osmo':0, 'Osmo Mobile':0, 'Spark':0, 'Mavic Pro':0, 'Mavic Air':0, 'Phantom 4/4Pro':0, 'Phantom 3/3SE':0, 'Inspire':0, 'Other':0}
    djiDevicePopularity = getPopularity()
    # Make sure the initial value is zero
    for key in deviceSeries:
        deviceSeries[key] = 0
    # Classify the devices 
    for key in djiDevicePopularity:
        if key == 'osmo mobile' or key == 'osmo mobile 2':
            deviceSeries['Osmo Mobile'] += djiDevicePopularity[key]
        elif key == 'osmo' or key == 'osmo＋' or key == 'osmo pro' or key == 'osmo raw':
            deviceSeries['Osmo'] += djiDevicePopularity[key]
        elif key == '晓spark':
            deviceSeries['Spark'] += djiDevicePopularity[key]
        elif key == 'mavic pro' or key == 'mavic pro 铂金版':
            deviceSeries['Mavic Pro'] += djiDevicePopularity[key]
        elif key == 'mavic air':
            deviceSeries['Mavic Air'] += djiDevicePopularity[key]
        elif key == '精灵4a' or key == '精灵4 pro' or key == '精灵4':
            deviceSeries['Phantom 4/4Pro'] += djiDevicePopularity[key]
        elif key == '精灵3' or key == '精灵3 se':
            deviceSeries['Phantom 3/3SE'] += djiDevicePopularity[key]
        elif key == '悟1' or key == '悟2' or key == '悟raw' or key == '悟pro':
            deviceSeries['Inspire'] += djiDevicePopularity[key]
        else:
            deviceSeries['Other'] += djiDevicePopularity[key];
    deviceSerieSorted = sorted(deviceSeries.items(), key = lambda deviceSeries:deviceSeries[0]);
    for index in deviceSerieSorted:
        if index[1] == 0:
            continue
        nameList.append(index[0]);
        valueList.append(index[1])
    valueListPlot = [];
    valueListPlot.append(valueList)
    plotBar(nameList, valueListPlot)
    plotPie(nameList, valueListPlot[0])

def addLabels(rects):
    for rect in rects:
        width = rect.get_width()
        plt.text(width,rect.get_y() + rect.get_height()/ 2, width, ha = 'left', va ='center')
        rect.set_edgecolor('white')

def plotPie(nameList, valueList):
    if(len(nameList) != len(valueList)):
        print('Error: the parameters must have same lenth!!!')
        return
    plt.clf()
    pi = plt.pie(valueList,labels=nameList,autopct='%1.1f%%')
    for font in pi[1]:
        font.set_fontproperties(zhfont)
    plt.title(u'DJI产品流行度分析\n数据来源:https://bbs.dji.com/forum-60-1.html',fontproperties=zhfont)
    plt.savefig("pie.png")

def plotBar(nameList, valueList):
    barNum = len(valueList)
    if barNum == 0:
        print('Error: There is no data !!!!!!!!')
        return
    index = np.arange(len(valueList[0]))
    # two bars for each device
    index = index * barNum
    colors = ['r','b','g','y']
    for i in range(barNum):
        rect = plt.barh(index+i, valueList[i], color=colors[i%4]);
        addLabels(rect)
    plt.yticks(index+(barNum-1)/2, nameList,fontproperties=zhfont)
    plt.xlabel('帖子数量', fontproperties=zhfont)
    plt.ylabel('DJI产品型号',fontproperties=zhfont)
    plt.title(u'DJI产品流行度分析\n数据来源:https://bbs.dji.com/forum-60-1.html',fontproperties=zhfont)
    plt.savefig("bar.png")

def sendMail():
    # Basic Imformation
    mailto_list = ['xxxxx@xx.com']
    mail_host = 'smtp.163.com'
    mail_user = 'xxxxxxx'
    mail_pass = 'xxxx'
    me = 'xxxxxx<xxxx@xxxx>'

    msg = MIMEMultipart()
    msg['Subject'] = 'Result'
    msg['From'] = me
    msg['To'] = ';'.join(mailto_list)

    body = """
    <h1>The Popularity of DJI Devices</h1>
    <img src="cid:image1"/>
    """
    msg.attach(MIMEText(body, 'html', 'utf-8'))
    with open('result.png', 'rb') as f:
        msgImage = MIMEImage(f.read())
    msgImage.add_header('Content-ID','<image1>')
    msg.attach(msgImage)

    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_user, mail_pass)
        server.sendmail(me, mailto_list, msg.as_string())
        server.close()
        print ('done')
    except Exception as e:
        print (str(e))

def main():
    getResult()
    #sendMail()

if __name__ == '__main__':
    main()
