from dictionary import Dictionary

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

    # read the tf-idf vector text
    def read_tfidf_document(self, path):
        with open(path, "r") as f:
            # read the file line by line
            content = f.readlines()

            # remove the top three lines in content
            content = content[4:]

            # fetch each element's t_index and tf-idf score
            tfidf_list = sorted([idx.strip("\n").split("\t") for idx in content], key=lambda x: int(x[0]))
            # sorted(dictionary.items(), key=operator.itemgetter(0))

            f.close()
        return tfidf_list

    # compute cosine similarity between two tf-idf vector text
    def cosine(self, doc1, doc2):
        tfidf_list1 = self.read_tfidf_document(doc1)
        tfidf_list2 = self.read_tfidf_document(doc2)

        score = 0.0

        i = 0
        j = 0

        while i < len(tfidf_list1) and j < len(tfidf_list2):
            t_index1 = int(tfidf_list1[i][0])
            t_index2 = int(tfidf_list2[j][0])

            tfidf1 = float(tfidf_list1[i][1])
            tfidf2 = float(tfidf_list2[j][1])

            if t_index1 < t_index2:
                i += 1
                continue

            if t_index2 < t_index1:
                j += 1
                continue

            if t_index1 == t_index2:
                score += tfidf1 * tfidf2
                i += 1
                j += 1
                continue

        return score


if __name__ == "__main__":

    tfidf1_path = "TF-IDF/1.txt"
    tfidf2_path = "TF-IDF/2.txt"

    vs = Vector_Space()

    score = vs.cosine(tfidf1_path, tfidf2_path)
    print(score)
