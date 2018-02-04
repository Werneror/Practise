# ^_^ coding:utf-8 ^_^

import json
import numpy as np 

from pearson_score import pearson_score

# 寻找特定数量的与输入用户相似的用户
def find_similar_users(dataset, user, num_users):
    
    if user not in dataset:
        raise TypeError('User {} not present in the dataset'.format(user))

    # 计算所有用户的皮尔逊相关度
    scores = np.array([ [X, pearson_score(dataset, user, X)] for X in dataset if user != X] )

    # 评分按照第二列排序
    scores_sorted =  scores[np.argsort(scores[:, 1])]

    # 评分按照降序排列
    scores_sorted_dec = scores_sorted[::-1]

    # 提取出k个最高得分并返回
    return scores_sorted_dec[0: num_users]

if __name__ == '__main__':
    # 加载数据
    data_file = 'movie_ratings.json'
    with open(data_file, 'r') as f:
        data =json.loads(f.read())

    # 查找三个与John Carson最相近的用户
    user = 'John Carson'
    similar_users = find_similar_users(data, user, 3)
    print(u"与John Carson最相近的三个用户是：")
    for item in similar_users:
        print(u"{}\t{:}".format(item[0], item[1]))