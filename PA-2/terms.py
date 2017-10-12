import re
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

p = PorterStemmer()

# Read stop words from stop-words.txt
stop_words_list = set(stopwords.words('english'))

regex = re.compile("[^a-zA-Z_\-0-9]")
re_alphabet = re.compile("[a-zA-Z]")
def term_generate(raw_data):

    # Tokenization and Lowercase
    token_list = []
    split_data = raw_data.lower().split()
    for s in split_data:
        raw_token = regex.sub('', s)
        if re_alphabet.search(raw_token) != None:
            token_list.append(raw_token)

    # Remove stop words
    after_removed_list = []
    for s in token_list:
        if not s in stop_words_list:
            after_removed_list.append(s)

    # Stemming by using Porter's algorithm
    result_list = []
    for s in after_removed_list:
        result_list.append(p.stem(s))

    return result_list


if __name__ == '__main__':
    with open('news.txt') as file:

        # Read the raw text and print it
        raw_data = file.read().decode("utf-8")

        result_list = term_generate(raw_data)

        # Write result to file
        file = open('result.txt','w')
        for result in result_list:
            file.write(result + '\n')
