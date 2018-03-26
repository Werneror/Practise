#!/usr/bin/python
# ^_^ coding:utf8 ^_^

import re
import requests
import traceback
from urllib import quote
import sys, getopt
reload(sys)
sys.setdefaultencoding('utf-8')

class crawler:
    '''爬百度搜索结果的爬虫'''
    url = u''
    urls = []
    o_urls = []
    html = ''
    total_pages = 5
    current_page = 0
    next_page_url = ''
    timeout = 60                    #默认超时时间为60秒
    headersParameters = {    #发送HTTP请求时的HEAD信息，用于伪装为浏览器
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Mozilla/6.1 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }

    def __init__(self, keyword):
        self.url = u'https://www.baidu.com/baidu?wd='+quote(keyword)+'&tn=monline_dg&ie=utf-8'

    def set_timeout(self, time):
        '''设置超时时间，单位：秒'''
        try:
            self.timeout = int(time)
        except:
            pass

    def set_total_pages(self, num):
        '''设置总共要爬取的页数'''
        try:
            self.total_pages = int(num)
        except:
            pass

    def set_current_url(self, url):
        '''设置当前url'''
        self.url = url

    def switch_url(self):
        '''切换当前url为下一页的url
           若下一页为空，则退出程序'''
        if self.next_page_url == '':
            sys.exit()
        else:
            self.set_current_url(self.next_page_url)

    def is_finish(self):
        '''判断是否爬取完毕'''
        if self.current_page >= self.total_pages:
            return True
        else:
            return False

    def get_html(self):
        '''爬取当前url所指页面的内容，保存到html中'''
        r = requests.get(self.url ,timeout=self.timeout, headers=self.headersParameters)
        if r.status_code==200:
            self.html = r.text
            self.current_page += 1
        else:
            self.html = u''
            print '[ERROR]',self.url,u'get此url返回的http状态码不是200'

    def get_urls(self):
        '''从当前html中解析出搜索结果的url，保存到o_urls'''
        o_urls = re.findall('href\=\"(http\:\/\/www\.baidu\.com\/link\?url\=.*?)\" class\=\"c\-showurl\"', self.html)
        o_urls = list(set(o_urls))  #去重
        self.o_urls = o_urls
        #取下一页地址
        next = re.findall(' href\=\"(\/s\?wd\=[\w\d\%\&\=\_\-]*?)\" class\=\"n\"', self.html)
        if len(next) > 0:
            self.next_page_url = 'https://www.baidu.com'+next[-1]
        else:
            self.next_page_url = ''

    def get_real(self, o_url):
        '''获取重定向url指向的网址'''
        r = requests.get(o_url, allow_redirects = False)    #禁止自动跳转
        if r.status_code == 302:
            try:
                return r.headers['location']    #返回指向的地址
            except:
                pass
        return o_url    #返回源地址

    def transformation(self):
        '''读取当前o_urls中的链接重定向的网址，并保存到urls中'''
        self.urls = []
        for o_url in self.o_urls:
            self.urls.append(self.get_real(o_url))

    def print_urls(self):
        '''输出当前urls中的url'''
        for url in self.urls:
            print url

    def print_o_urls(self):
        '''输出当前o_urls中的url'''
        for url in self.o_urls:
            print url

    def run(self):
        while(not self.is_finish()):
            c.get_html()
            c.get_urls()
            c.transformation()
            c.print_urls()
            c.switch_url()

if __name__ == '__main__':
    help = 'baidu_crawler.py -k <keyword> [-t <timeout> -p <total pages>]'
    keyword = None
    timeout  = None
    totalpages = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hk:t:p:")
    except getopt.GetoptError:
        print(help)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(help)
            sys.exit()
        elif opt in ("-k", "--keyword"):
            keyword = arg
        elif opt in ("-t", "--timeout"):
            timeout = arg
        elif opt in ("-p", "--totalpages"):
            totalpages = arg
    if keyword == None:
        print(help)
        sys.exit()

    c = crawler(keyword)
    if timeout != None:
        c.set_timeout(timeout)
    if totalpages != None:
        c.set_total_pages(totalpages)
    c.run()
