#! /usr/bin/env python
#-*- coding: utf8 -*-

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
zhfont = mpl.font_manager.FontProperties(fname='/usr/share/fonts/truetype/arphic/uming.ttc')

def addLabels(rects):
    for rect in rects:
        width = rect.get_width()
        plt.text(width,rect.get_y() + rect.get_height()/ 2, width, ha = 'left', va ='center')
        rect.set_edgecolor('white')

def plotPie(nameList, valueList,month):
    if(len(nameList) != len(valueList)):
        print('Error: the parameters must have same lenth!!!')
        return
    plt.clf()
    pi = plt.pie(valueList,labels=nameList,autopct='%1.1f%%')
    for font in pi[1]:
        font.set_fontproperties(zhfont)
    plt.title('DJI产品流行度分析\n数据来源:https://bbs.dji.com/forum-60-1.html\n统计时间: '+month,fontproperties=zhfont)
    plt.savefig("pie.png")

def plotBar(nameList, valueList, months):
    barNum = len(valueList)
    if barNum == 0:
        print('Error: There is no data !!!!!!!!')
        return
    index = np.arange(len(valueList[0]))
    # two bars for each device
    index = index * (barNum + 0.5)
    colors = ['r','b','g','y']
    for i in range(barNum):
        rect = plt.barh(index+i, valueList[i], color=colors[i%4],label = months[i]);
        addLabels(rect)
    plt.yticks(index+(barNum-1)/2, nameList,fontproperties=zhfont)
    plt.xlabel('帖子数量', fontproperties=zhfont, position =(0.95,0))
    #plt.ylabel('DJI产品型号',fontproperties=zhfont)
    plt.title(u'DJI产品流行度分析\n数据来源:https://bbs.dji.com/forum-60-1.html',fontproperties=zhfont)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5,-0.05),ncol=3,fancybox=True)
    plt.savefig("bar.png")

def main():
    nameList = ['mavic', 'spark', 'inspire']
    valueList = [[10,5,6]]
    plotBar(nameList, valueList)
    plotPie(nameList, valueList[0])

if __name__ == "__main__":
    main()
