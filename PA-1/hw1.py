#!/usr/local/bin/python3
import re
import string
from nltk.stem import PorterStemmer

def readFile(filename):
    f = open(filename, 'r', encoding='UTF-8')
    content = f.read()
    f.close()
    return content

def tokenization(content):
    #remove \t\n\r\f\v
    content = re.sub('[\t\n\r\f\v]', ' ', content)
    #remove '[a-z]
    content = re.sub('\'[a-z]*', '', content)
    #remove punctuation marks -> !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    content = re.sub('['+string.punctuation+']', '', content)
    #split by space
    token_list = content.split(' ')
    #remove empty item
    token_list = list(filter(None, token_list))
    return token_list

def normalization(token_list):
    #lower case
    token_list = [item.lower() for item in token_list]
    return token_list

def stemming(token_list):
    #create new stemmer
    stemmer = PorterStemmer()
    token_list = [stemmer.stem(token) for token in token_list]
    return token_list

def removeStopWord(token_list):
    #Read Stop Word List
    stop_word_list = readFile('stop-word-list.txt')
    stop_word_list = stop_word_list.split('\n')
    #remove stop word from token_list
    token_list = [token for token in token_list if token not in stop_word_list]
    return token_list

def writeFile(filename,token_list):
    f = open(filename, 'w', encoding='UTF-8')
    for token in token_list:
        f.write("%s\n" % token)
    f.close()

def main():
    content = readFile('news.txt')
    token_list = tokenization(content)
    token_list = normalization(token_list)
    token_list = stemming(token_list)
    token_list = removeStopWord(token_list)
    writeFile('result.txt',token_list)

if __name__=="__main__":
	main()
