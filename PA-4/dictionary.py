from porter_stemmer import PorterStemmer
import math
import re
import string

DOCUMENT_COUNT = 1095

# read files
def read_files(path):
    content = ""

    with open(path, "r") as f:
        content += f.read()
        f.close()

    return content


# do tokeninze
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


# remove stop words
def remove_stopwords(tokens):
    # read stop words
    with open("stop_words.txt", "r") as f:
        stop_words = f.read().split("\n")
        f.close()

    tokens = [token for token in tokens if token not in stop_words]

    return tokens


# use porter algorithm to stem
def stemming(tokens):
    p = PorterStemmer()

    terms = sorted([p.stem(token, 0, len(token) - 1) for token in tokens])

    return terms


# extract terms from file
def extract_terms(path):
    content = read_files(path)
    tokens = tokenize(content)
    tokens = remove_stopwords(tokens)
    terms = stemming(tokens)

    return terms


# read document frequency text
def read_df():
    with open("df.txt", "r") as f:
        df = {}

        content = f.readlines()
        df_list = list(map(lambda x: x.strip("\n").split("\t"), content))

        for element in df_list:
            df[element[0]] = int(element[1])

    return df


def tf(query, terms):
    return terms.count(query)


def idf(query, dictionary):
    return math.log(DOCUMENT_COUNT / int(dictionary[query]))


# compute tf-idf value
def tfidf(query, terms, dictionary):
    return tf(query, terms) * idf(query, dictionary)


# generate total dictionary of 1095 documents
def gen_dictionary():
    content = ""

    for i in range(1, DOCUMENT_COUNT+1):
        path = "Documents/{}.txt".format(i)
        content += read_files(path)

    tokens = tokenize(content)
    tokens = remove_stopwords(tokens)
    terms = stemming(tokens)

    return terms


# generate tfidf_vector to represent document
def gen_tfidf_vector():
    dictionary = gen_dictionary()
    dictionary = list(sorted(set(dictionary)))
    df = read_df()

    for i in range(1, DOCUMENT_COUNT+1):
        doc_tfidf = []

        path = "Documents/{}.txt".format(i)
        content = read_files(path)
        tokens = tokenize(content)
        tokens = remove_stopwords(tokens)
        doc_terms = stemming(tokens)
        doc_terms = list(sorted(doc_terms))

        for term in dictionary:
            if term in doc_terms:
                value = tfidf(term, doc_terms, df)
                doc_tfidf.append(value)
            else:
                doc_tfidf.append(0)

        square_sum = math.sqrt(sum(map(lambda x: x**2, doc_tfidf)))
        doc_tfidf = list(map(lambda x: x/square_sum, doc_tfidf))

        w = open("TFIDF/{}.txt".format(i), "w")

        for i in range(len(doc_tfidf)):
            w.write(str(doc_tfidf[i]) + "\n")

        w.close()


if __name__ == "__main__":
    gen_tfidf_vector()