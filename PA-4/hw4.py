import numpy as np
import os
from priority_queue import Heap
from cluster import Cluster
from doc_processor import get_doc_vectors


DOC_NUM = 1095


def write_result_file(file_name, clusters):
    file = open('result/{name}.txt'.format(name=file_name), 'w', encoding='utf-8')
    for cluster in clusters:
        for doc_idx in cluster:
            file.write(str(doc_idx) + '\n')
        file.write('\n')
    file.close()


def get_similarity(cluster_1, cluster_2):
    """ By Centroid Clustering """
    sim = np.linalg.norm(cluster_1.centroid - cluster_2.centroid)

    return sim


def stop(cluster_num, avail_list):
    clusters = avail_list.count(1)

    if cluster_num < clusters:
        return False
    else:
        return True


def get_avail_index(avail_list):
    a_list = []
    for idx, avail in enumerate(avail_list):
        if avail == 1:
            a_list.append(idx)
    return a_list


def HAC_clustering(cluster_num, docs):
    # initialize
    print(">>>>> initialize ...")
    num = cluster_num
    avail_list = []
    cluster_list = []
    temp_cluster_list = []
    history = []
    cluster_matrix = []

    for i in range(DOC_NUM):
        cluster_matrix.append([])
        sim_list = []
        for j in range(DOC_NUM):
            sim_value = np.linalg.norm(np.array(docs[i]) - np.array(docs[j]))
            cluster_matrix[i].append(sim_value)
            if i != j:  # remove self
                sim_list.append((j, sim_value))

        c = Cluster(docs[i], i, sim_list)
        cluster_list.append(c)
        avail_list.append(1)

    # clustering
    print(">>>>> clustering ...")
    for k in range(DOC_NUM - 1):
        a_list = get_avail_index(avail_list)

        # find which to merge
        distances = [[idx, cluster_list[idx].get_most_sim()] for idx in a_list]
        distances = sorted(distances, key=lambda L: L[1][0])
        k_1 = distances[0][0]
        k_2 = distances[0][1][1]
        history.append((k_1, k_2))
        print('history: ', (k_1, k_2))

        # update value
        avail_list[k_2] = 0
        cluster_k_1 = cluster_list[k_1]
        cluster_k_1.merge(cluster_list[k_2])
        cluster_k_1.pri_queue.clear()

        # update similarity
        for a_idx in a_list:
            if a_idx != k_1 and a_idx != k_2:
                cluster = cluster_list[a_idx]
                cluster.pri_queue.delete(k_1)
                cluster.pri_queue.delete(k_2)
                similarity = get_similarity(cluster, cluster_k_1)
                cluster.pri_queue.insert((k_1, similarity))
                cluster_k_1.pri_queue.insert((a_idx, similarity))

        if stop(cluster_num, avail_list):
            break

        if cluster_k_1.size > DOC_NUM / (num - 3):
            avail_list[k_1] = 0
            temp_cluster_list.append(sorted(cluster_k_1.doc_indices))
            cluster_num -= 1

    # organize
    final_a_list = get_avail_index(avail_list)
    final_clusters = []

    for c_idx in final_a_list:
        final_clusters.append(sorted(cluster_list[c_idx].doc_indices))

    for c in temp_cluster_list:
        final_clusters.append(c)

    return history, final_clusters


if __name__ == '__main__':
    if not os.path.exists('result'):
        os.makedirs('result')

    docs = get_doc_vectors('documents/')

    for num in [8, 13, 20]:
        history, clustering_result = HAC_clustering(num, docs)
        write_result_file(str(num), clustering_result)
