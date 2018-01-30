# ^-^ coding:utf-8 ^-^
import sys
import numpy as np
import sklearn.metrics as sm
from sklearn import linear_model

# 载入数据
filename = "data_multivar.txt"
X = []
y = []
with open(filename, 'r') as f:
	for line in f.readlines():
		temp = [float(i) for i in line.split(',')] 
		xt, yt = temp[:-1], temp[-1]
		X.append(xt)
		y.append(yt)

# 把数据分成训练数据集和测试数据集
num_training = int(0.8*len(X))
num_test = len(X) - num_training

X_train = np.array(X[:num_training])
y_train = np.array(y[:num_training])

X_test = np.array(X[num_training:])
y_test = np.array(y[num_training:])

# 创建岭回归对象
ridge_regressor = linear_model.Ridge(alpha=0.01, fit_intercept=True, max_iter=10000)

# 用训练数据集训练模型
ridge_regressor.fit(X_train, y_train)
y_test_pred = ridge_regressor.predict(X_test)

# 结果评价
print(u"岭回归：")
print(u"平均绝对误差\t{}".format(round(sm.mean_absolute_error(y_test, y_test_pred), 8)))
print(u"均方误差\t{}".format(round(sm.mean_squared_error(y_test, y_test_pred), 8)))
print(u"解释方差分\t{}".format(round(sm.explained_variance_score(y_test, y_test_pred), 8)))
print(u"R2方差分\t{}".format(round(sm.r2_score(y_test, y_test_pred), 8)))

## 对比
print(u"")

# 创建线性回归对象
linear_regressor = linear_model.LinearRegression()
# 用训练数据集训练模型
linear_regressor.fit(X_train, y_train)
y_test_pred = linear_regressor.predict(X_test)
# 结果评价
print(u"线性回归：")
print(u"平均绝对误差\t{}".format(round(sm.mean_absolute_error(y_test, y_test_pred), 8)))
print(u"均方误差\t{}".format(round(sm.mean_squared_error(y_test, y_test_pred), 8)))
print(u"解释方差分\t{}".format(round(sm.explained_variance_score(y_test, y_test_pred), 8)))
print(u"R2方差分\t{}".format(round(sm.r2_score(y_test, y_test_pred), 8)))
