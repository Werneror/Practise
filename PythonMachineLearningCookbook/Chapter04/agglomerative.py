# ^_^ coding:utf-8 ^_^

import numpy as np 
import matplotlib.pyplot as plt 
from sklearn.cluster import AgglomerativeClustering
from sklearn.neighbors import kneighbors_graph

# 定义一个实现凝聚层次聚类的函数
def perform_clustering(X, connectivity, title, num_clusters=3, linkage='ward'):
	plt.figure()
	model = AgglomerativeClustering(linkage=linkage,
		connectivity=connectivity, n_clusters=num_clusters)
	model.fit(X)

	# 提取标记
	labels = model.labels_
	# 为每种集群设置不同的标记
	markers = '.v*'
	# 绘制数据
	for i, marker in zip(range(num_clusters), markers):
		plt.scatter(X[labels==i,0], X[labels==i,1],s=50,marker=marker,color='k',facecolors='none')
	plt.title(title)

# 噪声函数
def add_noise(x, y, amplitude):
	X = np.concatenate((x, y))
	X += amplitude*np.random.randn(2, X.shape[1])
	return X.T

# 生成螺旋状数据
def get_spiral(t, noise_amplitude=0.5):
	r = t
	x = r*np.cos(t)
	y = r*np.sin(t)
	return add_noise(x, y, noise_amplitude)

# 获取位于玫瑰线上数据点的函数
def get_rose(t, noise_amplitude=0.02):
	#如果k是奇数，曲线有k朵花瓣，如果k是偶数，曲线有2k朵花瓣
	k = 5
	r = np.cos(k*t) + 0.25
	x = r*np.cos(t)
	y = r*np.sin(t)
	return add_noise(x, y, noise_amplitude)

# 为增加多样性，定义hypotrochoid函数：
def get_hypotrochoid(t, noise_amplitude=0.02):
	a, b, h = 10.0, 2.0, 4.0
	x = (a-b)*np.cos(t) + h*np.cos((a-b)/b*t)
	y = (a-b)*np.sin(t) + h*np.sin((a-b)/b*t)
	return add_noise(x, y, 0)

if __name__ == '__main__':
	#生成样本数据
	n_sample = 500
	np.random.seed(2)
	t = 2.5*np.pi*(1+2*np.random.rand(1, n_sample))
	#X = get_spiral(t)
	X = get_rose(t)
	#X = get_hypotrochoid(t)

	# 不考虑螺旋型的数据连续性
	connectivity = None
	perform_clustering(X, connectivity, 'No connectivity')

	# 根据数据连接线创建K个临近点的图形
	connectivity = kneighbors_graph(X, 10, include_self=False)
	perform_clustering(X, connectivity, 'K-Neighbors connectivity')

	plt.show()