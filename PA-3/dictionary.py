from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import math
import re
import string


def read_files(path):
    content = ""

    with open(path, "r") as f:
        content += f.read()
        f.close()

    return content


def tokenize(content):
    # do lowercase
    content = content.lower()

    # remove \n\f\r\v\t
    content = re.sub("[\n\f\r\v\t]", "", content)

    # remove characters after '
    content = re.sub("\'[a-z]+", "", content)

    # remove numbers
    content = re.sub("[0-9]", "", content)

    # remove punctuation
    content = re.sub("[" + string.punctuation + "]", "", content)

    # split by space
    tokens = content.split()

    return tokens


def remove_stopwords(tokens):
    # read stop words
    stop_words = set(stopwords.words('english'))

    # remove stop words
    tokens = [token for token in tokens if token not in stop_words]

    return tokens


def stemming(tokens):
    p = PorterStemmer()

    # use porter algorithm to stem
    terms = sorted([p.stem(token) for token in tokens])

    return terms

def extract_terms(path):
    # extract terms from file
    content = read_files(path)
    tokens = tokenize(content)
    tokens = remove_stopwords(tokens)
    terms = stemming(tokens)

    return terms


# return dictionary whose key is class number and value is document ids
def get_training_samples():
    class_dic = {}

    with open("training.txt", "r") as f:
        training_list = f.readlines()

        for element in training_list:
            document_list = element.split(" ")

            # class number
            document_class = document_list[0]

            # document ids
            documents = document_list[1:-1]
            class_dic[document_class] = documents

    return class_dic


# save dictionary to text file
def write_result(terms):
    with open('dictionary.txt', 'w') as f:
        for term in terms:
            f.write(term + '\n')


# build a dictionary without duplicate.
def build_dictionary():
    class_dic = get_training_samples()
    documents = []
    dictionary = []

    for docs in class_dic.values():
        documents += docs

    documents = set(documents)

    for doc_id in documents:
        path = "Documents/{}.txt".format(doc_id)
        terms = extract_terms(path)

        dictionary += terms

    dictionary = list(sorted(set(dictionary)))

    # do feature selection then save to txt
    return dictionary


# concatenate class terms
def build_concatenate_class_term():
    class_term_dict = {}
    class_dict = get_training_samples()

    for class_num, docs in class_dict.items():
        class_terms = []

        for doc_id in docs:
            path = "Documents/{}.txt".format(doc_id)

            terms = extract_terms(path)
            class_terms += terms

        class_term_dict[class_num] = class_terms

    return class_term_dict


def likelihood_ratio(matrix, total_present, total_N):
    total_ratio = 0

    for element in matrix:
        present = element[0]
        absent = element[1]
        prob = element[2]
        pt = total_present/total_N

        ratio = -2*(present*math.log(pt) +
                    absent*math.log(1-pt) -
                    present*math.log(prob) -
                    absent*math.log(1-prob))

        total_ratio += ratio

    return total_ratio


def compute_likelihood_ratio():
    dictionary = build_dictionary()
    class_dic = get_training_samples()

    terms_dic = {}

    for term in dictionary:
        class_matrix = []
        total_present = 0
        total_N = 0

        for class_num, docs in class_dic.items():
            present = 1
            absent = 1

            for doc_id in docs:
                path = "Documents/{}.txt".format(doc_id)

                terms = list(sorted(set(extract_terms(path))))

                if term in terms:
                    present += 1
                else:
                    absent += 1

            total_present += present
            total_N += present + absent

            class_matrix.append([present, absent, present/15+2])


        ratio = likelihood_ratio(class_matrix, total_present, total_N)

        terms_dic[term] = ratio

    dic_list = list(sorted(terms_dic.items(), key=lambda d: d[1], reverse=True))
    dic_list_500 = dic_list[:500]

    write_result(dic_list_500)


if __name__ == "__main__":
    compute_likelihood_ratio()
