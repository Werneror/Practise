#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib,urllib2,sys,re,time,getopt,socket		
socket.setdefaulttimeout(60)	#设置超时为60秒
def gethtml(url):
	'''返回输入url对应的HTML页面'''
	request = urllib2.Request(url, headers = {
	    'Connection': 'Keep-Alive',
	    'Accept': 'text/html, application/xhtml+xml, */*',
	    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
	    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
	})
	response = urllib2.urlopen(request)
	html = response.read()
	return html
def getallurl(html):	
	'''返回输入url对应的HTML页面'''
	allurl = re.findall(r'href\s*=\s*"([\s\S].*?)"',html) + re.findall(r'src\s*=\s*"([\s\S].*?)"',html) + \
	 re.findall(r'url\s*\(\s*"([\s\S].*?)"\)',html)
	return set(allurl)
def re2ab(urllist,url):
	'''返回输入url对应的HTML页面'''
	relist = []
	for x in urllist :
		if 'http' in x :
			pass
		else :
			spam = r'/'
			if x.startswith(r'/') :
				 spam = ''
			x = url + spam + x
		relist.append(x)
	return relist
def urlinweb(urllist,url):
	'''筛选出站内链接'''
	relist = []
	for x in urllist :
		if url in x:
			relist.append(x)
	return relist
def checkurl(urllist):
	'''排除非网页链接'''
	relist = []
	for x in urllist :
		if ('.js' in x or '.css' in x or '.gif' in x or '.png' in x or 'javascript:' in x or  'javaScript:' in x or
		'.jpg' in x or 'mailto:' in x or '.pdf' in x or '.xls' in x or '.doc' in x) :
			pass
		else :
			relist.append(x)
	return relist
def checjing(urllist):
	'''排除链接后的#和/'''
	relist = []
	for x in urllist :
		if x.endswith(r'#'):
			x = x[:-1]
		if x.endswith(r'/'):
			x = x[:-1]
		relist.append(x)
	return relist
def searchextension(urllist,extensionlist):
	'''筛选出含特定后缀名的URL'''
	relist = []
	for x in urllist :
		for y in extensionlist :
			if x.endswith(y):
				relist.append(x)
				break
	return relist
def dealextension(A):
	'''将字符串形式的的后缀名参数转换为列表，含“.”'''
	extensionlist = A.split('.')
	if extensionlist[0] == '':
		extensionlist = extensionlist[1:]
	extensionlist = ['.'+x for x in extensionlist]
	return extensionlist
def downfiles(filelist,logfile,n):
	'''下载filelist中的所有文件'''
	for x in filelist:
		filename = 'Unknown'
		if re.findall(r'/([^/]+)$',x):
			filename = re.findall(r'/([^/]+)$',x)[-1]
		try:
			print 'Donwloading:['+str(n)+']'+filename+' form '+ x
			print>>logfile,'Donwloading:['+str(n)+']'+filename+' form '+ x
			urllib.urlretrieve(x,'['+str(n)+']'+filename,reporthook)
		except:
			print 'Donwload false.'
			print>>logfile,'Donwload false.'
		else:
			print 'Donwload complete.'
			n += 1		#下载成功则给n加1
			print>>logfile,'Donwload complete.'
	return n
def reporthook(block_read,block_size,total_size):
	'''回调函数，block_size是每次读取的数据块的大小，block_read是每次读取的数据块个数，taotal_size是一一共读取的数据量，单位是byte
注：当服务器没有返回content-length首部时，urlretrieve不知道数据有多大，为total_size传入-1。'''
	if not block_read:
		print "connection opened"
		return
	if total_size<0:
		#unknown size
		print "read %d blocks (%dbytes)" %(block_read,block_read*block_size)
	else:
		amount_read=block_read*block_size
		print 'Read %d blocks,or %d/%d' %(block_read,block_read*block_size,total_size)
	return
def run(fatherurl,extensionlist):
	urlpoor = [fatherurl]	#初始化URL池
	oldurl = []	#初始化oldURL
	oldfile = []		#下载过的文件的列表
	logfile = open('downlog.txt','w')	#打开存储下载日志的文件
	n = 0		#统计下载成功文件总数
	while urlpoor:
		url = urlpoor[0]
		urlpoor = urlpoor[1:]	#删除urlpoor中的第一个元素
		oldurl.append(url)	#向oldurl中添加即将处理的URL
		try:
			print 'Opening:',url
			html = gethtml(url)	#打开网页
		except:
			print 'Opened false.'
		else:
			urllist =  getallurl(html)	#获得该网页中所有URL
			urllist =  re2ab(urllist,url)	#将相对路径转换为绝对路径
			#处理文件链接
			filelist = searchextension(urllist,extensionlist)	#获得下载文件列表
			filelist = [i for i in filelist if i not in oldfile] 	#筛选出未下载过的文件链接
			n = downfiles(filelist,logfile,n)	#下载文件
			oldfile += filelist	#将下载过的URL加入到oldfile列表中
			#处理网页链接
			urllist = checjing(urllist)	#排除链接后的#和/
			urllist = [i for i in urllist if i not in filelist]	#筛选出非已下载文件链接
			urllist = checkurl(urllist)	#排除非网页链接
			urllist = urlinweb(urllist,fatherurl)	#筛选出站内链接
			urllist = [i for i in urllist if i not in oldurl]	#筛选出没打开过的链接
			urllist = [i for i in urllist if i not in urlpoor] 	#去重
			urlpoor += urllist	#将有效url添加到urlpoor中
	return n
def main():
	if len(sys.argv) == 1:
		print u'添加“-h”查看帮助'
	else:
		extensionlist = []	#用于存储后缀名的列表
		fatherurl = ''	#用于存储最初的URL
		opts, args = getopt.getopt(sys.argv[1:], "hvw:A:")
		for op, value in opts:
			if op == '-h' :
				print helptxt
			elif op == '-v' :
				print version
			elif op == '-w' :
				fatherurl = value
			elif op == '-A' :
				extensionlist = dealextension(value)
		if extensionlist != [] and fatherurl != '':
			start = time.time()		#计时开始
			print 'The program starts running, please wait...'
			n = run(fatherurl,extensionlist)
			print 'A total of %d files are downloaded. The program is runing over %.2f s.' % (n,time.time()-start)	#打印程序运行时间
helptxt = u'''
-h	查看帮助
-v	查看版本信息
-w	指定目标网站，应该是完整的URL地址
-A	指定目标文件后缀名，需含“.”,若有多个，则连在一起写，不用加空格
'''
version = '''getall0.1	2015年10月2日'''
if __name__ == "__main__":
	main()
