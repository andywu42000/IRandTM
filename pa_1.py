from porter_stemmer import PorterStemmer

# Read news from English_News.txt
with open("English_News.txt", "r") as news:

    # Lowercase news and split by space
    raw_data = news.read().lower().split()
    news.close()


# Remove , and . from raw_data
symbols = [",", "."]
token_list = list(map(lambda word: "".join(map(lambda symbol: symbol if symbol not in symbols else "", word)), raw_data))


# Remove characters after ' from token
token_list = list(map(lambda x: x[:x.index("'")] if "'" in x else x, token_list))


# Read stop words from Stop_Words.txt
with open("Stop_Words.txt", "r") as words:
    stop_words = words.read().split("\n")
    words.close()


# Remove stop words
none_stop_words_list = [x for x in token_list if x not in stop_words]


# Use Porter Algorithm to stem
porter_stemmer = PorterStemmer()
results = list(map(lambda word: porter_stemmer.stem(word, 0, len(word)-1), none_stop_words_list))


# Save result to result.txt
with open("result.txt", "w") as output:
    for result in results:
        output.write(result + ",\n")
    output.close()