# ^_^ coding:utf-8 ^_^

import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.cm as cm
from sklearn import neighbors, datasets

from utilities import load_data

# 加载输入数据
input_file = 'data_nn_classifier.txt'
data = load_data(input_file)
X, y = data[:, :-1], data[:, -1].astype(np.int)

# 画出输入数据
plt.figure()
plt.title('Input datapoints')
markers = '^sov<>hp'
mapper = np.array([markers[i] for i in y])
for i in range(X.shape[0]):
    plt.scatter(X[i,0], X[i,1], marker=mapper[i], s=50, edgecolors='black', facecolors='none')

# 设置最近邻个数
num_neighbors = 10

# 定义网格步长
h = 0.01

# 创建KNN分类器模型并进行训练
classifier = neighbors.KNeighborsClassifier(num_neighbors, weights='distance')
classifier.fit(X, y)

# 建立网格来画出边界
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
x_grid, y_grid = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

# 计算网格中所有点的输出
predicted_values  = classifier.predict(np.c_[x_grid.ravel(), y_grid.ravel()])

# 在图中画出计算结果
predicted_values = predicted_values.reshape(x_grid.shape)
plt.figure()
plt.pcolormesh(x_grid, y_grid, predicted_values, cmap=cm.Pastel1)

# 在图中画出训练数据点
for i in range(X.shape[0]):
    plt.scatter(X[i, 0], X[i, 1], marker=mapper[i], s=50, edgecolors='black', facecolors='none')
plt.xlim(x_grid.min(), x_grid.max())
plt.ylim(y_grid.min(), y_grid.max())
plt.title('k nearest neighbors classifier boundaries')

# 测试输入数据点
test_datapoint = [4.5, 3.6]
plt.figure()
plt.title('Test datapoint')
for i in range(X.shape[0]):
    plt.scatter(X[i, 0], X[i, 1], marker=mapper[i], s=50, edgecolors='black', facecolors='none')
plt.scatter(test_datapoint[0], test_datapoint[1], marker='x', linewidth=3, s=200, facecolors='black')

# 提取KNN分类结果
dist, indices = classifier.kneighbors([test_datapoint])

# 画出KNN分类结果
plt.figure()
plt.title('k nearest neighbors')
for i in indices:
    plt.scatter(X[i, 0], X[i, 1], marker='o', linewidth=3, s=100, facecolors='black')

plt.scatter(test_datapoint[0], test_datapoint[1], marker='x', linewidth=3, s=200, facecolors='black')

for i in range(X.shape[0]):
    plt.scatter(X[i, 0], X[i, 1], marker=mapper[i], s=50, edgecolors='black', facecolors='none')

print(u"预测输出为：{}".format(classifier.predict([test_datapoint])[0]))

plt.show()