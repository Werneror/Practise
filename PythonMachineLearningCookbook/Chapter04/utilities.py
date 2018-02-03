# ^_^ coding:utf-8 ^_^

import time
import requests
import numpy as np
import matplotlib.pyplot as plt
from sklearn import cross_validation

# 加载回归数据
def load_data(input_file):
    X = []
    with open(input_file, 'r') as f:
        for line in f.readlines():
            data = [float(x) for x in line.split(',')]
            X.append(data)

    return np.array(X)

# 雅虎财经数据接口
def  quotes_yahoo(ticker, begin, end):
    cookies = dict(B='79bclatd788ib&b=3&s=vt')
    crumb = 'x.eNt0GsePI'
    period1 = int(time.mktime(begin.timetuple()))
    period2 = int(time.mktime(end.timetuple()))
    url = '''https://query1.finance.yahoo.com/v7/finance/download/{0}?period1={1}&period2={2}&interval=1d&events=history&crumb={3}'''
    s = requests.Session()
    r = s.get(url.format(ticker, period1, period2, crumb), cookies=cookies)
    if r.text.startswith('{"chart":{"result":null,"error"'):
        raise IOError(r.text)

    quote = {}
    lines = r.text.split('\n')
    items = [item.lower() for item in lines[0].split(',')]
    for item in items:
        quote[item] = []
    for line in lines[1:-1]:
        i = 0
        for data in line.split(','):
            data = data.replace("'", "")
            try:
                quote[items[i]].append(float(data))
            except:
                quote[items[i]].append(data)
            i+=1
    return quote