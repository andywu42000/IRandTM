#!/usr/local/bin/python3
"""This script converts a set of documents into tf-idf vectors"""

import os
import operator
import math
import time

import hw1

def construct_dictionary(documents_dir):
	"""construct dictionary"""
	now_path = os.path.dirname(os.path.abspath(__file__))+'/'
	documents = os.listdir(now_path + documents_dir)
	dictionary = {}
	for document in documents:
		token_list = hw1.preprocessing(documents_dir+document)
		pre_token = ''
		for token in token_list:
			if token == pre_token:
				continue
			if token in dictionary:
				dictionary[token] = dictionary[token] + 1
			else:
				dictionary[token] = 1
			pre_token = token
	dictionary = sorted(dictionary.items(), key=operator.itemgetter(0))
	write_dictionary(dictionary, './dictionary.txt')

def write_dictionary(dictionary, filename):
	"""write dictionary"""
	now_path = os.path.dirname(os.path.abspath(__file__))+'/'
	f_value = open(now_path + filename, 'w', encoding='UTF-8')
	f_value.write("t_index\tterm\tdf\n")
	for i in range(0, len(dictionary)):
		f_value.write(str(i+1)+'\t' + dictionary[i][0] + '\t' + str(dictionary[i][1]))
		if i != len(dictionary)-1:
			f_value.write('\n')
	f_value.close()

def read_dictionary(filename):
	"""read dictionary from ./filename"""
	dictionary = hw1.read_file(filename)
	dictionary_list = dictionary.split('\n')
	# remove header
	del dictionary_list[0]
	return dictionary_list

def dictionary_index(dictionary_list):
	"""construct a dictionary of index"""
	dictionary_of_index = {}
	for i in dictionary_list:
		content_list = i.split('\t')
		dictionary_of_index[content_list[1]] = content_list[0]
	return dictionary_of_index

def dictionary_df(dictionary_list):
	"""construct a dictionary of df"""
	dictionary_of_df = {}
	for i in dictionary_list:
		content_list = i.split('\t')
		dictionary_of_df[content_list[1]] = content_list[2]
	return dictionary_of_df

def transfer_tfidf_unit_vector(documents_dir, dictionary_of_index, dictionary_of_df):
	"""transfer tf-idf unit vector"""
	now_path = os.path.dirname(os.path.abspath(__file__))+'/'
	documents = os.listdir(now_path + documents_dir)
	for document in documents:
		dictionary = {}
		token_list = hw1.preprocessing(documents_dir+document)
		for token in token_list:
			if token in dictionary:
				dictionary[token] = dictionary[token] + 1
			else:
				dictionary[token] = 1
		dictionary = sorted(dictionary.items(), key=operator.itemgetter(0))
		#write to unit_vector/filename
		now_path = os.path.dirname(os.path.abspath(__file__))+'/'
		if not os.path.isdir(now_path+'unit_vector'):
			os.mkdir(now_path+'unit_vector')
		f_value = open(now_path + 'unit_vector/' + document, 'w', encoding='UTF-8')
		f_value.write(str(len(dictionary))+'\n')
		f_value.write('t_index\ttf-idf')
		tfidf_squares = 0.0
		for term in dictionary:
			tfidf_pow = math.pow(count_tfidf(len(documents), float(term[1]), float(dictionary_of_df[term[0]])), 2)
			tfidf_squares = tfidf_squares + tfidf_pow
		for term in dictionary:
			f_value.write('\n')
			tf_idf = count_tfidf(len(documents), float(term[1]), float(dictionary_of_df[term[0]]))
			f_value.write(dictionary_of_index[term[0]] + '\t' + str(tf_idf/math.sqrt(tfidf_squares)))
		f_value.close()

def count_tfidf(documents_num, tf, df):
	"""count term tf-idf"""
	idf = math.log10(documents_num/df)
	tf_idf = tf * idf
	return tf_idf

def cosine(doc_x, doc_y):
	"""count the cosine similarity of two documents"""
	doc_x_content = hw1.read_file(doc_x)
	doc_y_content = hw1.read_file(doc_y)
	doc_x_content = doc_x_content.split('\n')
	doc_y_content = doc_y_content.split('\n')
	del doc_x_content[0]
	del doc_x_content[0]
	del doc_y_content[0]
	del doc_y_content[0]
	doc_x_content = [term.split('\t') for term in doc_x_content]
	doc_y_content = [term.split('\t') for term in doc_y_content]
	cosine_similarity = 0.0
	i = 0
	j = 0
	while i < len(doc_x_content) and j < len(doc_y_content):
		if int(doc_x_content[i][0]) < int(doc_y_content[j][0]):
			i = i + 1
			continue
		if int(doc_x_content[i][0]) > int(doc_y_content[j][0]):
			j = j + 1
			continue
		if int(doc_x_content[i][0]) == int(doc_y_content[j][0]):
			cosine_similarity = cosine_similarity + float(doc_x_content[i][1]) * float(doc_y_content[j][1])
			i = i + 1
			j = j + 1
			continue
	return cosine_similarity

def main():
	"""main function"""
	print(time.strftime("%Y/%m/%d %H:%M:%S"), ' ---Start!')
	construct_dictionary('IRTM/')
	dictionary_list = read_dictionary('dictionary.txt')
	dictionary_of_index = dictionary_index(dictionary_list)
	dictionary_of_df = dictionary_df(dictionary_list)
	transfer_tfidf_unit_vector('IRTM/', dictionary_of_index, dictionary_of_df)
	cosine_similarity = cosine('unit_vector/1.txt', 'unit_vector/2.txt')
	print(cosine_similarity)
	print(time.strftime("%Y/%m/%d %H:%M:%S"), ' ---Done!')

if __name__ == "__main__":
	main()
