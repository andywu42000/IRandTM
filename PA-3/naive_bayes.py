from functools import reduce
import dictionary
import math


def read_dictionary():
    with open("dictionary.txt", "r") as f:
        data = f.readlines()
        dictionary = list(map(lambda x: x.split(",")[0].strip("'()"), data))

    return dictionary


def concatenate_all_term(docs):
    concatenate_terms = []

    for doc_id in docs:
        path = "Documents/{}.txt".format(doc_id)

        terms = dictionary.extract_terms(path)
        concatenate_terms += terms

    return concatenate_terms


def train_multinomialNB():
    train_docs_count = 195
    vocabulary = read_dictionary()
    class_dic = dictionary.get_training_samples()

    prior_prob = {}
    cond_prob = {}

    for class_num, docs in class_dic.items():
        term_prob = {}

        prior_prob[class_num] = len(docs) / train_docs_count

        concatenate_terms = concatenate_all_term(docs)
        class_term_count = len(concatenate_terms)

        for term in vocabulary:
            tf = concatenate_terms.count(term)
            term_prob[term] = (tf + 1) / (class_term_count + len(vocabulary))

        cond_prob[class_num] = term_prob

    return prior_prob, cond_prob


def apply_multinomialNB(doc_id, prior_prob, cond_prob):
    vocabulary = read_dictionary()
    path = "Documents/{}.txt".format(doc_id)

    terms = dictionary.extract_terms(path)
    terms = [term for term in terms if term in vocabulary]

    score = {}

    for i in range(1, 14):
        class_num = str(i)

        score[class_num] = math.log(prior_prob[class_num])

        for term in terms:
            score[class_num] += math.log(cond_prob[class_num][term])

    return max(score, key=score.get)


if __name__ == "__main__":
    total_docs = [str(x) for x in range(1, 1096)]
    class_dic = dictionary.get_training_samples()

    training_docs = list(sorted(reduce(lambda x, y: x + y, [x[1] for x in class_dic.items()])))
    testing_docs = [str(x) for x in total_docs if x not in training_docs]

    prior_prob, cond_prob = train_multinomialNB()

    with open("R06725027.txt", "w") as f:
        for doc_id in testing_docs:
            doc_class = apply_multinomialNB(doc_id, prior_prob, cond_prob)
            f.write(doc_id + "\t" + str(doc_class) + "\n")
