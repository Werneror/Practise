# -*- coding: utf-8 -*-
import sys
import json
import time
import itchat
import requests
reload(sys) 
sys.setdefaultencoding('utf-8') 
API_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
raw_TULINURL = "http://www.tuling123.com/openapi/api?key=%s&info=" % API_KEY
def result(queryStr):
    r = requests.get(raw_TULINURL+queryStr)
    hjson=json.loads(r.text)
    length=len(hjson.keys())
    content=hjson['text']
    if length==3:
        return content+hjson['url']
    elif length==2:
        return content
@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    print msg['FromUserName']+u"："+msg['Text']
    time.sleep(5)
    ret = result(msg['Text'])
    print u"我："+ret
    return ret
itchat.auto_login()
itchat.run()
