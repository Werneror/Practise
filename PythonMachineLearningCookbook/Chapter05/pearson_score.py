# ^_^ coding:utf-8 ^_^

import json
import numpy as np 

def pearson_score(dataset, user1, user2):

    if user1 not in dataset:
        raise TypeError('user {} not present in the dataset'.format(user1))
    if user2 not in dataset:
        raise TypeError('user {} not present in the dataset'.format(user2))

    # 提取两个用户均评过分的电影
    rated_by_both = {}
    for item in dataset[user1]:
        if item in dataset[user2]:
            rated_by_both[item] = 1

    num_ratings = len(rated_by_both)

    # 如果两个用户没有共同评分过的电影，得分为0
    if num_ratings == 0:
        return 0

    # 分别计算两用户均评过分的电影的评分之和
    user1_sum = np.sum([dataset[user1][item] for item in rated_by_both])
    user2_sum = np.sum([dataset[user2][item] for item in rated_by_both])

    # 分别计算两用户均评过分的电影的评分平方和
    user1_squared_sum = np.sum([ np.square(dataset[user1][item]) for item in rated_by_both])
    user2_squared_sum = np.sum([ np.square(dataset[user2][item]) for item in rated_by_both])

    # 计算两用户均评过分的电影的评分乘积之和
    product_sum = np.sum([dataset[user1][item]*dataset[user2][item] for item in rated_by_both])

    # 计算皮尔逊相关度
    Sxy = product_sum - (user1_sum * user2_sum / num_ratings)
    Sxx = user1_squared_sum - np.square(user1_sum) / num_ratings
    Syy = user2_squared_sum - np.square(user2_sum) / num_ratings

    # 考分为0的情况
    if Sxx*Syy == 0:
        return 0
    return Sxy / np.sqrt(Sxx*Syy)

if __name__ == '__main__':
        # 加载数据
    data_file = 'movie_ratings.json'
    with open(data_file, 'r') as f:
        data =json.loads(f.read())

    # 计算两用户的欧氏距离
    user1 = 'John Carson'
    user2 = 'Michelle Peterson'
    score = pearson_score(data, user1, user2)
    print(u"{}和{}的皮尔逊相关度为{:.4f}".format(user1, user2, score))