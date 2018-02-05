# ^_^ coding:utf-8 ^_^

import random
from nltk.corpus import names
from nltk import NaiveBayesClassifier
from nltk.classify import  accuracy as nltk_accuracy

# 提取输入单词的特性
def gender_features(word, num_letters=2):
    return {'feature': word[-num_letters:].lower()}

if __name__ == '__main__':
    # 提取标记名称
    labeled_names = ([(name, 'male') for name in names.words('male.txt')]) + \
                                  ([(name, 'female') for name in names.words('female.txt')])

    # 设置随机生成数的种子值，并混合搅乱训练数据
    random.seed(7)
    random.shuffle(labeled_names)

    # 定义一些输入的姓名
    input_names = ['Leonardo', 'Amy', 'Sam', 'Werner']

    # 搜索参数空间
    for i in range(1,5):
        print("取参数为{}".format(i))
        featuresets = [(gender_features(n, i), gender) for (n, gender) in labeled_names]
        
        # 分割数据为训练集和测试集
        train_set, test_set = featuresets[500:], featuresets[:500]

        # 用朴素贝叶斯分类器做分类
        classifier = NaiveBayesClassifier.train(train_set)

        # 打印分类器准确性
        print(u"准确性：{}%".format(100*nltk_accuracy(classifier, test_set)))

        # 为输入姓名预测结果
        for name in input_names:
            print("{} ==> {}".format(name, classifier.classify(gender_features(name, i))))