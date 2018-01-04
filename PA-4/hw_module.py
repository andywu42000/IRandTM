class PriorityQueue:
    def __init__(self):
        self.queue = {}

    def add(self, no, similarity):
        self.queue[no] = similarity

    def get_max(self):
        max_sim = max(self.queue.values())
        for no, sim in self.queue.items():
            if sim == max_sim:
                return no, sim
    def delete(self, i):
        self.queue[i] = 0

class Cluster:
    def __init__(self, vector_sum, this_no):
        self.s = vector_sum
        self.n = 1
        self.all_member = [this_no]

    def mergeCluster(self, cluster):
        new_vector_sum = {}
        for term, sim in self.s.items():
            new_vector_sum[term] = new_vector_sum.setdefault(term, 0.0) + sim
        for term, sim in cluster.s.items():
            new_vector_sum[term] = new_vector_sum.setdefault(term, 0.0) + sim
        self.s = new_vector_sum
        self.n += cluster.n
        self.all_member.extend(cluster.all_member)
