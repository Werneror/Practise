# -*- coding: utf-8 -*-
import re
import os
import sys
import time
import smtplib  
import MySQLdb
import requests
import traceback
import pandas as pd
from time import strftime,localtime
from email.mime.text import MIMEText

#使文件支持中文输出
reload(sys)
sys.setdefaultencoding('utf-8')

#管理员邮箱，接收程序运行信息之用
receiver = ["XXX@XXXX.XXX",]

#在此处设置数据库连接信息
db_config = {
    "hostname": "localhost",#主机名
    "username": "root",#数据库用户名
    "password": "root",#数据库密码
    "databasename": "test",#要存入数据的数据库名
    }

#发送HTTP请求时的HEAD信息，用于伪装为浏览器
headersParameters = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'User-Agent': 'Mozilla/6.1 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }

def printlog(message, data, number, i, logfile):
    '''该函数向logfile输出日志信息，虽然可以输出中文信息，
	但有些平台不支持中文显示，建议使用英文'''
    nowtime = strftime("%Y-%m-%d,%H:%M:%S", localtime())
    log = u"[{0},number={1},page={2}]{3}\t{4}\n".format(nowtime, number, i, message, data)
    logfile.write(log)
#END OF printlog

def send163mail(subject, body, receiver):
    '''按如下配置发送以subject为标题，body为内容的邮件到receiver，
    其中body支持html格式，receiver是列表，每个元素是一个收件人地址'''
    host = 'smtp.163.com'  # 设置发件服务器地址
    port = 25  # 设置发件服务器端口号。注意，这里有SSL和非SSL两种形式
    sender = 'XXXXXXXXX@163.com'  # 设置发件邮箱，一定要自己注册的邮箱
    pwd = '********************'  # 设置发件邮箱的密码，等会登陆会用到

    msg = MIMEText(body, 'html') # 设置正文为符合邮件格式的HTML内容
    msg['subject'] = subject # 设置邮件标题
    msg['from'] = sender  # 设置发送人

        
    s = smtplib.SMTP(host, port)  # 注意！如果是使用SSL端口，这里就要改为SMTP_SSL
    s.login(sender, pwd)  # 登陆邮箱
    for item in receiver:
        msg['to'] = item  # 设置接收人
        s.sendmail(sender, item, msg.as_string())  # 发送邮件
        time.sleep(5)	#谨慎起见，每发一封邮件都暂停5秒
        print('send mail to {0} is over.'.format(item))  #发送成功就会提示
#END OF send163mail

