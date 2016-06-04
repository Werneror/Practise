#/usr/bin/env python
#coding=utf8
import httplib
import md5
import urllib
import random
import re
import time
def translate(q, fromLang, toLang):
    '''本函数使用百度翻译API进行翻译，q是待翻译的词，fromLang是源语言，toLang是目标语言'''
    '''详情参见：http://api.fanyi.baidu.com/api/trans/product/apidoc'''
    appid = '20151113000005349'
    secretKey = 'osubCEzlGjzvw8qdQc41'

    httpClient = None
    myurl = '/api/trans/vip/translate'
    salt = random.randint(32768, 65536)

    sign = appid+q+str(salt)+secretKey
    m1 = md5.new()
    m1.update(sign)
    sign = m1.hexdigest()
    myurl = myurl+'?appid='+appid+'&q='+urllib.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign

    try:
        httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        #response是HTTPResponse对象
        response = httpClient.getresponse()
        s = response.read()
        dst = re.findall(r'"dst":"(.*)"', s)[0]
        return dst
    except Exception, e:
        return Null
    finally:
        if httpClient:
            httpClient.close()
#END OF translate

if __name__ == '__main__':
    print(translate('中国', 'zh', 'en').decode("unicode_escape").encode("UTF-8"))
