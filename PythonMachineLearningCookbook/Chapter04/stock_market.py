# ^_^ coding:utf-8 ^_^

import json
import datetime

import numpy as np 
import matplotlib.pyplot as plt 
from sklearn import covariance, cluster

from utilities import quotes_yahoo

# 输入符号信息文件
symbol_file = 'symbol_map.json'
with open(symbol_file, 'r') as f:
	symbol_dict = json.loads(f.read())

# 将字典数据转换成两个列表数据
symbols, names = np.array(list(symbol_dict.items())).T

# 选择时间段
start_date = datetime.datetime(2014, 4, 5)
end_date = datetime.datetime(2017, 6, 2)

# 读取输入的数据
quotes = [quotes_yahoo(symbol, start_date, end_date) for symbol in symbols]

# 提取开盘价和收盘价
opening_quotes = np.array([quote['open'] for quote in quotes]).astype(np.float)
closing_quotes = np.array([quote['close'] for quote in quotes]).astype(np.float)

# 计算每日股价波动
delta_quotes = closing_quotes - opening_quotes

# 从相关性中建立协方差图模型
edge_model = covariance.GraphLassoCV()

# 数据标准化
X = delta_quotes.copy().T
X /= X.std(axis=0)

# 训练模型
with np.errstate(invalid='ignore'):
	edge_model.fit(X)

# 用临近传播算法建立聚类模型
_, labels = cluster.affinity_propagation(edge_model.covariance_)
num_labels = labels.max()

# 打印聚类结果
for i in range(num_labels + 1):
	print(u"类别{} --> {}".format(i, ', '.join(names[labels==i])))