def rateList2mysql(itemId, sellerId, tablename, logfile):
    '''该函数将指定商品的评论信息保存到mysql数据库中的表tablename中，
    itemId是商品id，sellerid是卖家id，同时日志信息会保存在logfile中'''
    oldjson = ''
    i = 0   #i表示页码
    while i<99:	#最多返回99页结果
        i += 1
        url = 'http://rate.tmall.com/list_detail_rate.htm'
        urlparams = {'itemId':str(itemId),'sellerId':str(sellerId),'currentPage':str(i)}
        try:
            r = requests.get(url,params=urlparams,headers=headersParameters)
            printlog(u'Try to open the url:', r.url, number, i, logfile)
            if r.url=="http://err.taobao.com/error1.html":	#跳转到这个页面则暂停20分钟
                printlog(u'Back a error html.', u'ERROR', number, i, logfile)
                time.sleep(1200)
                try:
                    r = requests.get(url,params=urlparams,headers=headersParameters)
                    printlog(u'Try to open the url again:', r.url, number, i, logfile)
                except requests.exceptions.ConnectionError:
                    printlog(u'Failed to open the url.', u'ERROR', number, i, logfile)
                    continue
        except requests.exceptions.ConnectionError:
            time.sleep(10)
            try:
                r = requests.get(url,params=urlparams,headers=headersParameters)
                printlog(u'Try to open the url again:', r.url, number, i, logfile)
            except requests.exceptions.ConnectionError:
                printlog(u'Failed to open the url.', u'ERROR', number, i, logfile)
                continue
        
        printlog(u'Succeed in opening the url.', u'OK', number, i, logfile)
        time.sleep(0.1)
        try:
            response = unicode(r.content, r.encoding).encode('UTF-8')
            printlog(u'Try to unicode the content.', u'waiting...', number, i, logfile)
        except UnicodeDecodeError:
            printlog(u'Failed to unicode the content.', u'ERROR', number, i, logfile)
            time.sleep(1)
            continue

        printlog(u'Succeed in unicoding the content.', u'OK', number, i, logfile)
        #去除天猫返回的json中不和json规范的部分，即只保留中括号中的内容
        #用''.join()而不用[0]索引是为了防止匹配不成功出发错误中断程序
        printlog(u'Try to regular expression matching.', u'waiting', number, i, logfile)
        newjson = ''.join(re.findall(r'\"rateList\":(\[.*?\])\,\"searchinfo\"',response))
        if newjson == '':#如果匹配失败，则尝试老版本的正则
            newjson = ''.join(re.findall(r'\"rateList\":(\[.*?\])\,\"tags\"',response))
        if newjson =='':
            printlog(u'Regual matching results are null.', u'WARN', number, i, logfile)
        printlog(u'Succeed in regularing expression matching.', u'OK', number, i, logfile)
        if newjson == oldjson:  #当请求页码超过最大页码后，返回页面为最大页码页面，以此作为结束条件
            printlog(u'Finished collceting this rates.', u'OK', number, i, logfile)
            return

        printlog(u'Try to analyz Json.', u'waiting', number, i, logfile)
        mytable = pd.read_json(newjson) #不使用to_sql的原因是评论过于复杂，to_sql构造的sql语句常常出错
        printlog(u'Succeed in analyzing Json.', u'OK', number, i, logfile)
        for item in mytable.values:
            sql = u"INSERT INTO "+unicode(tablename)+u" VALUES ("
            for j in item:
                temp = re.sub(r'\"', r'\\"', unicode(j))	#句子中出现"需转义
                if len(temp)>1 and temp[-1]=="\\" and temp[-2]!="\\":	#防止句尾是\将后"转义时SQL语句出错
                    temp = temp[:-1]
                sql += u'\n"' + temp + u'",'
            sql = sql[:-1]
            sql += u');'
            # 使用cursor()方法获取操作游标
            try:#MySQLdb不支持长时间连接，在操作数据库前检查连接是否过期，过期则重连
                db.ping(True)
            except:
                #再次连接数据库
                printlog(u'Try to connect Mysql again.', db_config, number, i, logfile)
                db = MySQLdb.connect(db_config["hostname"],
                                     db_config["username"],
                                     db_config["password"],
                                     db_config["databasename"],
                                     charset='utf8')
                printlog(u'Succeed in connecting Mysql.', u'OK', number, i, logfile)
            # 使用cursor()方法获取操作游标 
            cursor = db.cursor()
            printlog(u'Try to executing the SQL:', u'waiting',  number, i, logfile)
            try:
                #使用execute方法执行SQL语句
                cursor.execute(sql)
                cursor.close()
                # 提交到数据库执行
                db.commit()
            except:
                printlog(u'Failed to execute the SQL. The SQL is:', sql, number, i, logfile)
                #exit(0)	#调试时打开此句。
            printlog(u'Succeed in executing the SQL:', u'OK', number, i, logfile)
        oldjson = newjson
#END OF rateList2mysql

