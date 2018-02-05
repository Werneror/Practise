# 《Python机器学习经典实例》手敲代码

运行环境：

- python 2.7.14
- numpy 1.10.2
- sklearn 0.19.1
- matplotlib 1.5.1

## Chapter01 监督学习

- 1.1 简介
- 1.2 数据预处理技术 [preprocessor.py](Chapter01/preprocessor.py)
- 1.3 标记编码方法 [label_encoder.py](Chapter01/label_encoder.py)
- 1.4 创建线性回归器 [regressor_linear.py](Chapter01/regressor_linear.py)
- 1.5 计算回归准确性 [regressor_linear.py](Chapter01/regressor_linear.py)
- 1.6 保存模型数据 [regressor_linear.py](Chapter01/regressor_linear.py)
- 1.7 创建岭回归器 [regressor_ridge.py](Chapter01/regressor_ridge.py)
- 1.8 创建多项式回归器 [regressor_multivar.py](Chapter01/regressor_multivar.py)
- 1.9 估计房屋价格 [housing.py](Chapter01/housing.py)
- 1.10 计算特征的相对重要性 [housing.py](Chapter01/housing.py)
- 1.11 评估共享单车的需求分布 [bike_sharing.py](Chapter01/bike_sharing.py)

## Chapter02 创建分类器

- 2.1 简介
- 2.2 建立简单分类器 [simple_classifier.py](Chapter02/simple_classifier.py)
- 2.3 建立逻辑回归分类器 [logistic_regression.py](Chapter02/logistic_regression.py)
- 2.4 建立朴素贝叶斯分类器 [naive_bayes.py](Chapter02/naive_bayes.py)
- 2.5 将数据集分割成训练集和测试集 [naive_bayes.py](Chapter02/naive_bayes.py)
- 2.6 用交叉验证检验模型准确性 [naive_bayes.py](Chapter02/naive_bayes.py)
- 2.7 混淆矩阵可视化 [confusion_matrix.py](Chapter02/confusion_matrix.py)
- 2.8 提取性能报告 [performance_reports.py](Chapter02/performance_reports.py)
- 2.9 根据汽车特征评估质量 [car.py](Chapter02/car.py)
- 2.10 生成验证曲线 [car.py](Chapter02/car.py)
- 2.11 生成学习曲线 [car.py](Chapter02/car.py)
- 2.12 估算收入阶层 [income.py](Chapter02/income.py)

## Chapter03 预测建模

- 3.1 简介 
- 3.2 用SVM建立线性分类器 [svm.py](Chapter03/svm.py)
- 3.3 用SVM建立非线性分类器 [svm.py](Chapter03/svm.py)
- 3.4 解决类型数量不平衡问题 [svm_imbalance.py](Chapter03/svm_imbalance.py)
- 3.5 提取置信度 [svm_confidence.py](Chapter03/svm_confidence.py)
- 3.6 寻找最优超参数 [perform_grid_search.py](Chapter03/perform_grid_search.py)
- 3.7 建立事件预测器 [event.py](Chapter03/event.py)
- 3.8 估算交通流量 [traffic.py](Chapter03/traffic.py)

## Chapter04 无监督学习——聚类

- 4.1 简介
- 4.2 用k-means算法聚类数据 [kmeans.py](Chapter04/kmeans.py)
- 4.3 用矢量量化压缩图片 [vector_quantization.py](Chapter04/vector_quantization.py)
- 4.4 建立均值漂移聚类模型 [mean_shift.py](Chapter04/mean_shift.py)
- 4.5 用凝聚层次聚类进行数据分组 [agglomerative.py](Chapter04/agglomerative.py)
- 4.6 评价聚类算法的聚类效果 [performance.py](Chapter04/performance.py)
- 4.7 用DBSCAN算法自动估算集群数量 [estimate_clusters.py](Chapter04/estimate_clusters.py)
- 4.8 探索股票数据的模式 [stock_market.py](Chapter04/stock_market.py)
- 4.9 建立客户细分模型 [customer_segmentation.py](Chapter04/customer_segmentation.py)

## Chapter05 构建推荐引擎

- 5.1 简介
- 5.2 为数据处理构建函数组合 [function_composition.py](Chapter05/function_composition.py)
- 5.3 构建机器学习流水线 [pipeline.py](Chapter05/pipeline.py)
- 5.4 寻找最近邻 [knn.py](Chapter05/knn.py)
- 5.5 构建一个KNN分类器 [nn_classification.py](Chapter05/nn_classification.py)
- 5.6 构建一个KNN回归器 [nn_regression.py](Chapter05/nn_regression.py)
- 5.7 计算欧氏距离分数 [euclidean_score.py](Chapter05/euclidean_score.py)
- 5.8 计算皮尔逊相系数 [pearson_score.py](Chapter05/pearson_score.py)
- 5.9 寻找数据集中的相似用户 [find_similar_users.py](Chapter05/find_similar_users.py)
- 5.10 生成电影推荐 [movie_recommendations.py](Chapter05/movie_recommendations.py)

## Chapter06 分析文本数据

- 6.1 简介
- 6.2 用标记解析的方法预处理数据 [tokenizer.py](Chapter06/tokenizer.py)
- 6.3 提取文本数据的词干 [stemmer.py](Chapter06/stemmer.py)
- 6.4 用词形还原的方法还原文本的基本形式 [lemmatizer.py](Chapter06/lemmatizer.py)
- 6.5 用分块的方法划分文本 [chunking.py](Chapter06/chunking.py)
- 6.6 创建词袋模型 [bag_of_words.py](Chapter06/bag_of_words.py)
- 6.7 创建文本分类器 [tfidf.py](Chapter06/tfidf.py)
- 6.8 识别性别 [gender_identification.py](Chapter06/gender_identification.py)
- 6.9 分析句子情感 [sentiment_analysis.py](Chapter06/sentiment_analysis.py)
- 6.10 用主题建模识别文本的模式 [topic_modeling.py](Chapter06/topic_modeling.py)