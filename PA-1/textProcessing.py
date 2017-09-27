
# coding: utf-8

# In[10]:

import re, nltk
from nltk.stem.porter import *

# R0672532
# 開啟news.txt檔並作初步的分割、去跳行及全小寫化
raw = open('news.txt', 'r', encoding='UTF-8').read().lower().strip().split()

# token化分割的單詞
tokens = []
for text in raw:
    tokens.append(re.compile("[^a-zA-Z\-_]").sub('', text))

# 使用nltk的PorterStemmer
stemmer = PorterStemmer()
singles = [stemmer.stem(token) for token in tokens]

# 開啟stopwords.txt去除stopwords並輸出結果
stopwords = open('stopwords.txt', 'r', encoding='UTF-8').read()
filtered_words = [word for word in singles if word not in stopwords]

output_file = open('result.txt', 'w', encoding='UTF-8')
for word in filtered_words:
    output_file.write(word + '\n')
output_file.close()


# In[ ]:




# In[ ]:



