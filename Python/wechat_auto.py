# coding:utf-8

import time
import itchat
from itchat.content import *

import sys  
reload(sys)  
sys.setdefaultencoding('utf8')   

def lc():
    print('login success')

def ec():
    print('logout success')

def get_time():
    return time.strftime('%H-%M-%S',time.localtime(time.time()))

def is_sleeping(start_time='22-30-00', end_time='06-30-00'):
    current = get_time()
    if current > start_time or current < end_time:
        # 因为开始时间是前一天晚上，结束时间是后一天早上
        return True
    else:
        return False

def is_outing(start_time='07-30-00', end_time='21-30-00'):
    current = get_time()
    if current > start_time and current < end_time:
        return True
    else:
        return False

@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    if is_sleeping():
        test = u"[自动回复]我已经睡觉了，明早回复您:)"
        msg.user.send(test)
    elif is_outing:
        test = u"[自动回复]我在自习，没有带手机，暂时无法回复您。大概会在晚上21:30回复您。若有事可考虑给我发邮件（me@werner.wiki），我可能会看到。"
        msg.user.send(test)
    else:
        #其他时间手动回复
        pass

itchat.auto_login(enableCmdQR=2, hotReload=True, loginCallback=lc, exitCallback=ec)
itchat.send('login success', toUserName='filehelper')
itchat.run(True)
