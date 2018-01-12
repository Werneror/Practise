#!/usr/bin/python
# ^_^ coding:utf8 ^_^
import time
import requests

page = 1
count = 32
uid = "2656274875"
album_id = "3555383218964139"

cookies = dict(
	login_sid_t="xxxxxx",
	cross_origin_proto="SSL",
	SUB="xxxxxx",
	SUBP="xxxxxx",
	SUHB="xxxxxx",
	ALF="xxxxxx",
	SSOLoginState="xxxxxx",
	wvr="xxxxxx",
	WBStorage="xxxxxx"
)

headers = {
    'Host': 'photo.weibo.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://www.baidu.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
}

f = open('photo_urls.txt', 'w')
number = 0

while True:
	r = requests.get('http://photo.weibo.com/photos/get_all?uid='+uid+'&album_id='+album_id+'&count='+str(count)+'&page='+str(page)+'&type=3', cookies=cookies, headers=headers)
	if r.json()['result'] == True:
		total = r.json()['data']['total']
		photo_list = r.json()['data']['photo_list']
		list_len = len(photo_list)
		print("INFO: photo_list's length is "+str(list_len))
		if list_len < 3:
			print(u'INFO: sleep 120s .. ')
			time.sleep(120)
		for photo in photo_list:
			photo_url = photo['pic_host']+'/mw690/'+photo['pic_name']
			f.write(photo_url+'\n')
			number += 1
	else:
		print(u'ERROR: get fail')
		break
	if number >= total:
		break
	else:
		print(u'INFO: finish page ' + str(page))
		page = page + 1
	time.sleep(30)
f.close()
print(u'SUCCESS: finish')