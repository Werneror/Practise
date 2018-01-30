# ^-^ coding:utf-8 ^-^
import sys
import numpy as np
import cPickle as pickle
import sklearn.metrics as sm
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures

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
#为了绘图时能够显示曲线，需要排序
Train = np.column_stack((X_train,y_train))
Train.sort(axis=0)
X_train = np.array(Train[:,0]).reshape((num_training, 1))
y_train = np.array(Train[:,1])

X_test = np.array(X[num_training:]).reshape((num_test, 1))
y_test = np.array(y[num_training:])
#为了绘图时能够显示曲线，需要排序
Test = np.column_stack((X_test,y_test))
Test.sort(axis=0)
X_test = np.array(Test[:,0]).reshape((num_test, 1))
y_test = np.array(Test[:,1])

# 将特征预处理为多项式形式
polynomial = PolynomialFeatures(degree=3)
X_train_transformed = polynomial.fit_transform(X_train)
X_test_transformed = polynomial.fit_transform(X_test)

# 创建线性回归对象
linear_regressor = linear_model.LinearRegression()
polynomial_regressor = linear_model.LinearRegression()

# 用训练数据集训练模型
linear_regressor.fit(X_train, y_train)
polynomial_regressor.fit(X_train_transformed, y_train)

# 显示对训练数据集的拟合情况
y_train_pred_linear = linear_regressor.predict(X_train)
y_train_pred_poly = polynomial_regressor.predict(X_train_transformed)

plt.figure()
plt.scatter(X_train, y_train, color='green')
plt.plot(X_train, y_train_pred_linear, color='black', linewidth=4)
plt.plot(X_train, y_train_pred_poly, color='red', linewidth=4)
plt.title(u"Training data")

# 显示对测试数据集的拟合情况
y_test_pred_linear = linear_regressor.predict(X_test)
y_test_pred_poly = polynomial_regressor.predict(X_test_transformed)

plt.figure()
plt.scatter(X_test, y_test, color='green')
plt.plot(X_test, y_test_pred_linear, color='black', linewidth=4)
plt.plot(X_test, y_test_pred_poly, color='red', linewidth=4)
plt.title(u"Test data")

# 结果评价
print(u"回归算法\t多项式回归\t线性回归")
print(u"平均绝对误差\t{0:.8f}\t{1:.8f}".format(sm.mean_absolute_error(y_test, y_test_pred_poly), sm.mean_absolute_error(y_test, y_test_pred_linear)))
print(u"均方误差\t{0:.8f}\t{1:.8f}".format(sm.mean_squared_error(y_test, y_test_pred_poly), sm.mean_squared_error(y_test, y_test_pred_linear)))
print(u"解释方差分\t{0:.8f}\t{1:.8f}".format(sm.explained_variance_score(y_test, y_test_pred_poly), sm.explained_variance_score(y_test, y_test_pred_linear)))
print(u"R2方差分\t{0:.8f}\t{1:.8f}".format(sm.r2_score(y_test, y_test_pred_poly), sm.r2_score(y_test, y_test_pred_linear)))

plt.show()