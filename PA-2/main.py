import nltk
import sys
import os
import math
from terms import term_generate

document_count = 1095

def main_function():
    idf_values = {}
    doc_tfidf = []

    # Go over all document and get:
    print "=== Document reading start ==="
    dictionary = {}         # term -> docID
    doc_word_count = []     # list of dict for knowing terms in every doc
    for i in range(1, document_count+1):
        with open('IRTM/' + str(i) + '.txt') as file:
            raw_data = file.read().decode("utf-8")
            term_generate_list = term_generate(raw_data)
            word_count = {}
            for term in term_generate_list:
                dictionary.setdefault(term, []).append(i)
                word_count[ term ] = word_count.setdefault(term, 0) + 1
            doc_word_count.append(word_count)
        progress_show(i)
    print "\n=== Document reading end ===\n"

    dict_ordered_keys = sorted(dictionary)  # sorted term -> docID

    term_id_mapping = {}
    for i, term in enumerate(dict_ordered_keys):
        term_id_mapping[term] = i + 1

    # Iterate all terms and write to dictionary.txt and calculate idf value
    dict_file = open('dictionary.txt', 'w')
    for i, term in enumerate(dict_ordered_keys):
        this_df = len(set(dictionary[term]))
        dict_file.write('{:8}{:25}{}\n'.format( str(i+1), term, str(this_df)))
        idf_values[term] = math.log(document_count / this_df, 10)
    dict_file.close()

    # check if dir 'result' exist
    if not os.path.exists('result'):
        os.makedirs('result')

    # Calculate for every doc's tfidf
    print "===== TF-IDF start ====="
    for i, word_count in enumerate(doc_word_count):
        term_tfidf = {}
        for term in word_count.keys():
            term_index = term_id_mapping[term]
            term_tfidf[term_index] = word_count[term] * idf_values[term]

        len_tfidf = math.sqrt(sum([value**2 for value in term_tfidf.values()]))

        this_file = open('result/' + str(i+1) + '.txt', 'w')
        this_file.write(str(len(term_tfidf)) + "\n")
        for term_index in sorted(term_tfidf.keys()):
            this_file.write("{:10s}{:s}\n".format(str(term_index), str(term_tfidf[term_index]/len_tfidf)))
        this_file.close()
        progress_show(i+1)
    sys.stdout.write("\n===== TF-IDF end =====\n")

def progress_show(current_index):
    sys.stdout.write('\r')
    sys.stdout.write("Current progress: {:.2f}%".format(float(current_index)/document_count*100))
    sys.stdout.flush()

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
