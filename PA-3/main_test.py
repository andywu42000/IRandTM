import math
import operator
import sys
from random import shuffle
from terms import term_generate

def main():
    '''
    label = get_label()
    vocabulary, all_term_list = get_vocabulary(label)
    print "Now Training..."
    prior, condprob = train_multinomial_nb( vocabulary , all_term_list , label )
    print "Now Testing..."
    argmax_score = test_multinomial_nb( vocabulary , all_term_list , label , prior , condprob )
    output_classification(argmax_score)
    print "Result written to output.txt!"
    '''

    origin_label, shuffled_docs = valid_get_label()
    while len(shuffled_docs) != 0:
        test_data = {}
        label = origin_label.copy()
        for i in range(0,20):
            if len(shuffled_docs) != 0:
                this_doc = shuffled_docs.pop()
                test_data[this_doc] = label.pop(this_doc)
            else:
                break
        vocabulary, all_term_list = get_vocabulary(label)
    #print "Now Training..."
        prior, condprob = train_multinomial_nb( vocabulary , all_term_list , label )
    #print "Now Testing..."
        argmax_score = test_multinomial_nb( vocabulary , all_term_list , label , prior , condprob )
        valid_classification(argmax_score, test_data)
    #output_classification(argmax_score)
    #print "Result written to output.txt!"

def valid_get_label():
    class_data = {}
    test_data = {}
    with open( 'training.txt' , 'r' ) as class_file :
        for line in class_file :
            this_class = line.split()
            for doc in this_class[1:] :
                class_data[ int(doc) ] = int(this_class[0])
    shuffled_docs = class_data.keys()
    shuffle(shuffled_docs)

    return class_data, shuffled_docs

def valid_classification(argmax_score, test_data):
    accuracy = 0
    counter = 0
    for docID, score_list in argmax_score.items():
        categoryID = score_list.index(max(score_list)) + 1
        if docID in test_data.keys():
            counter += 1
            if categoryID == test_data[docID]:
                accuracy += 1
            print docID, categoryID, test_data[docID]
    print float(accuracy) / counter * 100

def output_classification(argmax_score):
    class_result = [0]*13
    output = open('output.txt', 'w')
    for docID, score_list in argmax_score.items():
        categoryID = score_list.index(max(score_list)) + 1
        class_result[categoryID-1] += 1
        output.write(str(docID) + "\t" + str(categoryID) + "\n")
    output.close()

    for i in range(1,14):
        sys.stdout.write("{:4} ".format(i))
    sys.stdout.write("\n")
    for class_no in class_result:
        sys.stdout.write("{:4} ".format(class_no))
    sys.stdout.write("\n")

def test_multinomial_nb(vocabulary, all_term_list, label, prior, condprob):
    argmax_score = {}
    class_count = len(prior)
    for docID in all_term_list:
        if docID not in label.keys():
            this_doc_score = [0] * class_count
            for this_class in range(1, class_count+1):
                this_doc_score[this_class-1] += math.log(prior[this_class])
                for term in all_term_list[docID]:
                    this_doc_score[this_class-1] += math.log(condprob[this_class][term])
            argmax_score[docID] = this_doc_score

    return argmax_score

def train_multinomial_nb(vocabulary, all_term_list, docID_class):
    prior_prob, cond_prob = {}, {}
    class_terms = {}
    train_docs_count = len(docID_class)

    # Calculate prior_prob and collect class's terms
    for docID, this_class in docID_class.items():
        prior_prob.setdefault(this_class, 0)
        prior_prob[this_class] += 1
        class_terms.setdefault(this_class, [])
        for term in all_term_list[docID]:
            class_terms[this_class].append(term)
    for this_class in prior_prob:
        prior_prob[this_class] = float(prior_prob[this_class]) / train_docs_count

    # Calculate cond_prob
    for this_class, terms_in_class in class_terms.items():
        terms_count = len(terms_in_class)
        this_class_prob = {}
        for term in vocabulary:
            this_class_prob[term] = 0
        for term in terms_in_class:
            this_class_prob[term] += 1
        for term in this_class_prob:
            this_class_prob[term] = float(this_class_prob[term]+1) / ( terms_count + len(vocabulary) )
        cond_prob[this_class] = this_class_prob

    return prior_prob, cond_prob

def get_vocabulary(label):
    vocabulary = set()
    all_term_list = {}
    for i in range(1, 1096):
        sys.stdout.write('\r')
        sys.stdout.write("File reading progress: {:.2f}%".format(float(i)/1095*100))
        sys.stdout.flush()
        with open("IRTM/" + str(i) + ".txt") as input_data:
            raw_data = input_data.read().decode("utf-8")
            all_term_list[i] = term_generate(raw_data)
            if i in label.keys():
                for term in all_term_list[i]:
                    vocabulary.add(term)
    sys.stdout.write('\n')

    print "Now fearture selecting..."
    vocabulary = LLR(vocabulary, all_term_list, label, 500)
    #vocabulary = list(vocabulary)
    print "Now documents terms updating..."
    new_all_term_list = {}
    for docID, term_list in all_term_list.items():
        new_all_term_list[docID] = []
        for term in term_list:
            if term in vocabulary:
                new_all_term_list[docID].append(term)

    for i in range(0,len(vocabulary)):
        print i+1, vocabulary[i]

    return vocabulary, new_all_term_list

def get_label():
    class_data = {}
    with open( 'training.txt' , 'r' ) as class_file :
        for line in class_file :
            this_class = line.split()
            for doc in this_class[1:] :
                class_data[ int(doc) ] = int(this_class[0])
    return class_data

def LLR(vocabulary, all_term_list, docID_class, k):
    full_vocabulary_ratios = {}
    chi_vocabulary_ratios = {}
    tokens_count = 0

    for docID in all_term_list:
        tokens_count += len(all_term_list[docID])

    for term in vocabulary:
        prob_matrix = {}
        for docID, this_class in docID_class.items():
            prob_matrix.setdefault(this_class, [0,0])
            for this_term in all_term_list[docID]:
                if this_term == term:
                    prob_matrix[this_class][0] += 1
                else:
                    prob_matrix[this_class][1] += 1

        h1, h2 = .0, .0

        # Calculate H1
        term_present_count = sum([prob_matrix[i][0] for i in prob_matrix]) + 1
        term_absent_count = tokens_count - term_present_count + 1
        pt = float(term_present_count) / (tokens_count + 2)
        not_pt = 1 - pt
        h1 += math.log(pt) * term_present_count + math.log(not_pt) * term_absent_count

        this_chi_value = 0.0
        # Calculate H2 and chi-square
        for this_class, row in prob_matrix.items():
            Ep = float(term_present_count * (row[0] + row[1])) / tokens_count
            Enp = float(term_absent_count * (row[0] + row[1])) / tokens_count
            this_chi_value += (row[0] - Ep)**2 / Ep
            this_chi_value += (row[1] - Enp)**2 / Enp

            this_present_prob = float(row[0]+1) / (row[0] + row[1]+1)
            h2 += math.log(this_present_prob) * row[0] + math.log(1-this_present_prob) * row[1]
            #temp = math.pow(this_present_prob,row[0]) * math.pow(1-this_present_prob, row[1])
            #h2 += math.log(temp)

        full_vocabulary_ratios[term] = -2 * (h1 - h2)
        chi_vocabulary_ratios[term] = this_chi_value

    sorted_vocabulary = sorted(full_vocabulary_ratios.items(), key=operator.itemgetter(1), reverse=True)
    return [pair[0] for pair in sorted_vocabulary[:k]]

if __name__ == "__main__":
    main()
