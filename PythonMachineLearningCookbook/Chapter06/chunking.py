# ^_^ coding:utf-8 ^_^

import numpy as np
from nltk.corpus import brown

# 将文本分割成块
def splitter(data, num_words):
    words = data.split(' ')
    output = []

    # 初始化变量
    cur_count = 0
    cur_words = []

    for word in words:
        cur_words.append(word)
        cur_count += 1
        if cur_count == num_words:
            output.append(' '.join(cur_words))
            cur_words = []
            cur_count = 0

    #将cur_words中剩余的词也加入到返回值中
    output.append(' '.join(cur_words))

    return output

if __name__ == '__main__':
    # 加载预料库
    data = ' '.join(brown.words()[:10000])

    # 每块包含的单词数目
    num_words = 1700

    chunks = []
    counter = 0

    text_chunks = splitter(data, num_words)
    print(u"分块个数为：{}".format(len(text_chunks)))

    print(u"各块开头为：")
    for i in range(len(text_chunks)):
        print("[第{}块] {}".format(i+1, text_chunks[i][:40]))