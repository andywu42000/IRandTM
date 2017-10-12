#!/usr/local/bin/python3
"""This script extracts terms from a document"""
import re
import os
import string
from nltk.stem import PorterStemmer

def preprocessing(filename):
	"""read a file and preprocessing ,return a token list"""
	content = read_file(filename)
	token_list = tokenization(content)
	token_list = normalization(token_list)
	token_list = stemming(token_list)
	token_list = remove_stop_word(token_list)
	token_list = sorted(token_list)
	return token_list

def read_file(filename):
	"""Read the file of dictionary and return a string"""
	now_path = os.path.dirname(__file__)+'/'
	f_value = open(now_path + filename, 'r', encoding='UTF-8')
	content = f_value.read()
	f_value.close()
	return content

def tokenization(content):
	"""tokenization"""
	#remove \t\n\r\f\v
	content = re.sub('[\t\n\r\f\v]', ' ', content)
	#remove '[a-z]
	content = re.sub('\'[a-z]*', '', content)
	#remove [0-9]
	content = re.sub('[0-9]', '', content)
	#remove punctuation marks -> !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
	content = re.sub('['+string.punctuation+']', '', content)
	#split by space
	token_list = content.split(' ')
	#remove empty item
	token_list = list(filter(None, token_list))
	return token_list

def normalization(token_list):
	"""normalization"""
	#lower case
	token_list = [item.lower() for item in token_list]
	return token_list

def stemming(token_list):
	"""stemming"""
	#create new stemmer
	stemmer = PorterStemmer()
	token_list = [stemmer.stem(token) for token in token_list]
	return token_list

def remove_stop_word(token_list):
	"""remove stop word"""
	#Read Stop Word List
	stop_word_list = read_file('stop-word-list.txt')
	stop_word_list = stop_word_list.split('\n')
	#remove stop word from token_list
	token_list = [token for token in token_list if token not in stop_word_list]
	return token_list

def write_file(filename, token_list):
	"""write files"""
	now_path = os.path.dirname(__file__)+'/'
	f_value = open(now_path + filename, 'w', encoding='UTF-8')
	for token in token_list:
		f_value.write("%s\n" % token)
	f_value.close()


def main():
	"""main function"""
	token_list = preprocessing('news.txt')
	write_file('result.txt', token_list)


if __name__ == "__main__":
	main()
