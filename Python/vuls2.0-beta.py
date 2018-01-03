# -*- coding: utf-8 -*-
import urllib2,sys,re,csv,os,time,getopt
exp3 = r'before\s[\d\.xX]+[-\w]*(?=\s|\,)|and\s[\d\.xX]+[-\w]*(?=\s|\,)|through\s[\d\.xX]+[-\w]*(?=\s|\,)|from\s[\d\.xX]+[-\w]*(?=\s|\,)|to\s[\d\.xX]+[-\w]*(?=\s|\,)|(?<=\s)\d+\.[\d\.xX\w-]*(?=\s|\,)|and earlier'
#正则表达式exp3用于匹配有漏洞软件版本号
exp4 = r'[\w_][\w_\\\/]+\.c(?=\s)|[\w_][\w_\\\/]+\.h(?=\s)|[\w_][\w_\\\/]+\.S(?=\s)|[\w_][\w_\\\/]+\.py(?=\s)'
#正则表达式exp4用于匹配漏洞所在文件名
exp5 = r'\w+[_\.]*[\w]+(?=\s+function)|\w+[_\.]*[\w]+\sand\s\w+[_\.]*[\w]+(?=\s+function)|\w+[_\.]*[\w]+\sor\s\w+[_\.]*[\w]+(?=\s+function)'
#正则表达式exp5匹配漏洞函数名，认为函数名一定在function前
def openweb(url):		#此函数返回输入的url对应的页面
	request = urllib2.Request(url)
	response = urllib2.urlopen(request,timeout=100)		#设置请求超时时间为100秒
	html = response.read()
	return html
def makedir(dirname):		#此函数用于创建文件夹
	if not os.path.exists(dirname) :		#判断文件夹是否存在
		os.mkdir(dirname)	#若不存在则新建文件夹
def getdetail(softwarename):		#此函数获得某软件所有指向漏洞细节的链接将其存储到urldetail中并返回urldetail
	index = 0		#标记翻页的量
	urldetail = []		#存储指向漏洞细节链接的列表
	while True :
		#打开某软件漏洞搜索结果主页
		url = 'https://web.nvd.nist.gov/view/vuln/search-results?adv_search=true&cves=on&cpe_product=cpe:/::'
		url += softwarename
		url += '&startIndex=' + str(index)
		try:
			html = openweb(url)
		except :		#处理错误
			print 'Failed to open the web!'
			break
		else:
			#正则匹配得到该网页中指向漏洞细节的链接，存储到列表urldetail中
			for detail in re.findall('detail\?vulnId=CVE-\d*-\d*', html) :
				urldetail.append('https://web.nvd.nist.gov/view/vuln/' + detail)
			print 'Finding vulnerabilities:' + str(len(urldetail))		#输出已获得的漏洞的个数
			#是否翻页的判断，利用页面是否出现“>>”，即翻页符
			if re.search('&gt;&gt;', html) :
				index += 20
			else :
				print ''		#输出一个空行
				break
	return urldetail
def getdata(urldetail,softwarename) :		#此函数遍历列表urldetail中所有链接，逐一打开页面，并将获得的数据存储到文件中
	csvfile = open(softwarename + '.csv','wb')		#打开存储漏洞信息的csv文件
	txtfile = open(softwarename + '_Overview.txt','w')		#打开存储overview信息的txt文件
	spamwriter = csv.writer(csvfile,dialect='excel')
	spamwriter.writerow(['CVE ID', 'CWE ID', 'Software name', 'Software version', 'File name','Function name','Links to patch'])
	i = 0		#统计处理漏洞的个数
	for detail in urldetail :
		i += 1
		print '[' + str(i) + '/'+ str(len(urldetail)) + ']Dealing:',detail
		try:
			html = openweb(detail)
		except :		#处理错误
			a = re.findall(r'CVE-\d*-\d*',detail) 
			if  a:		#加if判断的目的是防止匹配不到时进行[0]运算会使程序出错中止
				spamwriter.writerow([a[0],'Failed to open the web!'])	#输出错误提示到文件
				txtfile.write(str(a[0]) + '\n')
				print a[0] + ':Failed to open the web!'		#输出错误提示到屏幕
			else :
				spamwriter.writerow(['Unknown Error!'])	#输出错误提示到文件
				print 'Unknown Error!'		#输出错误提示到屏幕
		else:
			vul = Analysis(detail,html,softwarename)
			spamwriter.writerow(vul[0:7])		#将取得的数据输出到csv文件
			txtfile.write(str(vul[0]) + '\t' + str(vul[7]) + '\n')		#将overview信息输出到txt文件
			print vul	#将取得的数据同时输出到屏幕
			print ''		#输出一个空行
	csvfile.close()		#关闭表格文件
	txtfile.close()		#关闭文本文件
