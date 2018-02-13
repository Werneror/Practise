# ^_^ coding:utf-8 ^_^
# 题目：http://ctf5.shiyanbar.com/jia/index.php

import requests

base_url = "http://ctf5.shiyanbar.com/jia/index.php"
str_1 = "<div name='my_expr'>"
str_2 = "</div>=?"

session = requests.session()
r = session.get(base_url)
start = r.text.index(str_1) + len(str_1)
end = r.text.index(str_2)
expr = r.text[start:end].replace('x', '*')
data = {'pass_key': eval(expr)}
r = session.post(base_url + "?action=check_pass", data=data)
print(r.text)
