import re
from porter import PorterStemmer

p = PorterStemmer()

# Read stop words from stop-words.txt
stop_words_list = []
with open('stop-words.txt') as stop_data:
    stop_words_list = stop_data.read().split()

regex = re.compile("[a-zA-Z\-_]+")

with open('news.txt') as file:
    
    # Read the raw text and print it
    raw_data = file.read().decode("utf-8")

    # Tokenization and Lowercase 
    token_list = []
    split_data = raw_data.lower().split()
    for s in split_data:
        token_list.append(regex.match(s).group())

    # Remove stop words
    after_removed_list = []
    for s in token_list:
        if not s in stop_words_list:    
            after_removed_list.append(s)
    
    # Stemming by using Porter's algorithm
    result_list = []
    for s in after_removed_list:
        result_list.append(p.stem(s, 0, len(s)-1))

    # Write result to file
    file = open('result.txt','w')
    for result in result_list:
        file.write(result + '\n')
