# ^_^ coding:utf-8 ^_^

import numpy as np
from itertools import cycle
import matplotlib.pyplot as plt
from sklearn.cluster import MeanShift, estimate_bandwidth

import utilities

# 加载数据
X = utilities.load_data('data_multivar.txt')

# 设置带宽参数bandwidth
bandwidth = estimate_bandwidth(X, quantile=0.1, n_samples=len(X))

# 用MeanShift计算聚类
meanshift_estimator = MeanShift(bandwidth=bandwidth, bin_seeding=True)

# 训练模型
meanshift_estimator.fit(X)

# 提取标记
labels = meanshift_estimator.labels_

# 从模型中提取集群的中心点
centroids = meanshift_estimator.cluster_centers_
num_clusters = len(np.unique(labels))

print(u"输入数据被分为{}个集群。".format(num_clusters))

# 将集群可视化
plt.figure()

# 为每种集群设置不同标记
markser = '.*xv'

# 迭代数据并画出它们
for i ,marker in zip(range(num_clusters), markser):
	# 画出集群中的数据点
	plt.scatter(X[labels==i, 0], X[labels==i,1], marker=marker, color='k')

	# 画出集群中心
	centroid = centroids[i]
	plt.plot(centroid[0], centroid[1], marker='o', markerfacecolor='k', markeredgecolor='k', markersize=15)

plt.title('Clusters and their centroids')
plt.show()