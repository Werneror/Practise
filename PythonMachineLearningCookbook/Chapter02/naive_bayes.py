# ^-^ coding:utf-8 ^-^

import numpy as np
from sklearn.naive_bayes import GaussianNB
from logistic_regression import plot_classifier
from sklearn import cross_validation

# 加载数据
input_file = "data_multivar.txt"

X = []
y = []

with open(input_file, 'r') as f:
	for line in f.readlines():
		data = [float(x) for x in line.split(',')]
		X.append(data[:-1])
		y.append(data[-1])

X = np.array(X)
y = np.array(y)

# 建立朴素贝叶斯分类器
classifier_gussiannb = GaussianNB()
classifier_gussiannb.fit(X, y)
y_pred = classifier_gussiannb.predict(X)

# 计算分类器的准确性
accuracy = 100.0*(y==y_pred).sum() / X.shape[0]
print(u"训练集上分类器的准确性 = {0:4f}%".format(accuracy))

# 画出数据点和边界
plot_classifier(classifier_gussiannb, X, y)


#### 2.5 将数据集分割成训练集和测试集 ####

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.25, random_state=5)
classifier_gussiannb_new = GaussianNB()
classifier_gussiannb_new.fit(X_train, y_train)
y_test_pred = classifier_gussiannb_new.predict(X_test)
accuracy = 100.0*(y_test==y_test_pred).sum() / X_test.shape[0]
print(u"测试集上分类器的准确性 = {0:4f}%".format(accuracy))
plot_classifier(classifier_gussiannb_new, X_test, y_test)


#### 2.6 用交叉验证检验模型准确性 ####

num_validations = 5
print(u"\n用交叉验证检验模型准确性：");
accuracy = cross_validation.cross_val_score(classifier_gussiannb,
	                                                             X, y, scoring="accuracy",
	                                                             cv=num_validations)
print(u"分类器的准确性 = {0:4f}%".format(100.0*accuracy.mean()))

f1 = cross_validation.cross_val_score(classifier_gussiannb,
	                                                 X, y, scoring="f1_weighted",
	                                                 cv=num_validations)
print(u"分类器的F1得分 = {0:4f}%".format(100.0*f1.mean()))

precision = cross_validation.cross_val_score(classifier_gussiannb,
	                                                 X, y, scoring="precision_weighted",
	                                                 cv=num_validations)
print(u"分类器的精度 = {0:4f}%".format(100.0*precision.mean()))

recall = cross_validation.cross_val_score(classifier_gussiannb,
	                                                 X, y, scoring="recall_weighted",
	                                                 cv=num_validations)
print(u"分类器的召回率 = {0:4f}%".format(100.0*recall.mean()))
