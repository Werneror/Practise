# ^_^ coding:utf-8 ^_^

import numpy as np 
import matplotlib.pyplot as plt 
from sklearn.neighbors import NearestNeighbors

# 输入数据
X = np.array([[1, 1],
                       [1, 3],
                       [2, 2],
                       [2.5, 5],
                       [3, 1],
                       [4 ,2],
                       [2, 3.5],
                       [3 ,3],
                       [3.5, 4]])

# 寻找最近邻的数量
num_neighbors = 3

# 输入数据点
input_point = [2.6, 1.7]

# 建立最近邻模型
knn = NearestNeighbors(n_neighbors=num_neighbors, algorithm='ball_tree').fit(X)

# 计算输入点与输入数据中所有点的距离
distances, indices = knn.kneighbors([input_point])

# 打印出k个最近邻点
print(u"{}个最近邻点为：".format(num_neighbors))
for rank, index in enumerate(indices[0][:num_neighbors]):
    print(u"{} --> {}".format(rank+1, X[index]))

# 画出最近邻点
plt.figure()
plt.scatter(X[:,0], X[:,1], marker='o', s=25, color='k')
plt.scatter(X[indices][0][:][:, 0], X[indices][0][:][:, 1], marker='o', s=150, color='k', facecolors='none')
plt.scatter(input_point[0], input_point[1], marker='*', s=150, color='k', facecolors='none')
plt.show()