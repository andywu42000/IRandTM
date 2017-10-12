import nltk
import math
import collections
from terms import term_generate

def main_function():
    document_count = 100
    idf_values = {}
    doc_tfidf = []

    # Go over all document and get:
    dictionary = {}         # term -> docID
    doc_word_count = []     # list of dict for knowing terms in every doc
    for i in range(1, document_count+1):
        with open('IRTM/' + str(i) + '.txt') as file:
            raw_data = file.read().decode("utf-8")
            result_list = term_generate(raw_data)
            word_count = {}
            for term in result_list:
                dictionary.setdefault(term, []).append(i)
                word_count[ term ] = word_count.setdefault(term, 0) + 1
            doc_word_count.append(word_count)

    dict_ordered_keys = sorted(dictionary)

    # Iterate all terms and write to dictionary.txt and calculate idf value
    dict_file = open('dictionary.txt', 'w')

    for i, term in enumerate(dict_ordered_keys):
        this_df = len(set(dictionary[term]))
        dict_file.write('{:8}{:25}{}\n'.format( str(i+1), term, str(this_df)))
        idf_values[term] = math.log(document_count / this_df, 10)

    dict_file.close()

    # Calculate for every doc's tfidf
    for i, word_count in enumerate(doc_word_count):
        this_result = {}
        for term in word_count.keys():
            term_index = dict_ordered_keys.index(term) + 1
            this_result[term_index] = word_count[term] * idf_values[term]

        len_tfidf = math.sqrt(sum([value**2 for value in this_result.values()]))

        this_file = open('result/' + str(i+1) + '.txt', 'w')
        this_file.write(str(len(this_result)) + "\n")
        for term_index in sorted(this_result.keys()):
            this_file.write(str(term_index) + "\t" + str(this_result[term_index]/len_tfidf) + "\n")
        this_file.close()

def cosine(docX, docY):
    with open('result/' + str(docX) + '.txt', 'r') as file:
        contentX = file.readlines()
    xInfo = [info.strip().split() for info in contentX][1:]

    with open('result/' + str(docY) + '.txt', 'r') as file:
        contentY = file.readlines()
    yInfo = [info.strip().split() for info in contentY][1:]

    x_iter, y_iter, cosine = 0 , 0 , 0
    while x_iter < len(xInfo) and y_iter < len(yInfo):
        if int(xInfo[x_iter][0]) == int(yInfo[y_iter][0]):
            cosine += float(xInfo[x_iter][1]) * float(yInfo[y_iter][1])
            x_iter += 1
            y_iter += 1
        elif int(xInfo[x_iter][0]) > int(yInfo[y_iter][0]):
            y_iter += 1
        else:
            x_iter += 1
    return cosine

if __name__ == "__main__":
    main_function()
