# !/usr/local/bin/python3
# -*- coding: utf-8 -*-
import numpy as np


DOC_DIRECTORY = "result/"


def _read_doc(filename):
    data_list = []
    with open(DOC_DIRECTORY + filename) as file:
        next(file)  # skip the first line
        for line in file:
            data_list.append(float(line.strip().split()[1]))

    return np.asarray(data_list)


def cosine(doc_index_1, doc_index_2):
    """Calculate cosine value of two docs."""
    doc1_filename = "Doc{}.txt".format(str(doc_index_1 + 1))
    doc2_filename = "Doc{}.txt".format(str(doc_index_2 + 1))

    doc1_vector = _read_doc(doc1_filename)
    doc2_vector = _read_doc(doc2_filename)

    normalized_doc1 = doc1_vector / np.linalg.norm(doc1_vector)
    normalized_doc2 = doc2_vector / np.linalg.norm(doc2_vector)

    cosine_value = np.dot(normalized_doc1, normalized_doc2)
    return cosine_value
