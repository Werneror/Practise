# ^_^ coding:utf-8 ^_^

import json
import numpy as np 

#计算user1和user2的欧氏距离分数
def euclidean_score(dataset, user1, user2):

    if user1 not in dataset:
        raise TypeError('user {} not present in the dataset'.format(user1))
    if user2 not in dataset:
        raise TypeError('user {} not present in the dataset'.format(user2))

    # 提取两个用户均评过分的电影
    rated_by_both = {}
    for item in dataset[user1]:
        if item in dataset[user2]:
            rated_by_both[item] = 1

    # 如果两个用户没有共同评分过的电影，得分为0
    if len(rated_by_both) == 0:
        return 0

    # 计算两用户评分之差的平方和的平方根，并返回归一化的值
    squared_differences = []
    for item in dataset[user1]:
        if item in dataset[user2]:
            squared_differences.append(np.square(dataset[user1][item]-dataset[user2][item]))

    return 1/(1+np.sqrt(np.sum(squared_differences)))

if __name__ == '__main__':
    # 加载数据
    data_file = 'movie_ratings.json'
    with open(data_file, 'r') as f:
        data =json.loads(f.read())

    # 计算两用户的欧氏距离
    user1 = 'John Carson'
    user2 = 'Michelle Peterson'
    score = euclidean_score(data, user1, user2)
    print(u"{}和{}的欧氏距离为{:.4f}".format(user1, user2, score))