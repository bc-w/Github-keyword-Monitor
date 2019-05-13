#import importlib,sys
#import configparser
#import os
#import re
import smtplib
import time
#import sys
#import traceback
#from email import encoders
#from email.header import Header
#from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#from email.utils import formataddr, parseaddr
from time import gmtime, sleep, strftime
import requests
import csv
from lxml import etree


class github_serch:
    def __init__(self):
        pass
    def login_github(self,username="bc-w",password="github登录密码"):#登陆Github
        #初始化参数
        login_url = 'https://github.com/login'
        session_url = 'https://github.com/session'
        try:
            #获取session
            s = requests.session()
            resp = s.get(login_url).text
            dom_tree = etree.HTML(resp)
            key = dom_tree.xpath('//input[@name="authenticity_token"]/@value')
            user_data = {
                'commit': 'Sign in',
                'utf8': '✓',
                'authenticity_token': key,
                'login': username,
                'password': password
            }
            #发送数据并登陆
            s.post(session_url,data=user_data)
            s.get('https://github.com/settings/profile')
            print("登录Github成功,正在检索关键字xxxxxxx")
            #keyword = input("输入搜索关键字:")
            sleep(6)
            global n
            n = 0
            turl = []
            csv_file = open('leak.csv', 'w', encoding='utf-8', newline='')
            writer = csv.writer(csv_file)
            writer.writerow(['url',"upload time"])
            f1 = open('上传时间.txt', 'w')
            for page in range(1,3): #检索1到3页匹配关键词的结果
                search_code ="https://github.com/search?p="+str(page)+"&q=xxxxxxx&type=Code"
                resp = s.get(search_code)
                results_code = resp.text
                dom_tree_code = etree.HTML(results_code)
                # 获取存在信息泄露的链接地址
                Urls = dom_tree_code.xpath('//div[@class="flex-auto min-width-0 col-10"]/a[2]/@href')
                #users = dom_tree_code.xpath('//a[@class="text-blod"]/text()')  # 获取用户名
                datetime = dom_tree_code.xpath('//relative-time/text()')  # 获取上传时间
                for i in range(len(Urls)):
                    n = n + 1
                    for url in Urls:
                        url = "https://github.com"+url
                        turl.append(url)
                    writer.writerow([turl[i],datetime[i]])
                    f1.write(str(datetime[i]) + "\n")
            print("共搜索到"+str(n)+"个结果，详见附件")
            return s
        except Exception as e:
            print("产生异常")
            print(e)
            
    def send_mail(self): #发送邮件
        f2 = open('上传时间.txt', 'r')
        str1 = "2019"
        n1 = 0
        date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        username = 'wbc19847@163.com'
        password = '邮箱登录密码'
        sender = 'wbc19847@163.com'
        receiver = ["wbc19847@163.com"]
        for ff in f2: #检索上传时间
            if str1 in ff:
                n1 = +1
        if n1 == 0 and n <= 13: #判断上传时间与数量
            try:
                subject = 'Github未发现新上传代码'
                msg = MIMEMultipart('mixed')
                msg['Subject'] = subject
                msg['From'] = 'Github监控'
                att1 = MIMEText(open('leak.csv', 'rb').read(), 'base64', 'utf-8')
                att1["Content-Type"] = 'application/octet-stream'
                att1.add_header('Content-Disposition', 'attachment', filename='fujian.csv')
                msg.attach(
                    MIMEText("Dear all: \r\n\r\n"+str(date)+" 检测关键字xxxxxxx,Github检测到上传代码"+str(n)+"个,未发现新上传代码，详见附件\r\n\r\n"))
                msg.attach(att1)
                smtp = smtplib.SMTP()
                smtp.connect('partner.outlook.cn')
                smtp.starttls()
                smtp.login(username, password)
                smtp.sendmail(sender, receiver, msg.as_string())
                smtp.quit()
                print("邮件发送成功")
            except Exception as err:
                print(err)
        else:
            #print("检测到新上传文件"+str(n1)+"个")
            try:
                subject = 'Github发现新上传代码'
                msg = MIMEMultipart('mixed')
                msg['Subject'] = subject
                msg['From'] = 'Github监控'
                att1 = MIMEText(open('leak.csv', 'rb').read(), 'base64', 'utf-8')
                att1["Content-Type"] = 'application/octet-stream'
                att1.add_header('Content-Disposition', 'attachment', filename='fujian.csv')
                msg.attach(
                    MIMEText("Dear all: \r\n\r\n" + str(date) + " 检测关键字xxxxxxx,Github检测到上传代码" + str(
                        n1) + "个,发现新上传代码，详见附件\r\n\r\n"))
                msg.attach(att1)
                smtp = smtplib.SMTP()
                smtp.connect('smtp.163.com')
                smtp.starttls()
                smtp.login(username, password)
                smtp.sendmail(sender, receiver, msg.as_string())
                smtp.quit()
                print("邮件发送成功")
            except Exception as err:
                print(err)
    def run(self):
        g.login_github()
        g.send_mail()
       
if __name__ == '__main__':
    g = github_serch()
    g.run()
    