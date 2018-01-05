class PriorityQueue:
    def __init__(self):
        self.queue = []

    def add(self, no, similarity):
        self.queue.append([no, similarity])
        self.filter_up(len(self.queue))

    def filter_up(self, index):
        parent_index = index / 2
        current_index = index
        while parent_index > 0 and self.queue[parent_index-1][1] < self.queue[current_index-1][1]:
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
                if max_value is left:
                    self.queue[current_index-1], self.queue[left_child_index-1] = self.queue[left_child_index-1], self.queue[current_index-1]
                    current_index = left_child_index
                    left_child_index, right_child_index = current_index*2, current_index*2+1
                elif max_value is right:
                    self.queue[current_index-1], self.queue[right_child_index-1] = self.queue[right_child_index-1], self.queue[current_index-1]
                    current_index = right_child_index
                    left_child_index, right_child_index = current_index*2, current_index*2+1
                else:
                    break
            else:   # only left child
                if left > current:
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
        index = 0
        for pair in self.queue:
            index += 1
            if pair[0] is No:
                break
        self.queue[index-1][1] = similarity
        self.heapify(index)

    def delete(self, No):
        index = 0
        flag = False
        for pair in self.queue:
            index += 1
            if pair[0] == No:
                flag = True
                break
        if flag == False:
            raise Error()
        self.queue[index-1] = self.queue[-1]
        self.queue.pop()
        if index <= len(self.queue):
            self.heapify(index)

    def heapify(self, index):
        parent_index = index / 2
        #print parent_index, index, len(self.queue)
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
