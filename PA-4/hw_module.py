class PriorityQueue:
    def __init__(self):
        self.queue = []
        self.no_index_map = {}

    def add(self, no, similarity):
        self.queue.append([no, similarity])
        self.no_index_map[no] = len(self.queue)
        self.filter_up(len(self.queue))

    def filter_up(self, index):
        parent_index, current_index = index/2, index
        while parent_index > 0 and self.queue[parent_index-1][1] < self.queue[current_index-1][1]:
            current_no, parent_no = self.queue[current_index-1][0], self.queue[parent_index-1][0]
            self.no_index_map[current_no], self.no_index_map[parent_no] = parent_index, current_index
            self.queue[current_index-1], self.queue[parent_index-1] = self.queue[parent_index-1], self.queue[current_index-1]
            current_index = parent_index
            parent_index = current_index / 2

    def filter_down(self, index):
        current_index, left_child_index, right_child_index = index, index*2, index*2+1
        while left_child_index <= len(self.queue):
            current, left = self.queue[current_index-1][1], self.queue[left_child_index-1][1]
            if right_child_index <= len(self.queue):    # has right child
                right = self.queue[right_child_index-1][1]
                max_value = max(current, left, right)
                if max_value == left:
                    current_no, left_no = self.queue[current_index-1][0], self.queue[left_child_index-1][0]
                    self.no_index_map[current_no], self.no_index_map[left_no] = left_child_index, current_index
                    self.queue[current_index-1], self.queue[left_child_index-1] = self.queue[left_child_index-1], self.queue[current_index-1]
                    current_index = left_child_index
                    left_child_index, right_child_index = current_index*2, current_index*2+1
                elif max_value == right:
                    current_no, right_no = self.queue[current_index-1][0], self.queue[right_child_index-1][0]
                    self.no_index_map[current_no], self.no_index_map[right_no] = right_child_index, current_index
                    self.queue[current_index-1], self.queue[right_child_index-1] = self.queue[right_child_index-1], self.queue[current_index-1]
                    current_index = right_child_index
                    left_child_index, right_child_index = current_index*2, current_index*2+1
                else:
                    break
            else:   # only left child
                if left > current:
                    current_no, left_no = self.queue[current_index-1][0], self.queue[left_child_index-1][0]
                    self.no_index_map[current_no], self.no_index_map[left_no] = left_child_index, current_index
                    self.queue[current_index-1], self.queue[left_child_index-1] = self.queue[left_child_index-1], self.queue[current_index-1]
                    current_index = left_child_index
                    left_child_index, right_child_index = current_index*2, current_index*2+1
                else:
                    break

    def get_max(self):
        if len(self.queue) > 0:
            return self.queue[0]
        else:
            return 0, 0

    def update(self, No, similarity):
        index = self.no_index_map[No]
        self.queue[index-1][1] = similarity
        self.heapify(index)

    def delete(self, No):
        index = self.no_index_map[No]
        del self.no_index_map[No]
        self.queue[index-1] = self.queue[-1]
        self.no_index_map[self.queue[index-1][0]] = index
        self.queue.pop()
        if index <= len(self.queue):
            self.heapify(index)

    def heapify(self, index):
        parent_index = index / 2
        if parent_index > 0 and self.queue[parent_index-1][1] < self.queue[index-1][1]:
            self.filter_up(index)
        else:
            self.filter_down(index)

class Cluster:
    def __init__(self, vector_sum, this_no):
        self.s = vector_sum
        self.n = 1
        self.all_member = [this_no]

    def mergeCluster(self, cluster):
        new_vector_sum = {}
        for term, sim in self.s.items():
            new_vector_sum[term] = sim
        for term, sim in cluster.s.items():
            new_vector_sum[term] = new_vector_sum.setdefault(term, 0.0) + sim
        self.s = new_vector_sum
        self.n += cluster.n
        self.all_member.extend(cluster.all_member)
