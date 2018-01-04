from terms import term_generate
import math
from hw_module import PriorityQueue, Cluster
N = 1095

def main():
    vocabulary, doc_term_count, term_docID_dict = get_data()
    doc_tfidf = calculate_tfidf(doc_term_count, term_docID_dict)
    gaac(doc_tfidf, [20, 13, 8])

def get_data():
    doc_term_count = []
    term_docID_dict = {}
    vocabulary = set()
    for i in range(1, N+1):
        term_count = {}
        with open("IRTM/" + str(i) + ".txt", "r") as input_file:
            raw_data = input_file.read().decode("utf-8")
            news_terms = term_generate(raw_data)
            for term in news_terms:
                term_docID_dict.setdefault(term, []).append(i)
                term_count[term] = term_count.setdefault(term, 0) + 1
                vocabulary.add(term)
        doc_term_count.append(term_count)
    '''
    for term_count in doc_term_count:
        for term in vocabulary:
            term_count.setdefault(term, 0)
    '''
    return vocabulary, doc_term_count, term_docID_dict

def calculate_tfidf(doc_term_count, term_docID_dict):
    doc_tfidf = []
    idf_values = {}
    for term, doc_list in term_docID_dict.items():
        idf_values[term] = math.log(float(N) / len(set(doc_list)), 10)
    for term_count in doc_term_count:
        raw_tfidf = {}
        for term, count in term_count.items():
            raw_tfidf[term] = count * idf_values[term]

        len_tfidf = math.sqrt(sum([value**2 for value in raw_tfidf.values()]))

        normalized_tfidf = {}
        for term in raw_tfidf:
            normalized_tfidf[term] = raw_tfidf[term] / len_tfidf

        doc_tfidf.append(normalized_tfidf)

    return doc_tfidf

def gaac(doc_tfidf, K_list):
    K_list = sorted(K_list, reverse=True)

    cluster_list = []
    for i in range(0, N):
        cluster_list.append(Cluster(doc_tfidf[i], i+1))

    C = {}
    for i, clusterX in enumerate(cluster_list[:-1]):
        C[i+1] = PriorityQueue()
        j = i + 1
        for clusterY in cluster_list[i+1:]:
            C[i+1].add(j+1, sim_ga(clusterX, clusterY))
            j += 1

    cluster_count = sum(1 if cluster != None else 0 for cluster in cluster_list)
    while (cluster_count is not 1 and len(K_list) is not 0):
        max_X_no, max_Y_no = get_max_sim_pair(C)
        clusterX, clusterY = cluster_list[max_X_no-1], cluster_list[max_Y_no-1]
        clusterX.mergeCluster(clusterY)

        # Delete clusterY record in C
        for i in range(1, max_Y_no):
            if C[i] == None:
                continue
            else:
                C[i].delete(max_Y_no)
        C[max_Y_no] = None
        # Remove this cluster from cluster list
        cluster_list[max_Y_no-1] = None

        # Add new clusterX record to C
        for i in range(1, max_X_no):
            if C[i] == None:
                continue
            else:
                C[i].add(max_X_no, sim_ga(clusterX, cluster_list[i-1]))
        j = max_X_no + 1
        for clusterZ in cluster_list[max_X_no:]:
            if clusterZ == None:
                j += 1
                continue
            else:
                C[max_X_no].add(j, sim_ga(clusterX, clusterZ))
                j += 1
        cluster_count = sum(1 if cluster != None else 0 for cluster in cluster_list)

        if cluster_count == K_list[0]:
            output_result(cluster_count, cluster_list)
            del K_list[0]
        print cluster_count

def output_result(K, cluster_list):
    output_file = open(str(K)+".txt", "w")
    for cluster in cluster_list:
        if cluster != None:
            for clusterNo in cluster.all_member:
                output_file.write(str(clusterNo) + "\n")
            output_file.write("\n")
    output_file.close()

def get_max_sim_pair(C):
    max_X_no, max_Y_no, max_sim = 0, 0, 0
    for clusterNo in C:
        if C[clusterNo] == None:
            continue
        this_no, this_sim = C[clusterNo].get_max()
        #print this_no, this_sim
        if this_sim > max_sim:
            max_sim = this_sim
            max_X_no = clusterNo
            max_Y_no = this_no
    #print max_X_no, max_Y_no, max_sim
    return max_X_no, max_Y_no

def sim_ga(clusterX, clusterY):
    total_vector_sum = {}
    for term, tfidf in clusterX.s.items():
        total_vector_sum[term] = total_vector_sum.setdefault(term, 0.0) + tfidf
    for term, tfidf in clusterY.s.items():
        total_vector_sum[term] = total_vector_sum.setdefault(term, 0.0) + tfidf
    similarity = sum([value**2 for value in total_vector_sum.values()])
    num = clusterX.n + clusterY.n
    similarity = float( similarity - num ) / ( num * (num-1) )
    return similarity

if __name__ == "__main__":
    main()
