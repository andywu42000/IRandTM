import numpy as np
from cluster import Cluster

DOCUMENT_COUNT = 1095
TERM_DIM = 14168

# read document tfidf vector
def read_doc_vector():
    doc_vector = {}

    for i in range(1, DOCUMENT_COUNT+1):
        path = "TFIDF/{}.txt".format(i)

        f = open(path, "r")
        content = f.readlines()
        vector = list(map(lambda x: float(x.strip("\n")), content))

        doc_vector[i] = vector

    return doc_vector


# compute group-average similarity
def ga_similarity(cluster1, cluster2):
    total_vector_sum = cluster1.vector_sum + cluster2.vector_sum

    numerator = (total_vector_sum.dot(total_vector_sum)) - (cluster1.size + cluster2.size)
    denominator = (cluster1.size + cluster2.size)*(cluster1.size + cluster2.size - 1)

    if denominator == 0:
        return 0
    else:
        return numerator / denominator


# write clusters into text
def write_file(indexs, clusters, cluster_num):
    with open("{}.txt".format(cluster_num), "w") as w:

        for index in indexs:
            cluster = clusters[index]
            documents = list(sorted(cluster.documents))

            for doc in documents:
                w.write(str(doc) + "\n")

            w.write("\n")

        w.close()


# do hierarchical agglomerative clustering
def hac():
    print("=========read document vector========")
    # {doc_id : vector}
    doc_vector = read_doc_vector()
    # metrix with similarity
    similarity_map = np.zeros((DOCUMENT_COUNT, DOCUMENT_COUNT))
    # {num, Cluster}
    clusters = {}
    # 1 is available, 0 is not available
    availables = [1 for i in range(DOCUMENT_COUNT)]

    print("=================start building map=================")

    # DOCUMENT_COUNT+1
    for i in range(1, DOCUMENT_COUNT + 1):
        for j in range(1, DOCUMENT_COUNT + 1):
            cluster1 = Cluster(np.array(doc_vector[i]), [i])
            cluster2 = Cluster(np.array(doc_vector[j]), [j])

            similarity = ga_similarity(cluster1, cluster2)

            similarity_map[i - 1][j - 1] = similarity

        clusters[i - 1] = cluster1

    for i in range(1, DOCUMENT_COUNT + 1):
        similarity_map[i - 1][i - 1] = 0

    np.save("similarity_map.npy", similarity_map)

    print("similarity_map", similarity_map)

    print("=================start clustering=================")

    # do clustering, N-1 because internal node = external node - 1
    for k in range(1, DOCUMENT_COUNT):
        print("***** clustering step {} *****".format(k))
        row, column = np.unravel_index(similarity_map.argmax(), similarity_map.shape)

        small = min(row, column)
        big = max(row, column)

        small_cluster = clusters[small]
        big_cluster = clusters[big]
        new_cluster = Cluster(small_cluster.vector_sum + big_cluster.vector_sum,
                              small_cluster.documents + big_cluster.documents)
        zero_cluster = Cluster(np.zeros((TERM_DIM,)), [])

        clusters[small] = new_cluster
        clusters[big] = zero_cluster

        for n in range(1, DOCUMENT_COUNT + 1):
            # new similarity
            similarity_map[small][n - 1] = ga_similarity(new_cluster, clusters[n - 1])
            similarity_map[n - 1][small] = ga_similarity(new_cluster, clusters[n - 1])

            # make big column and row become negative
            similarity_map[big][n - 1] = 0
            similarity_map[n - 1][big] = 0

            # make self similarity 0
            similarity_map[n - 1][n - 1] = 0

        availables[big] = 0

        # 20 clusters
        if k == DOCUMENT_COUNT - 20:
            print("=================write 20 cluster file=================")

            indexs = [i for i, j in enumerate(availables) if j == 1]

            write_file(indexs, clusters, 20)

        # 13 clusters
        if k == DOCUMENT_COUNT - 13:
            print("=================write 13 cluster file=================")

            indexs = [i for i, j in enumerate(availables) if j == 1]

            write_file(indexs, clusters, 13)

        # 8 clusters
        if k == DOCUMENT_COUNT - 8:
            print("=================write 8 cluster file=================")

            indexs = [i for i, j in enumerate(availables) if j == 1]

            write_file(indexs, clusters, 8)


if __name__ == "__main__":
    hac()

