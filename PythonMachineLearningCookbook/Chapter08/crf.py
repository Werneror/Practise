# ^_^ coding:utf-8 ^_^

import argparse

import numpy as np
from pystruct.models import ChainCRF
from pystruct.datasets import load_letters
from pystruct.learners import FrankWolfeSSVM


# 定义参数解析器 C是超参数
def build_arg_parser():
    parser = argparse.ArgumentParser(description='Trains the CRF classifier')
    parser.add_argument("--c-value", 
                                          dest = "c_value",
                                          required = False,
                                          type = float,
                                          default = 1.0,
                                          help = 'The C value that will be used for training')
    return parser

# 定义一个类处理所有CRF相关事宜
class CRFTrainer(object):

    def __init__(self, c_value, classifier_name='ChainCRF'):
        self.c_value = c_value
        self.classifier_name = classifier_name

        if self.classifier_name == 'ChainCRF':
            model = ChainCRF()
            self.clf = FrankWolfeSSVM(model=model, C=self.c_value, max_iter=50)
        else:
            raise TypeError('Invalid classifier type')

    def load_data(self):
        letters = load_letters()

        X, y, folds = letters['data'], letters['labels'], letters['folds']
        X, y = np.array(X), np.array(y)
        return X, y, folds

    # X是一个由样本组成的numpy数组，每个样本为（字母，数值）
    def train(self, X_train, y_train):
        self.clf.fit(X_train, y_train)

    def evaluate(self, X_test, y_test):
        return self.clf.score(X_test, y_test)

    # 对输入数据运行分类器
    def classify(self, input_data):
        return self.clf.predict(input_data)[0]


def decoder(arr):
    alphabets = 'abcdefghijklmnopqrstuvwxyz'
    output = ''
    for i in arr:
        output += alphabets[i]
    return output


if __name__ == '__main__':
    # 接收参数
    args = build_arg_parser().parse_args()
    c_value = args.c_value

    # 初始化
    crf = CRFTrainer(c_value)

    # 加载数据
    X, y, folds = crf.load_data()

    # 将数据分割成训练集和测试集
    X_train, X_test = X[folds == 1], X[folds != 1]
    y_train, y_test = y[folds == 1], y[folds != 1]

    # 训练CRF模型
    print(u"训练CRF模型......")
    crf.train(X_train, y_train)

    # 评价CRF模型性能
    score = crf.evaluate(X_test, y_test)
    print(u"精确度是：{:.2f}%".format(score * 100))

    # 输入一个随机测试向量，并用模型预测输出
    print(u"输入：{}".format(decoder(y_test[0])))
    predict_output = crf.classify([X_test[0]])
    print(u"预测：{}".format(decoder(predict_output)))
