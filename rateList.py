# -*- coding: utf-8 -*-
import re
import time
import MySQLdb
import requests
import pandas as pd
from time import strftime,localtime
import sys
reload(sys)
sys.setdefaultencoding('utf-8') #其中utf-8为你想输出的字符编码

def printlog(message, data, number, i):
    nowtime = strftime("%Y-%m-%d,%H:%M:%S", localtime())
    log = u"[{0},number={1},i={2}]{3}\n{4}\n".format(nowtime, number, i, message, data)
    logfile.write(log)
    print(log)
#END OF printlog

def rateList2mysql(itemId,sellerId):
    '''该函数将指定商品的评论信息保存到mysql数据库中，
    itemId是商品id，sellerid是卖家id'''
    headersParameters = {
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Mozilla/6.1 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }
    oldjson = ''
    i = 0
    while True:
        i += 1
        url = 'http://rate.tmall.com/list_detail_rate.htm'
        urlparams = {'itemId':str(itemId),'sellerId':str(sellerId),'currentPage':str(i)}
        try:
            r = requests.get(url,params=urlparams,headers=headersParameters)
        except requests.exceptions.ConnectionError:
            print u"网络连接超时，十五秒后重试。"
            time.sleep(15)
            try:
                r = requests.get(url,params=urlparams,headers=headersParameters)
            except requests.exceptions.ConnectionError:
                print u'网络连接超时！舍去此页。', urlparams
                continue
        print '\n['+str(i)+']','url=',r.url
        time.sleep(0.1)
        try:
            response = unicode(r.content, r.encoding).encode('UTF-8')
        except UnicodeDecodeError:
            print u"解码错误！跳过此页。"
            time.sleep(2)
            if i > 99:
                return
        else:
            print response
            #去除天猫返回的json中不和json规范的部分，即只保留中括号中的内容
            #用''.join()而不用[0]索引是为了防止匹配不成功出发错误中断程序
            newjson = ''.join(re.findall(r'\"rateList\":(\[.*?\])\,\"searchinfo\"',response))
            if newjson == '':#如果匹配失败，则尝试老版本的正则
                newjson = ''.join(re.findall(r'\"rateList\":(\[.*?\])\,\"tags\"',response))
            print 'newjson:'
            print newjson
            if newjson == oldjson:  #当请求页码超过最大页码后，返回页面为最大页码页面，以此作为结束条件
                endtime = time.asctime(time.localtime(time.time()))
                print u'\a\n“累计评价”数据采集完成：)\t\t', endtime, '\n','*'*80
                return
            mytable = pd.read_json(newjson)
            for item in mytable.values:
                sql = u"INSERT INTO "+unicode(db_config["tablename"])+u" VALUES ("
                for j in item:
                    temp = re.sub(r'\"', r'\\"', unicode(j))
                    sql += u'\n"' + temp + u'",'
                sql = sql[:-1]
                sql += u');'
                print sql
                # 使用cursor()方法获取操作游标
                try:#MySQLdb不支持长连接，在操作数据库前检查连接是否过期，过期则重连
                    db.ping(True)
                except:
                    db = MySQLdb.connect(db_config["hostname"],
                                          db_config["username"],
                                          db_config["password"],
                                          db_config["databasename"],
                                          charset='utf8')
                # 使用cursor()方法获取操作游标 
                cursor = db.cursor()
                try:
                    #使用execute方法执行SQL语句
                    cursor.execute(sql)
                    cursor.close()
                    # 提交到数据库执行
                    db.commit()
                except:
                #Rollback in case there is any error
                    db.rollback()
            oldjson = newjson
#END OF rateList2mysql

#在此处设置数据库连接信息
db_config = {
    "hostname": "localhost",#主机名
    "username": "root",#数据库用户名
    "password": "root",#数据库密码
    "databasename": "tmalldata",#要存入数据的数据库名
    "tablename": "rateList"#要存入数据的表名
    }
#打开日志文件
logfile = open('rateListLog.txt', 'a')
# 打开数据库连接
db = MySQLdb.connect(db_config["hostname"],
                     db_config["username"],
                     db_config["password"],
                     db_config["databasename"],
                     charset='utf8')
# 抓取数据
#rateList2mysql(44090725053, 725677994)
printlog(u'测试日志功能', u'OK', 23, 56)
'''
itemIdList = open('itemId.txt', 'r').readlines()
sellerIdList = open('sellerId.txt', 'r').readlines()
number = 0 #已经爬取过数据的商品的个数
for (itemId,selllerId) in zip(itemIdList, sellerIdList)[number:]:
    number += 1
    print u'第['+str(number)+u']个商品：'
    time.sleep(2)
    rateList2mysql(int(itemId), int(selllerId))
    #exit(0)
'''
#关闭数据库连接
db.close()
#关闭日志文件
logfile.close()

'''
创建数据库时就设置好字符编码，防止中文乱码
CREATE DATABASE tmalldata DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
创建数据表
CREATE TABLE rateList(
aliMallSeller text,
anony text,
appendComment text,
attributes text,
attributesMap text,
aucNumId text,
auctionPicUrl text,
auctionPrice text,
auctionSku text,
auctionTitle text,
buyCount text,
carServiceLocation text,
cmsSource text,
displayRatePic text,
displayRateSum text,
displayUserLink text,
displayUserNick text,
displayUserNumId text,
displayUserRateLink text,
dsr text,
fromMall text,
fromMemory text,
gmtCreateTime text,
id text,
pics text,
picsSmall text,
position text,
rateContent text,
rateDate text,
reply text,
sellerId text,
serviceRateContent text,
structuredRateList text,
tamllSweetLevel text,
tmallSweetPic text,
tradeEndTime text,
tradeId text,
useful text,
userIdEncryption text,
userInfo text,
userVipLevel text,
userVipPic  text);
'''
