# ^-^ coding:utf-8 ^-^
import sys
import numpy as np
import cPickle as pickle
import sklearn.metrics as sm
import matplotlib.pyplot as plt
from sklearn import linear_model

# 载入数据
filename = "data_singlevar.txt"
X = []
y = []
with open(filename, 'r') as f:
	for line in f.readlines():
		xt, yt = [float(i) for i in line.split(',')]
		X.append(xt)
		y.append(yt)

# 把数据分成训练数据集和测试数据集
num_training = int(0.8*len(X))
num_test = len(X) - num_training

X_train = np.array(X[:num_training]).reshape((num_training, 1))
y_train = np.array(y[:num_training])

X_test = np.array(X[num_training:]).reshape((num_test, 1))
y_test = np.array(y[num_training:])

# 创建线性回归对象
linear_regressor = linear_model.LinearRegression()

# 用训练数据集训练模型
linear_regressor.fit(X_train, y_train)

# 显示对训练数据集的拟合情况
y_train_pred = linear_regressor.predict(X_train)
plt.figure()
plt.scatter(X_train, y_train, color='green')
plt.plot(X_train, y_train_pred, color='black', linewidth=4)
plt.title(u"Training data")
plt.show()

# 显示对测试数据集的拟合情况
y_test_pred = linear_regressor.predict(X_test)
plt.figure()
plt.scatter(X_test, y_test, color='green')
plt.plot(X_test, y_test_pred, color='black', linewidth=4)
plt.title(u"Test data")
plt.show()

# 结果评价
print(u"平均绝对误差\t{}".format(round(sm.mean_absolute_error(y_test, y_test_pred), 2)))
print(u"均方误差\t{}".format(round(sm.mean_squared_error(y_test, y_test_pred), 2)))
print(u"解释方差分\t{}".format(round(sm.explained_variance_score(y_test, y_test_pred), 2)))
print(u"R2方差分\t{}".format(round(sm.r2_score(y_test, y_test_pred), 2)))

# 保存模型数据
output_model_file = 'saved_modle.pk1'
with open(output_model_file, 'w') as f:
	pickle.dump(linear_regressor, f)

'''
# 打开并使用保存的模型
output_model_file = 'saved_modle.pk1'
with open(output_model_file, 'r') as f:
	model_linregr = pickle.load(f)
y_test_pred_new = model_linregr.predict(X_test)
print("\n")
print(u"新平均绝对误差\t{}".format(round(sm.mean_absolute_error(y_test, y_test_pred_new), 2)))
'''