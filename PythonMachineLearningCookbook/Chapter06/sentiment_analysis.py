# ^_^ coding:utf-8 ^_^

import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews

def extract_features(word_list):
    return dict([(word, True) for word in word_list])

if __name__ == '__main__':
    # 加载积极与消极评论
    positive_fileids = movie_reviews.fileids('pos')
    negative_fileids = movie_reviews.fileids('neg')

    features_positive = [(extract_features(movie_reviews.words(fileids=[f])), 
                                     'Positive') for f in positive_fileids]
    features_negative = [(extract_features(movie_reviews.words(fileids=[f])),
                                      'Negative') for f in negative_fileids]

    # 划分测试集和训练集
    threshold_factor = 0.8
    threshold_positive = int(threshold_factor*len(features_positive))
    threshold_negative = int(threshold_factor*len(features_negative))

    # 提取特征
    features_train = features_positive[:threshold_positive] + features_negative[:threshold_negative]
    features_test = features_positive[threshold_positive:] + features_negative[threshold_negative:]

    print("训练集数量为：{}，测试集数量为：{}".format(len(features_train), len(features_test)))

    # 训练朴素贝叶斯分类器
    classifier = NaiveBayesClassifier.train(features_train)
    print(u"训练器精确度为：{}%".format(100*nltk.classify.util.accuracy(classifier, features_test)))

    # 打印含信息量最多的前十个单词
    print(u"含信息量最多的前十个单词：")
    for item in classifier.most_informative_features()[:10]:
        print(item[0])
    
    # 输入一些简单的评论        
    input_reviews = [
        "It is an amazing movie", 
        "This is a dull movie. I would never recommend it to anyone.",
        "The cinematography is pretty great in this movie", 
        "The direction was terrible and the story was all over the place"]

    # 对输入评论进行情感分析
    for review in input_reviews:
        probdist = classifier.prob_classify(extract_features(review.split()))
        pred_semtiment = probdist.max()
        probability = probdist.prob(pred_semtiment)*100   
        print(u"输入：{}\n分析：{}\n概率：{:.2f}%".format(review, pred_semtiment, probability))