number = 0 #已经爬取过数据的（包括正在爬的）商品的数目 全局变量！
if __name__ == '__main__':
    dirs = os.listdir(os.getcwd())	    #读取目录信息
    dirs.remove('rateList.py')
    dirs.remove('rateList.py~')
    for d in dirs:
        try:

            #打开商品信息文件
            itemIdfile = open(d+'/itemId.txt', 'r')
            itemIdList = itemIdfile.readlines()
            sellerfile = open(d+'/sellerId.txt', 'r')
            sellerIdList = sellerfile.readlines()

            #尝试连接数据库
            tablename = d   #表名等于目录名
            db = MySQLdb.connect(db_config["hostname"],
                                 db_config["username"],
                                 db_config["password"],
                                 db_config["databasename"],
                                 charset='utf8')
            #尝试创建表
            sql = '''CREATE TABLE '''+tablename+'''(
                    aliMallSeller varchar(8),
                    anony varchar(8),
                    appendComment text,
                    attributes text,
                    attributesMap text,
                    aucNumId tinytext,
                    auctionPicUrl tinytext,
                    auctionPrice tinytext,
                    auctionSku tinytext,
                    auctionTitle tinytext,
                    buyCount varchar(20),
                    carServiceLocation tinytext,
                    cmsSource varchar(20),
                    displayRatePic varchar(20),
                    displayRateSum varchar(20),
                    displayUserLink tinytext,
                    displayUserNick varchar(20),
                    displayUserNumId tinytext,
                    displayUserRateLink tinytext,
                    dsr tinytext,
                    fromMall varchar(8),
                    fromMemory tinytext,
                    gmtCreateTime varchar(22),
                    id varchar(22),
                    pics text,
                    picsSmall tinytext,
                    position tinytext,
                    rateContent text,
                    rateDate varchar(30),
                    reply text,
                    sellerId varchar(20),
                    serviceRateContent text,
                    structuredRateList tinytext,
                    tamllSweetLevel tinytext,
                    tmallSweetPic tinytext,
                    tradeEndTime varchar(20),
                    tradeId tinytext,
                    useful varchar(8),
                    userIdEncryption tinytext,
                    userInfo tinytext,
                    userVipLevel varchar(8),
                    userVipPic tinytext);'''
            # 使用cursor()方法获取操作游标
            cursor = db.cursor()
            #使用execute方法执行SQL语句
            cursor.execute(sql)
            cursor.close()
            # 提交到数据库执行
            db.commit()

            # 抓取数据
            for (itemId,selllerId) in zip(itemIdList, sellerIdList)[number:]:
                time.sleep(1)	#谨慎起见
                number += 1
                #打开日志文件
                logfile = open(d+'/{0}rateListLog.txt'.format(number), 'a')
                printlog(u'Start collceting this rates.', u'OK', number, 0, logfile)
                rateList2mysql(int(itemId), int(selllerId), tablename, logfile)
                #关闭日志文件
                printlog(u'Close log file.', u'OK', number, 0, logfile)
                logfile.close()
                #删除前一个的前一个商品的日志文件，避免最后日志文件过大
                try:
                    os.remove(d+'/{0}rateListLog.txt'.format(number-2))
                except OSError:
                    pass	#万一删除失败了也不再纠结于此
                #break

            #关闭数据库连接及文件等收尾工作
            number = 0
            db.close()
            itemIdfile.close()
            sellerfile.close()

            #发送程序运行结束的邮件
            subject = tablename
            nowtime = strftime("%Y-%m-%d,%H:%M:%S", localtime())
            body = "<h2>OK!</h2><p>{0}</p>".format(nowtime)
            send163mail(subject, body, receiver)

        #若程序意外终端则给管理员发送邮件
        except Exception, e:
            errorstr = traceback.format_exc()
            print(errorstr)
            subject = tablename
            nowtime = strftime("%Y-%m-%d,%H:%M:%S", localtime())
            body = "<h2>Unexpeccted halt!</h2><pre>{0}</pre><p>{1}</p>".format(errorstr, nowtime)
            send163mail(subject, body, receiver)
        #每抓完一类商品都暂停5秒
        time.sleep(5)

'''
创建数据库时就设置好字符编码，防止中文乱码
CREATE DATABASE test DEFAULT charACTER SET utf8 COLLATE utf8_general_ci;
'''
