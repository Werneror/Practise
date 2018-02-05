# ^_^ coding:utf-8 ^_^

from sklearn.datasets import fetch_20newsgroups

# 选择一个类型列表，并且用词典映射方式定义
category_map = {'misc.forsale': 'Sales',
                             'rec.motorcycles': 'Motorcycles',
                             'rec.sport.baseball': 'Baseball',
                             'sci.crypt': 'Cryptography',
                             'sci.space': 'Space'}

# 基于刚刚定义的类型加载训练数据集
training_data = fetch_20newsgroups(subset='train',
                                                               categories=category_map.keys(),
                                                               shuffle=True,
                                                               random_state=7)

# 特征提取
from sklearn.feature_extraction.text import CountVectorizer

# 对训练数据提取特征
vectorizer = CountVectorizer()
X_train_termcounts = vectorizer.fit_transform(training_data.data)
print(u"训练数据的维度是：{}".format(X_train_termcounts.shape))

# 训练分类器
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer

# 定义tf-idf变换器对象并训练
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_termcounts)

# 训练多项式朴素贝叶斯分类器
classifier = MultinomialNB().fit(X_train_tfidf, training_data.target)

# 定义一些随即输入的句子
input_data = [
    "The curveballs of right handed pitchers tend to curve to the left", 
    "Caesar cipher is an ancient form of encryption",
    "This two-wheeler is really good on slippery roads"]

# 用词频统计转换输入数据
X_input_termcounts = vectorizer.transform(input_data)

# 用tf-idf变换器转换输入数据
X_input_tfidf = tfidf_transformer.transform(X_input_termcounts)

# 用训练过的分类器预测句子类型
predicted_categories = classifier.predict(X_input_tfidf)

# 打印结果
for sentence, category in zip(input_data, predicted_categories):
    print("输入：{}.\n类型：{}".format(sentence, 
              category_map[training_data.target_names[category]]))