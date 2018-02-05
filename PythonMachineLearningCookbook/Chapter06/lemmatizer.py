# ^_^ coding:utf-8 ^_^

from nltk.stem import WordNetLemmatizer

words = ['table', 'probably', 'wolves', 'playing', 'is', 'dogs', 'the', 'beaches', 'grounded', 'dreamt', 'envision']

# 对比不同的词形还原器
lemmatizers = ['NOUN LEMMATIZER', 'VERB LEMMATIZER']

# 基于WordNet词形还原器创建一个对象
lemmatizers_wordnet = WordNetLemmatizer()
formatted_row = '{:24}' * (len(lemmatizers)+1)
print(formatted_row.format('WORD', *lemmatizers))

for word in words:
    lemmatizers_words = [lemmatizers_wordnet.lemmatize(word, pos='n'), lemmatizers_wordnet.lemmatize(word, pos='v')]
    print(formatted_row.format(word, *lemmatizers_words))
