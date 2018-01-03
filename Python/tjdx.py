#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib,urllib2,sys,re,time,getopt,socket,os		
socket.setdefaulttimeout(60)	#设置超时为60秒
def downfiles(filelist):
	'''下载filelist中的所有文件'''
	for x in filelist:
		if naigetcode(x)==200:
			dirname = filename = re.findall(r'photo\/\d\d\d\d(\d\d\d)\d\d\d\.jpg',x)[0]
			makedir(dirname)
			filename = re.findall(r'photo\/(\d*\.jpg)',x)[0]
			print filename
			print 'Download ',x
			try:
				urllib.urlretrieve(x,dirname+'/'+filename,reporthook)
			except socket.timeout:
				print 'timeout!'
			else:
				pass
		else:
			print 'Not 200',x
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
def naigetcode(url):
	'''返回输入URL的响应HTTP状态码'''
	request = urllib2.Request(url, headers = {
	    'Connection': 'Keep-Alive',
	    'Accept': 'text/html, application/xhtml+xml, */*',
	    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
	    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
	})	#伪装为浏览器
	try:
		response = urllib2.urlopen(request)
		code = response.getcode()
	except urllib2.URLError, e:	#有些返回状态码会引发urllib2.URLError异常
    		return e.code
	except socket.timeout:	#若等待时间超过设定的超时时间，会引发socket.timeout异常，此时函数返回408
		return 408
	return code
def makedir(dirname):		#此函数用于创建文件夹
	if not os.path.exists(dirname) :		#判断文件夹是否存在
		os.mkdir(dirname)	#若不存在则新建文件夹
def main():
	filelist = []
	urlA = r'http://****.****.****.****/cetphoto/photo/'
	urlC = r'.jpg'
	for i in range(3014218070,3014218080):
		filelist.append(urlA + str(i) +urlC)
	downfiles(filelist)
version = '''tjdx	2015年11月20日'''
if __name__ == "__main__":
	main()

'''201,机械学院动力机械及工程
202,精仪学院
203,电气与自动化工程学院电力系统及其自动化专业
204,信息学院
205,建筑工程学院
206,建筑学院
207,化工学院化学工程专业
208,材料学院
209,管理与经济学部
210,理学院
211,文法学院
212,教育学院
213,药物科学与技术学院
214,环境科学与工程学院
216,计算机科学与技术学院
218,软件学院
226,生命科学学院
227,海洋科学与技术学院
'''
