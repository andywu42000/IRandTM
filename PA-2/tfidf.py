from dictionary import Dictionary
import pandas as pd
import math
import glob
from functools import reduce

class TFIDF:

    def __init__(self):
        self.dictionary = Dictionary()

        # create dictionary's dataFrame
        self.df_dict = self.dictionary.main()

        # show dataFrame's all rows in console
        pd.set_option("display.max_rows", None)

    # compute how many times each term show in document
    def tf(self, query, terms):
        return terms.count(query)

    # compute how many times each term show in document collections
    def idf(self, query, df_dict):
        return math.log(1095 / (df_dict.loc[df_dict["term"] == query, "df"].values[0]))

    # compute tf * idf
    def tfidf(self, query, terms):
        return self.tf(query, terms) * self.idf(query, self.df_dict)

    def write_file(self, path, desc, t_indexs, scores):
        with open(path, "w") as f:
            f.write(desc + "\n")
            f.write("\n")
            f.write("t_index   tfidf" + "\n" )

            for i in range(0, len(t_indexs)):
                f.write(str(t_indexs[i]) + "\t" + str(scores[i]) + "\n")

            f.close()

    def main(self):
        # load documents path
        path = "Documents/*.txt"
        paths = sorted(glob.glob(path))

        # extract document id from path
        doc_ids = list(map(lambda x: x[x.rfind("/")+1 : x.rfind(".")], paths))

        # doing for loop with documents, convert each document's content into terms
        for idx, path in enumerate(paths):
            content = self.dictionary.read_files(path)
            tokens = self.dictionary.tokenize(content)
            tokens = self.dictionary.remove_stopwords(tokens)
            terms = self.dictionary.stemming(tokens)

            # prevent from having duplicated value when creating tf-idf records
            unique_terms = sorted(set(terms))

            t_indexs = []
            scores = []

            # for each term of document, computing it's tf-idf score
            for term in unique_terms:
                # get the term's t_index in dictionary which is being computed
                t_index = self.df_dict.index[self.df_dict["term"] == term].values[0]

                # compute the tf-idf score
                tfidf_score = self.tfidf(term, terms)

                t_indexs.append(t_index)
                scores.append(tfidf_score)

            # power each element in scores to 2
            p2_scores = list(map(lambda x: x**2, scores))
            # compute normalize tfidf
            norm_score = math.sqrt(reduce(lambda x, y: x+y, p2_scores))

            scores = list(map(lambda x: x/norm_score, scores))

            # get the specific document id which is being computed
            doc_id = doc_ids[idx]

            # get the total terms count in one document
            term_count = len(t_indexs)

            desc = "The document has {} terms".format(term_count)
            txt_path = "TF-IDF/{}.txt".format(doc_id)

            self.write_file(txt_path, desc, t_indexs, scores)


if __name__ == "__main__":
    tfidf = TFIDF()
    tfidf.main()