def Analysis(url,html,softwarename) :		#此函数取得网址和网页中所需数据，并返回
	p = ['Unknown','Unknown','Unknown','Unknown','Unknown','Unknown','Unknown','Unknown']		#暂存漏洞信息的列表
	a = re.findall(r'CVE-\d+-\d+',url)
	if  a:
		p[0] = a[0]		#从URL中匹配CVE ID
	a = re.findall(r'CWE-\d+',html)
	if  a:
		p[1] = a[0]			#匹配CWE ID
	p[2] = softwarename		#从命令行参数直接获得软件名
	a = re.findall(r'<h4>Overview</h4>\s+<p>([\s\S].*?)</p>',html)
	if  a:	#从html中匹配Overview
		overview = a[0]
		b= re.findall(exp3,overview)
		if b:
			p[3] = ' '.join(b)		#匹配有漏洞软件版本号
		b = re.findall(exp4,overview)
		if b:
			p[4] = b[0]		#匹配漏洞文件名
		b = re.findall(exp5,overview)
		if b:		#匹配漏洞函数名
			p[5] = b[0]
			if p[5] == 'the' or p[5] == 'for' or p[5] == 'other' :		#过滤错误的函数名
				p[5] = 'Unknown'
		p[7] = overview		#将Overview的内容全部输出以便于人工核查
	else :
		p[3] = 'Not found Overview!'
		p[4] = p[5] = p[6] = ''
	diffurls = getreferences(html)
	diff = getdiff(softwarename,p[0],diffurls)
	if diff != '' :
		p[6] = diff
	return p
def getreferences(html):		#此函数用于从html中得到可能指向diff文件的diffurls，即NVD网站“References to Advisories, Solutions, and Tools”中的超链接，返回值是列表，只负责http页面，忽略ftp等
	exp = r'<span\s*class="label">Hyperlink:</span>\s*<a\s*href="(http[\s\S].*?)"'
	return re.findall(exp,html)
def getdiff(softwarename,cveid,diffurls):		#此函数用于从diffurls列表中寻找diff文件，并将找到的diff文件输出到以cveid命名的txt文件中，返回存在diff文件的url，若存在多个url中含有diff文件，则返回以逗号隔开的多个url，相应的txt文件会在cveid后加数字以区分
	makedir(softwarename)		#创建以软件名命名的文件夹
	diurl = []
	i = 0
	for refer in diffurls:
		print '\tSearching diff file in:',refer
		try:
			html = openweb(refer)
		except :		#处理错误
			print '\tFailed to open it.'
		else:
			diff = hasdiff(html,refer)	#判断html中是否存在diff文件
			if diff :	#若存在diff则写入到文件
				if i == 0:		#找到的第一个diff直接写入cveid文件
					file = open(softwarename + r'/' + cveid + r'.txt','w')
				else:		#再找到的diff需写入有“_数字”的文件
					file = open(softwarename + r'/' + cveid + r'_' + str(i) + r'.txt','w')
				file.write(diff)
				file.close()
				diurl.append(refer)	#将存在diff文件的超链接添加至列表diurl
				print '\tFound!'
				i += 1
			else :
				print '\tNot found.'
	return ','.join(diurl)	#将列表diurl转换为字符串
def hasdiff(html,refer):		#此函数用于从html中判断是否存在diff文件，若存在，以字符串形式返回该文件，不存在返回False
	dr = re.compile(r'<[^>]+>',re.S)
	nohtml = dr.sub('',html)			#去掉HTML标签
	if re.findall('@@[\s,\+\-\d]*@@',nohtml) :	
		diff = ''
		if 'html' in html :		#判断是否是html文件
			a = re.findall('<pre[\s\S]*?>[\s\S]*@@[\s,\+\-\d]*@@[\s\S]*</pre>',html)
			if a:
				diff = '\n\n'.join(a)		#有多个则用两个空行隔开
				diff = dr.sub('',diff)		#去掉HTML标签
				return diff
			else :
				return 'The program failed to match. Please finish it by yourself.\nReference:' + refer
		else :		#匹配.path、.txt等文件
			 return html
	else:
		return False
