# -*- coding: utf-8 -*-
# 让两个机器人聊天，图灵机器人和青云客智能聊天机器人
import sys
import json
import time
import requests

reload(sys) 
sys.setdefaultencoding('utf-8') 
API_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
raw_TULINURL = "http://www.tuling123.com/openapi/api?key=%s&info=" % API_KEY

raw_QINGYUNKE = "http://api.qingyunke.com/api.php?key=free&appid=0&msg="

def tuling(queryStr):
    '''图灵机器人'''
    r = requests.get(raw_TULINURL+queryStr)
    hjson=json.loads(r.text)
    length=len(hjson.keys())
    content=hjson['text']
    if length==3:
        return content+hjson['url']
    elif length==2:
        return content

def qingyunke(queryStr):
    '''青云客智能聊天机器人'''
    r = requests.get(raw_QINGYUNKE+queryStr)
    try:
        hjson=json.loads(r.text)
    except:
        return u'呃，我处了点毛病...'
    try:
        content=hjson['content']
    except:
        content=u'你说什么，我听不懂'
    return content

#发起会话
print u'青： 你叫什么名字？'
s1 = tuling(u'你叫什么名字？')
print u'图：',s1

#接着由两个机器人自己聊
while True:
    time.sleep(5)
    s2 = qingyunke(s1)
    print u'青：',s2
    time.sleep(5)
    s1 = tuling(s2)
    print u'图：',s1
