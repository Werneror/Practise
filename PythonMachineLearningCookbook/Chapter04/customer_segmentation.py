# ^_^ coding:utf-8 ^_^

import csv

import numpy as np 
from sklearn import cluster, covariance, manifold
from sklearn.cluster import MeanShift, estimate_bandwidth
import matplotlib.pyplot as plt 

# 从输入文件中加载数据
input_file = 'wholesale.csv'
file_reader = csv.reader(open(input_file, 'r'), delimiter=',')
X = []
for count, row in enumerate(file_reader):
	if not count:
		names = row[2:]
		continue
	X.append([float(x) for x in row[2:]])

# 转换为numpy数组
X = np.array(X)

# 估计带宽参数bandwidth
bandwidth = estimate_bandwidth(X, quantile=0.8, n_samples=len(X))

# 用MeanShift函数计算聚类
meanshift_estimator = MeanShift(bandwidth=bandwidth, bin_seeding=True)
meanshift_estimator.fit(X)
labels = meanshift_estimator.labels_
centroids = meanshift_estimator.cluster_centers_
num_clusters = len(np.unique(labels))

# 打印获得的集群中心
print("输入数据分为 {} 个类".format(num_clusters))
print("分类中心为：")
print('\t'.join([name[:3] for name in names]))
for centroid in centroids:
	print( '\t'.join([str(int(x)) for x in centroid]))

# 数据可视化
centroids_milk_groceries = centroids[:, 1:3]

plt.figure()
plt.scatter(centroids_milk_groceries[:, 0], centroids_milk_groceries[:, 1],
	s = 100, edgecolors='k', facecolors='none')
offset = 0.2
plt.xlim(centroids_milk_groceries[:,0].min()-offset*centroids_milk_groceries[:,0].ptp(),
	centroids_milk_groceries[:,0].max()+offset*centroids_milk_groceries[:,0].ptp())
plt.ylim(centroids_milk_groceries[:,1].min()-offset*centroids_milk_groceries[:,1].ptp(),
	centroids_milk_groceries[:,1].max()+offset*centroids_milk_groceries[:,1].ptp())
plt.title('Centroids of clusters for milk and groceries')
plt.show()