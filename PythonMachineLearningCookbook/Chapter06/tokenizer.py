# ^_^ coding:utf-8 ^_^

# 分析对象
text = "Are you cruous about tokenization? Let's see how it works! We need to analyze a couple of sentences with punctuations to see it in action."

# 对句子进行解析
from nltk.tokenize import sent_tokenize
sent_tokenize_list = sent_tokenize(text)

# 打印句子分析结果列表
print(u"句子分析结果：{}".format(sent_tokenize_list))

# 建立一个新的单词解释器
from nltk.tokenize import word_tokenize
print(u"单词分析结果：{}".format(word_tokenize(text)))

# 创建一个带标点符号的单词解析器
from nltk.tokenize import WordPunctTokenizer

word_punkt_tokenizer = WordPunctTokenizer()
print(u"Punkt单词分析：{}".format(word_punkt_tokenizer.tokenize(text)))