import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import gmtime, sleep, strftime
import requests
import datetime
import csv
import re
from lxml import etree
import pandas as pd


class github_serch:

    def __init__(self):
        pass

    def login_github(self,username="bc-w",password="bpsb-2006"):#登陆Github
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
            print("登录Github成功,正在检索关键字g")
            #keyword = input("输入搜索关键字:")
            sleep(3)
            global n #搜索计数
            n = 0
            turl = []
            csv_file = open('leak.csv', 'w', encoding='utf-8', newline='')
            writer = csv.writer(csv_file)
            writer.writerow(['url',"upload time","username/entry name","filename"])
            f1 = open('上传时间.txt', 'w')
            for page in range(1,3): #检索1到2页匹配关键词的结果
                search_code = "https://github.com/search?p="+str(page)+"&q=gx&type=Code"
                resp = s.get(search_code)
                results_code = resp.text
                dom_tree_code = etree.HTML(results_code)
                reg = re.compile("[^/]+(?!.*/)") #正则过滤上传文件名
                # 获取存在信息泄露的链接地址
                #Urls = dom_tree_code.xpath('//div[@class="flex-auto min-width-0 col-10"]/a[2]/@href') #获取链接地址
                Urls = dom_tree_code.xpath('//div[@class="f4 text-normal"]/a/@href')
                users = dom_tree_code.xpath('//div[@class="flex-shrink-0 text-small text-bold"]/a[1]/@href') # 获取用户名
                datetime = dom_tree_code.xpath('//relative-time/text()') # 获取上传时间
                filename = dom_tree_code.xpath('//div[@class="f4 text-normal"]/a/@title')
                str1 = "https://github.com"
                for i in range(len(Urls)):
                    n = n + 1
                    writer.writerow([str1+str(Urls[i]),datetime[i],users[i],re.findall(reg,str(filename[i]))])
                    f1.write(str(datetime[i]) + "\n")
            print("共搜索到" + str(n) + "个结果，详见附件")
            return s
        except Exception as e:
            print("产生异常")
            print(e)

    def get_timestamp(self): #创建时间戳
        f3 = open('上传时间.txt', 'r')
        f4 = open('上传时间戳.txt', 'w')
        for i in f3:
            i = i.strip("\n")
            ti = datetime.datetime.strptime(i, "%b %d, %Y")
            timeStamp = (time.mktime(ti.timetuple()))
            f4.write(str(timeStamp) + "\n")

    def edit_csv(self): #查询结果时间升序排序
        df = pd.read_csv("leak.csv", encoding='utf-8')
        df["upload time"] = pd.to_datetime(df["upload time"]) #转换为时间对象
        df.sort_values(by="upload time", ascending=True,inplace=True)
        df.to_csv('finally.csv', encoding='utf-8', index=False)

    def send_mail(self): #发送邮件
        f2 = open('上传时间戳.txt', 'r')
        n1 = 0
        date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        username = 'wang@gx.com' #邮件地址
        password = 'jllx@2020'#邮件密码
        sender = 'wang@gx.com'
        receiver = ["wang@gx.com"]
        receiver1 = ["wang@gx.com","jiang@gx.com"]
        now_time = time.time() #获取当前时间戳
        time1 = now_time - (72*3600) #前推72小时
        for ff in f2: #检索上传时间
            i2 = float(ff.strip("\n"))
            time1 = float(time1)
            if i2 > time1: #判断上传时间,检索72小时上传文件
                n1 = n1 + 1
        if n1 == 0: #判断上传数量
            try:
                subject = 'Github未发现新上传代码'
                msg = MIMEMultipart('mixed')
                msg['Subject'] = subject
                msg['From'] = 'Github监控'
                att1 = MIMEText(open('finally.csv', 'rb').read(), 'base64', 'utf-8')
                att1["Content-Type"] = 'application/octet-stream'
                att1.add_header('Content-Disposition', 'attachment', filename='fujian.csv')
                msg.attach(
                    MIMEText("Dear all: \r\n\r\n"+str(date)+" 检测关键字gx,Github检测到上传代码"+str(n)+"个,未发现新上传代码，详见附件\r\n\r\n"))
                msg.attach(att1)
                smtp = smtplib.SMTP(host="partner.outlook.cn")
                smtp.connect(host='partner.outlook.cn')
                smtp.starttls()
                smtp.login(username, password)
                smtp.sendmail(sender, receiver, msg.as_string())
                smtp.quit()
                print("邮件发送成功")
            except Exception as err:
                print(err)
        else:
            try:
                subject = 'Github发现新上传代码'
                msg = MIMEMultipart('mixed')
                msg['Subject'] = subject
                msg['From'] = 'Github监控'
                att1 = MIMEText(open('finally.csv', 'rb').read(), 'base64', 'utf-8')
                att1["Content-Type"] = 'application/octet-stream'
                att1.add_header('Content-Disposition', 'attachment', filename='fujian.csv')
                msg.attach(
                    MIMEText("Dear all: \r\n\r\n" + str(date) + " 检测关键字gx,发现新上传代码，Github检测到新上传代码" + str(
                        n1) + "个,详见附件\r\n\r\n"))
                msg.attach(att1)
                smtp = smtplib.SMTP(host="partner.outlook.cn")
                smtp.connect(host="partner.outlook.cn")
                smtp.starttls()
                smtp.login(username, password)
                smtp.sendmail(sender, receiver1, msg.as_string())
                smtp.quit()
                print("邮件发送成功")
            except Exception as err:
                print(err)

    def run(self):
        g.login_github()
        g.get_timestamp()
        g.edit_csv()
        g.send_mail()
       
if __name__ == '__main__':
    g = github_serch()
    g.run()
    