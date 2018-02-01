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

# 将数据分为两类
class_0 = np.array([X[i] for i in range(len(X)) if y[i]==0])
class_1 = np.array([X[i] for i in range(len(X)) if y[i]==1])

# 显示数据
plt.figure()
plt.scatter(class_0[:, 0], class_0[:, 1], facecolors='black', edgecolors='black', marker='s')
plt.scatter(class_1[:, 0], class_1[:, 1], facecolors='None', edgecolors='black', marker='s')
plt.title('Input data')
plt.show()

# 分割数据集
X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.25, random_state=5)

# 用线性核函数初始化SVM对象
params = {'kernel': 'linear'}
# 用多项式函数初始化SVM对象
params = {'kernel': 'poly', 'degree':2}
# 用径向基函数初始化SVM对象
params = {'kernel': 'rbf'}
classifier = SVC(**params)

# 训练SVM分类器
classifier.fit(X_train, y_train)

# 画出对训练数据集的分类结果
utilities.plot_classifier(classifier, X_train, y_train, 'Training dataset')
plt.show()

# 对测试数据集的分类效果
y_test_pred = classifier.predict(X_test)
utilities.plot_classifier(classifier, X_test, y_test, 'Test dataset')
plt.show()

# 计算训练数据集的准确性
target_names = ['Class-' + str(int(i)) for i in set(y)]
print("#"*30)
print("在训练数据集上分类器的表现为：")
print(classification_report(y_train, classifier.predict(X_train), target_names=target_names))
print("#"*30)

# 计算测试数据集的准确性
target_names = ['Class-' + str(int(i)) for i in set(y)]
print("#"*30)
print("在测试据集上分类器的表现为：")
print(classification_report(y_test, classifier.predict(X_test), target_names=target_names))
print("#"*30)