import glob
import re
import string
import collections
import pandas as pd
from porter_stemmer import PorterStemmer


class Dictionary:

    def __init__(self):
        self.dict = {}

    def read_files(self, path):
        content = ""

        with open(path, "r") as f:
            content += f.read()
            f.close()

        return content

    def tokenize(self, content):
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

    def remove_stopwords(self, tokens):
        # read stop words
        with open("stop_words.txt", "r") as f:
            stop_words = f.read().split("\n")
            f.close()

        # remove stop words
        tokens = [token for token in tokens if token not in stop_words]

        return tokens

    def stemming(self, tokens):
        p = PorterStemmer()

        # use porter algorithm to stem
        terms = sorted([p.stem(token, 0, len(token) - 1) for token in tokens])

        return terms

    def construct_dictionary(self, terms):
        # remove duplicate terms
        set_terms = set(terms)

        # create term dictionary
        for term in set_terms:
            self.dict.setdefault(term, 0)
            self.dict[term] += 1

        # sorted dict by keys
        self.dict = collections.OrderedDict(sorted(self.dict.items()))

    def convert_to_dataFrame(self, dict):
        # convert dict to dataFrame
        df_dict = pd.DataFrame(list(dict.items()), columns=["term", "df"])
        df_dict.index += 1

        return df_dict

    def write_result(self, df):
        # save dictionary to text file
        df.to_csv("dictionary.txt", sep=" ", header=True, index=True, index_label="t_index")

    def main(self):
        path = "Documents/*.txt"

        for path in sorted(glob.glob(path)):
            content = self.read_files(path)
            tokens = self.tokenize(content)
            tokens = self.remove_stopwords(tokens)
            terms = self.stemming(tokens)
            self.construct_dictionary(terms)

        df_dict = self.convert_to_dataFrame(self.dict)

        return df_dict



if __name__ == "__main__":
    dictionary = Dictionary()
    df_dict = dictionary.main()
    dictionary.write_result(df_dict)