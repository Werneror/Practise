# ^_^ coding:utf-8 ^_^

import numpy as np 
import matplotlib.pyplot as plt 
from sklearn import neighbors

# 生成样本数据
amplitude = 10
num_points = 100
X = amplitude*np.random.rand(num_points, 1) - 0.5*amplitude

# 计算目标并添加噪声
y = np.sinc(X).ravel()
y += 0.2*(0.5 - np.random.rand(y.size))

# 画出输入数据
plt.figure()
plt.scatter(X, y, s=40, c='k', facecolors='none')
plt.title('Input data')
plt.show()

# 用输入数据10倍的密度创建一维网格
x_values = np.linspace(-0.5*amplitude, 0.5*amplitude, 10*num_points)[:, np.newaxis]

# 定义最近邻的个数
n_neighbors = 8

# 定义并训练回归器
knn_regressor = neighbors.KNeighborsRegressor(n_neighbors, weights='distance')
y_values = knn_regressor.fit(X, y).predict(x_values)

# 画出预测值
plt.figure()
plt.scatter(X, y, s=40, c='k', facecolors='none', label='input data')
plt.plot(x_values, y_values, c='k', linestyle='--', label='predicted values')
plt.xlim(X.min()-1, X.max()+1)
plt.ylim(y.min()-1, y.max()+1)
plt.legend()
plt.title('K Nearest Neighbors Regressor')
plt.show()