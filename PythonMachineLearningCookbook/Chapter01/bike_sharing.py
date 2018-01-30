# ^-^ coding:utf-8 ^-^
import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
from sklearn import cross_validation
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, explained_variance_score

# 绘制条形图的函数
def plot_feature_importances(feature_impoerances, title, feature_names):
	# 将重要性质标准化
	feature_impoerances = 100.0*(feature_impoerances/max(feature_impoerances))

	# 将得分从高到低排序
	index_sored = np.flipud(np.argsort(feature_impoerances))

	# 让X坐标轴上的标签居中显示
	pos = np.arange(index_sored.shape[0]) + 0.5

	# 画出条形图
	plt.figure()
	plt.bar(pos, feature_impoerances[index_sored], align='center')
	plt.xticks(pos, feature_names[index_sored])
	plt.ylabel('Relative Impoertance')
	plt.title(title)
	plt.show()

# 数据加载函数
def load_dataset(filename):
	file_reader = csv.reader(open(filename, 'r'), delimiter=',')
	X, y = [], []
	for row in file_reader:
		X.append(row[2:13])
		y.append(row[-1])
	# 提取特征名称
	feature_names = np.array(X[0])
	#将第一行特征名称移除，仅保留数值
	return np.array(X[1:]).astype(np.float32), np.array(y[1:]).astype(np.float32), feature_names

# 读取数据并打乱顺序并划分数据
X, y, feature_names = load_dataset("bike_day.csv")
X, y = shuffle(X, y, random_state = 7)
X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.1, random_state=0)

rf_regressor = RandomForestRegressor(n_estimators=1000, #评估器（决策树）数量
	                                                     max_depth=10, #每个决策树的最大深度
	                                                     min_samples_split=1) #决策树分裂一个节点需要用到的最小数量样本
rf_regressor.fit(X_train, y_train)

# 评价随机森林回归器的训练效果
y_pred = rf_regressor.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
evs = explained_variance_score(y_test, y_pred)
print(u"均方误差\t{0:.8f}".format(mse_dt))
print(u"解释方差分\t{0:.8f}".format(evs_dt))

plot_feature_importances(rf_regressor.feature_impoerances_, 'Random Forest regressor', feature_names)