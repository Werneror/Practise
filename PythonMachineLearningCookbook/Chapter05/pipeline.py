# ^_^ coding:utf-8 ^_^

from sklearn.datasets import samples_generator
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.pipeline import Pipeline

# 生成样本数据
X, y = samples_generator.make_classification(n_informative=4,
                                                                              n_features=20,
                                                                              n_redundant=0,
                                                                              random_state=5)
#n_features :特征个数= n_informative（） + n_redundant + n_repeated
#n_informative：提供信息的特征的个数
#n_redundant：冗余信息，informative特征的随机线性组合
#n_repeated ：重复信息，随机提取n_informative和n_redundant 特征
#n_classes：分类类别
#n_clusters_per_class ：某一个类别是由几个cluster构成的

# 特征选择器
selece_k_best = SelectKBest(f_regression, k=10)

# 随机森林分类器
classifier = RandomForestClassifier(n_estimators=50, max_depth=4)

# 构建机器学习流水线
pipeline_classifier = Pipeline([('selector', selece_k_best), ('rf', classifier)])

# 可调整流水线参数
pipeline_classifier.set_params(selector__k=10, rf__n_estimators=25)

# 训练分类器
pipeline_classifier.fit(X, y)

# 输出预测结果
prediction = pipeline_classifier.predict(X)
print(u"预测结果是：{}".format(prediction))

# 打印分类器得分
print(u"分类器得分：{:.2f}".format(pipeline_classifier.score(X, y)))

# 查看被选中的特征
feature_status = pipeline_classifier.named_steps['selector'].get_support()
selected_features = []
for count, item in enumerate(feature_status):
    if item:
        selected_features.append(count)
print(u"选中特征为：{}".format(', '.join([str(x) for x in selected_features])))