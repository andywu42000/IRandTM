import math
import operator
import sys
from terms import term_generate

def main():
    label = get_label()
    vocabulary, all_term_list = get_vocabulary( label )
    print "Now training..."
    prior, condprob = train_multinomial_nb( vocabulary , all_term_list , label )
    print "Now testing..."
    argmax_score = test_multinomial_nb( vocabulary , all_term_list , label , prior , condprob )
    output_classification( argmax_score , all_term_list )
    print "Result written to r06725052.txt!"

def output_classification(argmax_score, all_term_list):
    class_result = [0]*13
    output = open('r06725052.txt', 'w')
    for docID, score_list in argmax_score.items():
        categoryID = score_list.index(max(score_list)) + 1
        class_result[categoryID-1] += 1
        output.write(str(docID) + "\t" + str(categoryID) + "\n")
    output.close()

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
        class_terms.setdefault(this_class, [])
        prior_prob[this_class] += 1
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

    print "Now feature selecting..."
    vocabulary = LLR(vocabulary, all_term_list, label, 500)

    print "Now documents terms updating..."
    new_all_term_list = {}
    for docID, term_list in all_term_list.items():
        new_all_term_list[docID] = []
        for term in term_list:
            if term in vocabulary:
                new_all_term_list[docID].append(term)

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

    for term in vocabulary:
        prob_matrix = {}
        for docID, this_class in docID_class.items():
            prob_matrix.setdefault(this_class, [0,0])
            if term in all_term_list[docID]:
                prob_matrix[this_class][0] += 1
            else:
                prob_matrix[this_class][1] += 1

        h1, h2 = .0, .0

        # Calculate H1
        term_present_count = sum([prob_matrix[i][0] for i in prob_matrix]) + 1
        term_absent_count = len(docID_class) - term_present_count + 1
        pt = float(term_present_count) / (len(docID_class) + 2)
        not_pt = 1 - pt
        h1 += math.log(pt) * term_present_count + math.log(not_pt) * term_absent_count

        # Calculate H2
        for this_class, row in prob_matrix.items():
            this_present_prob = float(row[0]) / (row[0] + row[1])
            h2 += math.log(math.pow(this_present_prob,row[0]) * math.pow(1-this_present_prob, row[1]))

        full_vocabulary_ratios[term] = -2 * (h1 - h2)

    sorted_vocabulary = sorted(full_vocabulary_ratios.items(), key=operator.itemgetter(1), reverse=True)
    return [pair[0] for pair in sorted_vocabulary[:k]]

if __name__ == "__main__":
    main()
