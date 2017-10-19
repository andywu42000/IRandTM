from dictionary import Dictionary
import numpy as np
import time

class Vector_Space:

    def __init__(self):
        # create dictionary's dataFrame
        self.dict_index = self.build_dictionary_index()

    def build_dictionary_index(self):
        d = Dictionary()

        # create dictionary's dataFrame
        df_dict = d.main()

        # drop df column, only left t_index and term columns
        df_dict = df_dict.drop("df", axis=1)

        return df_dict

    # read the original document text
    def read_document(self, path):
        with open(path, "r") as f:
            content = f.read()
            f.close()

        return content

    # read the tf-idf vector text
    def read_tfidf_document(self, path):
        with open(path, "r") as f:
            # read the file line by line
            content = f.readlines()

            # remove the top three lines in content
            content = content[3:]

            # fetch each element's t_index and tf-idf score
            tfidf_list = sorted([idx[5:].strip().split() for idx in content])
            f.close()

        return tfidf_list

    # build the vector for the original document text
    def build_document_vector(self, doc):
        d = Dictionary()

        # tokenize, remove stop words, stem
        tokens = d.tokenize(doc)
        tokens = d.remove_stopwords(tokens)
        terms = set(d.stemming(tokens))

        # create an initial vector whose values are 0
        vector = [0] * self.dict_index.count().values[0]

        for term in terms:
            # find the index in dict_index whose term equals to the word,
            # and then set the vector[index] value to 1
            vector[self.dict_index[self.dict_index["term"] == term].index.values[0]] += 1

        return vector

    # build the vector for the td-idf vector text
    def build_tfidf_vector(self, tfidf_list):
        # create an initial vector whose values are 0
        vector = [0] * self.dict_index.count().values[0]

        for element in tfidf_list:
            # set the vector's value whose index equals to t_index to 1
            t_index = int(element[0])
            tfidf_score = float(element[1])

            vector[t_index] += tfidf_score

        return vector

    # compute cosine similarity
    def cosine_similarity(self, vector1, vector2):
        # cosine = (V1 * V2) / | | V1 | | x | | V2 | |
        score = np.dot(vector1, vector2) / (abs(np.linalg.norm(vector1)) * abs(np.linalg.norm(vector2)))

        return score

    # compute cosine similarity between two original document text
    def cosine_document(self, doc1, doc2):
        content1 = vs.read_document(doc1)
        content2 = vs.read_document(doc2)

        # create content1's vector
        vector1 = self.build_document_vector(content1)

        # create content2's vector
        vector2 = self.build_document_vector(content2)

        # compute cosine similarity between vector1 and vector2
        score = self.cosine_similarity(vector1, vector2)

        print(score)

    # compute cosine similarity between two tf-idf vector text
    def cosine(self, doc1, doc2):
        tfidf_list1 = self.read_tfidf_document(doc1)
        tfidf_list2 = self.read_tfidf_document(doc2)

        # create tfidf_list1's vector
        vector1 = self.build_tfidf_vector(tfidf_list1)

        # create tfidf_list2's vector
        vector2 = self.build_tfidf_vector(tfidf_list2)

        # compute cosine similarity between vector1 and vector2
        score = self.cosine_similarity(vector1, vector2)

        print(score)


if __name__ == "__main__":
    doc1_path = "Documents/1.txt"
    doc2_path = "Documents/2.txt"

    tfidf1_path = "TF-IDF/1005.txt"
    tfidf2_path = "TF-IDF/1003.txt"

    print(time.strftime("%Y/%m/%d %H:%M:%S"), ' ---Done!')
    vs = Vector_Space()

    # vs.cosine_document(doc1_path, doc2_path)
    vs.cosine(tfidf1_path, tfidf2_path)
    print(time.strftime("%Y/%m/%d %H:%M:%S"), ' ---Done!')