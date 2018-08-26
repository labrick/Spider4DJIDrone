#! /usr/bin/env python
#-*- coding: utf8 -*-

'''
 > File Name: sendEmail.py
 > Author:
 > Email:
 > Created Time: Mon 12 Mar 2018 08:13:31 PM CST
'''
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import parseaddr, formataddr

def sendEmail():
    # Basic Imformation
    mailto_list = ['1349501292@qq.com']
    mail_host = 'smtp.163.com'
    mail_user = 'wangfuan361'
    mail_pass = 'job4netease'
    me = 'wangfuan361<wangfuan361@163.com>'

    msg = MIMEMultipart()
    msg['Subject'] = 'Result'
    msg['From'] = me
    msg['To'] = ';'.join(mailto_list)

    body = """
    <h1>The Popularity of DJI Devices</h1>
    <img src="cid:image1"/>
    <img src="cid:image2"/>
    """
    msg.attach(MIMEText(body, 'html', 'utf-8'))
    with open('bar.png', 'rb') as f:
        msgImage = MIMEImage(f.read())
    msgImage.add_header('Content-ID','<image1>')
    with open('pie.png', 'rb') as f:
        msgImage = MIMEImage(f.read())
    msgImage.add_header('Content-ID','<image2>')
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
    sendEmail()
if __name__ == "__main__":
    main()
