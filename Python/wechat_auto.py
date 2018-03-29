# coding:utf-8

import re
import json
import time
import random
import itchat
import logging
import requests
from itchat.content import *

import sys
reload(sys)
sys.setdefaultencoding("utf8")

config = u"""
{
    "my_user_name": "",
	"period": [
        {
			"start": "22-30-00",
			"end": "24-00-00",
			"reason": "我已经睡觉了",
			"reply": "明早回复您"
		},
		{
			"start": "00-00-00",
			"end": "06-00-00",
			"reason": "我还在睡觉",
			"reply": "早上起来回复您"
		},
		{
			"start": "08-00-00",
			"end": "21-20-00",
			"reason": "我在自习，没有带手机",
			"reply": "晚上回到宿舍再回复您"
		}
	],
	"interlocution": [
        {
			"question": "为什么要设置自动回复？",
			"answer": "这是程序员的乐趣:)"
		},
		{
			"question": "这个自动回复是怎么实现的？",
			"answer": "用Python的itchat库实现的，该库调用的是网页版微信接口。"
		},
		{
			"question": "可以帮我做个自动回复吗？",
			"answer": "不可以。如果你是程序员，就应该自己动手。如果你不是程序员，我帮你写好了你也不会运行呀。"
		},
		{
			"question": "可以让我看看这个自动回复的源代码吗？",
			"answer": "可以，代码在这里：https://github.com/werner-wiki/Practise/blob/master/Python/wechat_auto.py"
		},
        {
            "question": "你自习为何不带手机呢？不怕错过什么重要的消息吗？",
            "answer": "自习为何要带手机呢？根据以往的经验，不带手机不会错过任何重要的消息。"
        },
        {
            "question": "你一般在哪自习？",
            "answer": "一般在主图2338自习，若确有急事可以在这里找到我。"
        },
        {
            "question": "自动回复还有什么功能？",
            "answer": "回复你的名字可以返回包含你的名字的一句古诗词（如果存在这样的古诗词），这一功能调用以诗之名(poem.werner.wiki)的接口实现；回复任意内容可和图灵机器人聊天。"
        }
	],
	"direct": [
        {
			"request": "在吗",
			"response": "不在"
		},
		{
			"request": "在吗?",
			"response": "不在。"
		},
		{
			"request": "在吗？",
			"response": "不在！"
		}
	]
}
"""
assess = {}
logging.basicConfig(level=logging.INFO,
                    filename='wechat.log',
                    filemode='a',
                    format='[%(asctime)s] - %(message)s')

def get_time():
    return time.strftime("%H-%M-%S",time.localtime(time.time()))

def is_in_period(start_time, end_time):
    current = get_time()
    if current > start_time and current < end_time:
        return True
    else:
        return False

def is_first_access(msg):
    '''上次访问距现在是否在30min内'''
    ret = False
    if msg["FromUserName"] in assess.keys():
        if assess[msg["FromUserName"]] - time.time() > 30*60:
            ret = True
        assess[msg["FromUserName"]] = time.time()
    else:
        ret = True
        assess.update({msg["FromUserName"]: time.time()})
    return ret

def tuling(msg):
    API_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxx'
    raw_TULINURL = "http://www.tuling123.com/openapi/api?key=%s&info=" % API_KEY
    try:
        r = requests.get(raw_TULINURL+msg["Text"])
        ret = json.loads(r.text)['text']
    except:
        ret = ""
    return ret

def poem(msg):
    poem_api = "https://poem.werner.wiki/api/search.php?keyword={}"
    ret = ""
    if 1 < len(msg["Text"]) < 4:
        try:
            r = requests.get(poem_api.format(msg["Text"]))
            pjson = json.loads(r.text)
            if pjson["ret"] == 0 and pjson["total"] > 0:
                if pjson["total"] < 10:
                    upper = pjson["total"] - 1
                else:
                    upper = 9
                ret = pjson["result"][random.randint(0, upper)]["content"]
        except:
            pass
    return ret

def direct_response(msg):
    ret = ""
    for direct in config["direct"]:
        if direct["request"] == msg["Text"]:
            ret = direct["response"]
            break
    return ret

def question_answer(msg):
    if msg["Text"] == "？" or msg["Text"] == "?":
        ret = u"回复问题编号查看答案"
        for i, interlocution in enumerate(config["interlocution"]):
            ret += u"\n" + str(i) + u"." + interlocution["question"]
    else:
        ret = ""
        matchObj = re.match(r"(^\d{1,2}$)", msg["Text"], re.I)
        if matchObj:
            number = int(matchObj.group(1))
            if number < len(config["interlocution"]):
                ret = u"问：" + config["interlocution"][number]["question"]
                ret += u"\n答：" + config["interlocution"][number]["answer"]
                ret += u"\n（回复？查看更多）"
    return ret

@itchat.msg_register([TEXT])
def text_reply(msg):

    logging.info(u"[" + msg["FromUserName"] + u"] - " + msg["Text"])

    if msg["FromUserName"] == config["my_user_name"]:
        return

    ret = ""
    for period in config["period"]:
        if (is_in_period(period["start"], period["end"])):
            if is_first_access(msg):
                ret = u"{}，{}。".format(period["reason"], period["reply"])
                ret += u"\n（回复？查看更多功能）"
            else:
                ret = question_answer(msg)
                if ret == "":
                    ret = direct_response(msg)
                    if ret == "":
                        ret = poem(msg)
                        if ret == "":
                            ret = tuling(msg)
            if ret != "":
                ret = u"[自动回复]\n" + ret
                msg.user.send(ret)
                logging.info(u"[此乃自动回复] - " + ret)
            break

if __name__ == '__main__':
    itchat.auto_login(enableCmdQR=2, hotReload=True)
    config = json.loads(config)
    config["my_user_name"] = itchat.get_friends(update=True)[0]["UserName"]
    itchat.run()
