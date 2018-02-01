# ^_^ coding:utf-8 ^_^

import numpy as np 
from sklearn.svm import SVC
import matplotlib.pyplot as plt 
from sklearn import cross_validation
from sklearn.metrics import classification_report

import utilities

# 加载数据
input_file = 'data_multivar.txt'
X, y = utilities.load_data(input_file)

# 分割数据集
X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.25, random_state=5)

# 用径向基函数初始化SVM对象
params = {'kernel': 'rbf', 'probability': True}
classifier = SVC(**params)

# 训练SVM分类器
classifier.fit(X_train, y_train)

input_datapoints = np.array([[2,1.5],[8,9],[4.8,5.2],[4,4],[2.5,7],[7.6,2],[5.4,5.9]])

# 测量数据点与边界距离
print(u"数据点到边界的距离：")
for i in input_datapoints:
	print(u"{}\t到边界的距离为\t{:.3f}".format(i, classifier.decision_function([i])[0]))

# 测量数据点分类的置信度
print(u"数据点分类的置信度：")
for i in input_datapoints:
	print(u"{}\t到边界的置信度为\t{}".format(i, classifier.predict_proba([i])))

# 画出数据点与边界的位置

utilities.plot_classifier(classifier, input_datapoints, [0]*len(input_datapoints), 'Input datapoints', True)
plt.show()