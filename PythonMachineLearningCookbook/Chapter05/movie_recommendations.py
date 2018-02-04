# ^_^ coding:utf-8 ^_^

import json
import numpy as np 

from euclidean_score import euclidean_score
from pearson_score import pearson_score
from find_similar_users import find_similar_users

# 为给定用户生成电影推荐
def generate_recommendations(dataset, user):
    
    if user not in dataset:
        raise TypeError('User {} no present in the dataset')

    total_scores = {}
    user_numbers = {}
    for u in [ x for x in dataset if x != user]:

        similarity_score = pearson_score(dataset, user, u)
        if similarity_score <= 0:
            continue

        # 找到还未被该用户评分的电影
        for item in [x for x in dataset[u] if x not in dataset[user] or dataset[user][x]==0]:
            if(total_scores.has_key(item)):                
                total_scores.update({item: dataset[u][item]*similarity_score+total_scores[item]})
                user_numbers.update({item: user_numbers[item]+1})
            else:
                total_scores.update({item: dataset[u][item]*similarity_score})
                user_numbers.update({item: 1})
    # 如果该用户看过数据库中所有电影，则不为该用户推荐电影
    if len(total_scores) == 0:
        return [u'您真的看过好多电影，我们没有可推荐的']

    # 生成一个电影评分标准化列表
    movie_ranks = np.array([[total/user_numbers[item], item] for item,total in total_scores.items()])
    # 根据第一列对皮尔逊相关系数进行降序排列
    movie_ranks = movie_ranks[np.argsort(movie_ranks[:, 0])[::-1]]
    # 提取推荐的电影
    return movie_ranks

if __name__ == '__main__':

    # 加载数据
    data_file = 'movie_ratings.json'
    with open(data_file, 'r') as f:
        data =json.loads(f.read())

    # 为Michael Henry生成推荐
    user = 'Michael Henry'
    print(u"对用户{}的推荐电影是：".format(user))
    movies = generate_recommendations(data, user)
    for i, movie in enumerate(movies):
        print(u"[{}] 推荐指数：{:.1f} 《{}》".format(i+1, float(movie[0]), movie[1]))