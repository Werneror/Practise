# ^_^ coding:utf-8 ^_^

import numpy as np
from chunking import splitter
from nltk.corpus import brown
from sklearn.feature_extraction.text import CountVectorizer

if __name__ == '__main__':

    # 读取布朗语料库数据
    data = ' '.join(brown.words()[:10000])

    # 将语料库分块
    num_words = 2000
    chunks = []
    counter = 0

    text_chunks = splitter(data, num_words)

    # 创建一个基于这些文本块的词典
    for text in text_chunks:
        chunk = {'index': counter, 'text': text}
        chunks.append(chunk)
        counter += 1

    # 提取文档-词矩阵
    vectorizer = CountVectorizer(min_df=5, max_df=.95)
    doc_term_matrix = vectorizer.fit_transform([chunk['text'] for chunk in chunks])

    vocab = np.array(vectorizer.get_feature_names())
    print("词汇：\n{}".format(vocab))

    # 打印文档-词矩阵
    print(u"文档-词矩阵：")
    chunk_names = ['Chunk-0', 'Chunk-1', 'Chunk-2', 'Chunk-3', 'Chunk-4']
    format_row = '{:>12}' * (len(chunk_names) + 1)
    print(format_row.format('Word', *chunk_names))

    for word, item in zip(vocab, doc_term_matrix.T):
        # “item”是压缩的稀疏矩阵（csr_matrix）数据结构
        output = [x for x in item.data]
        print(format_row.format(word, *output))