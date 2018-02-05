# ^_^ coding:utf-8 ^_^

from nltk.tokenize import RegexpTokenizer  
from nltk.stem.snowball import SnowballStemmer
from gensim import models, corpora
from nltk.corpus import stopwords

# 加载输入数据
def load_data(input_file):
    data = []
    with open(input_file, 'r') as f:
        for line in f.readlines():
            data.append(line[:-1])
    return data

class Preprocessor(object):

    # 对各种操作进行初始化
    def __init__(self):
        # 创建正则表达式解析器
        self.tokenizer = RegexpTokenizer(r'\w+')

        # 获取停用词列表
        self.stop_words_english = stopwords.words('english')

        # 创建Snowball词干提取器
        self.stemmer = SnowballStemmer('english')

    # 标记解析、移除停用词、词干提取
    def process(self, input_text):
        # 标记解析
        tokens = self.tokenizer.tokenize(input_text.lower())

        #移除停用词
        tokens_stopwords = [x for x in tokens if not x in self.stop_words_english]

        # 词干提取
        tokens_stemmed = [self.stemmer.stem(x) for x in tokens_stopwords]

        # 返回处理后的标记
        return tokens_stemmed

if __name__ == '__main__':

    # 加载数据
    input_file = 'data_topic_modeling.txt'
    data= load_data(input_file)

    # 创建预处理对象
    preprocessor = Preprocessor()

    # 创建一组经过预处理的文档
    processed_tokens = [preprocessor.process(x) for x in data]

    # 创建基于标记的文档的词典
    dict_tokens = corpora.Dictionary(processed_tokens)
    
    # 创建文档-词矩阵
    corpus = [dict_tokens.doc2bow(text) for text in processed_tokens]

    # 基于刚刚创建的语料库生成LDA模型
    num_topics = 2
    num_words = 4
    ladmodel = models.ldamodel.LdaModel(corpus, num_topics=num_topics, id2word=dict_tokens, passes=25)

    for item in ladmodel.print_topics(num_topics=num_topics, num_words=num_words):
        print("Topic {} ===> {}".format(item[0], item[1]))