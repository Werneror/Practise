# ^-^ coding:utf-8 ^-^

import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn import datasets
from sklearn.metrics import mean_squared_error, explained_variance_score
from sklearn.utils import shuffle
import matplotlib.pyplot as plt
from sklearn import cross_validation

# 加载房屋价格数据
housing_data = datasets.load_boston()

# 打乱数据
X, y = shuffle(housing_data.data, housing_data.target, random_state=7)

# 划分数据
X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2, random_state=0)

# 用普通决策树回归模型进行拟合
dt_regressor = DecisionTreeRegressor(max_depth=4)
dt_regressor.fit(X_train, y_train)

# 用带AdaBoost算法的决策树回归模型进行拟合
ab_regressor = AdaBoostRegressor(DecisionTreeRegressor(max_depth=4),
	                                             n_estimators=400,
	                                             random_state=7)
ab_regressor.fit(X_train, y_train)

# 评价训练效果
y_pred_dt = dt_regressor.predict(X_test)
y_pred_ab = ab_regressor.predict(X_test)
mse_dt = mean_squared_error(y_test, y_pred_dt)
evs_dt = explained_variance_score(y_test, y_pred_dt)
mse_ab = mean_squared_error(y_test, y_pred_ab)
evs_ab = explained_variance_score(y_test, y_pred_ab)

print(u"回归算法\t普通决策树\tAdaBoost决策树")
print(u"均方误差\t{0:.8f}\t{1:.8f}".format(mse_dt, mse_ab))
print(u"解释方差分\t{0:.8f}\t{1:.8f}".format(evs_dt, evs_ab))

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

# 计算特征的相对重要性并绘图
plot_feature_importances(dt_regressor.feature_importances_,
	                             'Decision Tree regressor',
	                             housing_data.feature_names)
plot_feature_importances(ab_regressor.feature_importances_,
	                             'AdaBoost Tree regressor',
	                             housing_data.feature_names)