#!/usr/bin/python3
#-*- coding: UTF-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import parseaddr, formataddr
import matplotlib.pyplot as plt
#from module2 import djiDevicePopularity

djiDevicePopularity = {'mavic air': 1, 'mavic pro': 1, 'spark': 2}

def getResult():
    nameList = []
    valueList = []
    totalValue = 0
    for value in djiDevicePopularity.values():
        totalValue += value
    totalValue = float(totalValue)
    for key in djiDevicePopularity:
        nameList.append(key)
        valueList.append(djiDevicePopularity[key]/totalValue)
    plt.bar(range(len(valueList)), valueList, color='rgb',tick_label=nameList)
    plt.savefig("result.png")
    
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
    sendMail()

if __name__ == '__main__':
    main()

