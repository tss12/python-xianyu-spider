#encoding=utf8 

from bs4 import BeautifulSoup
import urllib
import urllib.request
import time
import random
import re
import types

import smtplib  
from email.mime.text import MIMEText  
from email.header import Header  




def gen_req(url):
    req = urllib.request.Request(
        url,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3)'
            ' AppleWebKit/537.36 (KHTML, like Gecko)'
            ' Chrome/35.0.1916.47 Safari/537.36'
        }
    )
    return req


def fish_scrawler(url):
    req = gen_req(url)
    r = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(r, "html.parser")
    # print(soup)
    list = soup.find_all('div',class_="ks-waterfall")
    for info in list:
        try:
            price = info.find('span',class_="price").find('em').get_text()
            location = info.find('div',class_="item-location").get_text()
            desc = info.find('div',class_="item-brief-desc").get_text()
            url = info.find('div',class_="item-pic").find('a').get('href')
            title = info.find('div',class_="item-pic").find('a').get('title')
            dr = re.compile(r'<[^>]+>',re.S)
            title = dr.sub('',title)
            priceStr = ""
            price1 = priceStr.join(price)
            price2 = float(price1)
            price3 = int(price2)
            
            print(price3)
            print(location)
            print(desc)
            print(url)
            print(title)
        except:
            print('解析出错了')
            continue
        try:    
            if price3 < 1200:
                file_handler = open('/mydata/fish/swimCard/data.txt',"a")
                # file_handler = open("D:/python/xianyu/data.txt","a")
                file_handler.write(title+'|'+str(price3)+'|'+desc+'|'+location+'|'+url+'\n')
                
                file_handler.close()

            
        except:
            print('写入出错了')
            continue


def send_email(SMTP_host, from_account, from_passwd, to_account, subject, content):
    email_client = smtplib.SMTP(SMTP_host)
    email_client.login(from_account, from_passwd)

    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')  # subject
    msg['From'] = from_account
    msg['To'] = to_account
    email_client.sendmail(from_account, to_account, msg.as_string())
    email_client.quit()


if __name__ == '__main__':
    # url = 'https://s.2.taobao.com/list/list.htm?spm=2007.1000337.0.0.mTx4fq&st_trust=1&page='+str(page)+'&q=%D3%CE%D3%BE%BF%A8&ist=1'
    for page in range(1,100):
        url = 'https://s.2.taobao.com/list/list.htm?spm=2007.1000337.0.0.mTx4fq&st_trust=1&page='+str(page)+'&q=%D3%CE%D3%BE%BF%A8&ist=1&divisionId=110100'
        fish_scrawler(url)
        second = random.randint(2,10)
        time.sleep(second)
    
    send_email('smtp.163.com','yoursendemail','yourpassword','yourreceviedemail','闲鱼低价(低于1200游泳卡)','详情见附件')
    #contact me by mail playactors@163.com for any question    
