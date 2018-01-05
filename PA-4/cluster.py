class Cluster:

    def __init__(self, vector_sum, documents):
        # cluster vector sum
        self.vector_sum = vector_sum

        # document ids
        self.documents = documents

        # cluster size
        self.size = len(self.documents)


