# ^_^ coding:utf-8 ^_^

import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm, grid_search, cross_validation
from sklearn.metrics import classification_report

import utilities

# 加载数据
input_file = 'data_multivar.txt'
X, y = utilities.load_data(input_file)

# 分割数据集
X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.25, random_state=5)

# 通过交叉验证设置参数
parameter_grid = [
	{'kernel': ['linear'], 'C': [1, 10, 50, 600]},
	{'kernel': ['poly'], 'degree': [2,3]},
	{'kernel': ['rbf'], 'gamma': [0.01, 0.001], 'C':[1, 10, 50, 600]}]

# 定义需要使用的指标
metrics = ['precision', 'recall_weighted']

# 为每个指标搜索最优参数
for metric in metrics:
	print(u"为指标{}搜索最优参数：".format(metric))
	classifier = grid_search.GridSearchCV(svm.SVC(C=1), parameter_grid, cv=5, scoring=metric)
	classifier.fit(X_train, y_train)

	# 打印得分
	print(u"各参数得分：")
	for params, avg_score, _ in classifier.grid_scores_:
		print(u"{}\t{:.3f}".format(params, avg_score))

	# 打印最佳参数
	print(u"最佳参数是：{}".format(classifier.best_params_))

# 在测试数据集上做试验
y_true, y_pred = y_test, classifier.predict(X_test)
print(u"全参数报告：")
print(classification_report(y_true, y_pred))