def dealurl(urldetail,startcve,endcve):		#此函数用于筛选出用户选择的漏洞的URL，返回一个含URLs的列表
	startindex = -1
	endindex = -1
	if startcve != '' and endcve == '' :
		try :
			startindex = urldetail.index(startcve)
		except :
			print 'Ignore start CVE ID.'
			return urldetail
		else:
			return urldetail[startindex:]
	if endcve != ''  and startcve == '' :
		try :
			endindex = urldetail.index(endcve)
		except :
			print  'Ignore end CVE ID.'
			return urldetail
		else:
			return urldetail[:endindex+1]
	if endcve != ''  and startcve != '' :
		try :
			startindex = urldetail.index(startcve)
		except :
			print 'Ignore start CVE ID.'
		try :
			endindex = urldetail.index(endcve)
		except :
			print 'Ignore end CVE ID.'
		if startindex != -1 and endindex == -1 : 
			return urldetail[startindex:]
		elif  endindex != -1 and startindex == -1 : 
			return urldetail[:endindex+1]
		elif  endindex != -1 and startindex != -1 : 
			if startindex > endindex :		#如果开始值大于结束值，则将两数交换
				startindex,endindex = endindex,startindex
			return urldetail[startindex:endindex+1]
		else :
			return urldetail
	else :
		return urldetail
#使用说明和版本说明
help = u'''
	-h	查看使用说明
	-v	查看版本说明
	-n	输入目标软件名
	-s	选择开始的CVE ID（可选）
	-e	选择结束的CVE ID（可选）\n
*如：vuls2.0-beta.py -n firefox -s 2015-7327 -e 2015-4507\n
*是在告诉程序去搜寻关于firefox的漏洞，并整理从CVE-2015-7327开始，到CVE-2015-4507之间的漏洞，
*请务必注意先后顺序的判断！不同页中，页码小的在前，同一页中，靠上的较靠前。
*程序运行过程中会不时向屏幕打印一些提示信息，以表明程序正在正常运行。
*程序会将收集、整理的漏洞信息输出到“软件名.csv”文件。
*另外会将Overview信息输出到“软件名_Overview.txt”文件，以便于人工核查。
*同时程序会将收集的diff输出到以软件名命名的文件夹中。'''
version = u'''
这是全新的2.0-beta版，较上一版本：
\t增加了-s -e等参数，分别用于选择开始的CVE ID和结束的CVE ID；
\t修改了使用说明；
\t重写了程序主体部分；
\t修改了HTML文件的判断语句；
\t修改了匹配漏洞所在文件名的正则；
\t修改匹配不到diff文件时的输出；
\t修改程序运行时间的输出。'''
#程序主体
opts, args = getopt.getopt(sys.argv[1:], "hvn:s:e:")
startcve = ''	#开始的CVE ID，初始化为空字符串
endcve = ''		#结束的CVE ID，初始化为空字符串
if len(sys.argv) == 1 :
	print 'Please add an parameter -h.'
for op, value in opts:		#为了确保-s与-e执行过（如果有的话）
	if op == '-s' :
		if re.findall(r'\d\d\d\d-\d\d\d\d',value) :		#测试start CVE ID格式是否正确
			startcve = 'https://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-' + value
		else :
			print 'The start CVE ID is wrong!'
			break
	elif op == '-e' :
		if re.findall(r'\d\d\d\d-\d\d\d\d',value) :		#测试end CVE ID格式是否正确
			endcve = 'https://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-' + value
		else :
			print 'The end CVE ID is wrong!'
			break
for op, value in opts:
	if op == '-h' :
		print help
	elif op == '-v' :
		print version
	elif op == '-n' :
		softwarename = value
		start = time.time()		#计时开始
		print '\nThe program starts running, please wait...'		#输出第一个提示，以免用户不知道程序是否运行
		urldetail = getdetail(softwarename)		#获得指向漏洞细节的链接
		urldetail = dealurl(urldetail,startcve,endcve)		#对获得的链接进行筛选
		print 'In total:',len(urldetail)		#输出总共需要处理的漏洞的个数
		print ''		#输出一个空行
		if len(urldetail) > 0 :		#找到漏洞信息才执行，避免不必要地打开文件
			getdata(urldetail,softwarename)		#获得漏洞信息
		print 'The program is runing over %.2f s.' % (time.time() - start)		#打印程序运行时间
################################################################################
# 版本vuls2.0-beat
# 这是基于python2.7.10完成的用于整理漏洞信息的数据采集程序
# 任何人可以不受任何限制地自由修改源码、分发程序
# 同时希望使用者及时反馈任何意见、建议和错误，以及共享修改后的源代码和程序
################################################################################
# 作者：田宇
# 联系：2073211851@qq.com
################################################################################