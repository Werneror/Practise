# ^_^ coding:utf-8 ^_^

import numpy as np 
import matplotlib.pyplot as plt 
from sklearn import metrics
from sklearn.cluster import KMeans

import utilities

# 加载数据
data = utilities.load_data('data_perf.txt')

# 迭代寻找集群最佳数量
scores = []
range_values = np.arange(2, 10)

for i in range_values:
	#训练模型
	kmeans = KMeans(init='k-means++', n_clusters=i, n_init=10)
	kmeans.fit(data)
	score = metrics.silhouette_score(data, kmeans.labels_, metric='euclidean', sample_size=len(data))
	print("u数量：{}\t得分：{:.4f}".format(i, score))

	scores.append(score)

# 画出得分条形图
plt.figure()
plt.bar(range_values, scores, width=0.6, color='k', align='center')
plt.title('Silhouette score vs number of clusters')
plt.show()

# 画出数据
plt.figure()
plt.scatter(data[:,0], data[:,1], color='k', s=30, marker='o', facecolors='none')
x_min, x_max = min(data[:,0]) -1, max(data[:,0])+1
y_min, y_max = min(data[:,1]) -1, max(data[:,1])+1
plt.title('Input data')
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.xticks(())
plt.yticks(())
plt.show()

