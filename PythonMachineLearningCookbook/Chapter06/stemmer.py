# ^_^ coding:utf-8 ^_^

from nltk.stem.porter import PorterStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.snowball import SnowballStemmer

# 定义将要提取词干的词
words = ['table', 'probably', 'wolves', 'playing', 'is', 'dogs', 'the', 'beaches', 'grounded', 'dreamt', 'envision']

# 对比不同的词干提取算法
stemmers = ['Porter', 'Lancaster', 'Snowball']

stemmers_porter = PorterStemmer()
stemmers_lancaster = LancasterStemmer()
stemmers_snowball = SnowballStemmer('english')

format_row = '{:>16}' * (len(stemmers)+1)
print format_row
print(format_row.format('WORD', *stemmers))

for word in words:
    stemmers_words = [stemmers_porter.stem(word), stemmers_lancaster.stem(word), stemmers_snowball.stem(word)]
    print(format_row.format(word, *stemmers_words))