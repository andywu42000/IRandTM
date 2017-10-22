# !/usr/local/bin/python3
# -*- coding: utf-8 -*-
import os
from process_content import (
    clear_content, stem, generate_term_list)


DOCUMENT_DIRECTORY = "documents/"
DICTIONARY_FILEPATH = "result/dictionary.txt"


def prepare_content(directory):
    """Read all documents and do pre processing."""
    content = []
    for filename in sorted(
            os.listdir(directory),
            key=lambda filename: int(filename.replace(".txt", ""))):
        file = open(directory + filename, "r", encoding="utf-8")
        content.append(file.read())
        file.close()

    cleared_content = clear_content(content)
    return cleared_content


def generate_dictionary(term_list, content_list):
    """Generate df value for each term."""
    term_df_list = []
    for index, term in enumerate(term_list, start=1):
        df = 0
        for content in content_list:
            if term in content:
                df += 1
        term_df_list.append((index, term, df))

    return term_df_list


# Generate term list
cleared_content = prepare_content(DOCUMENT_DIRECTORY)
term_list = generate_term_list(" ".join(cleared_content))

# Process documents and generate dictionary
processed_content = []
for content in cleared_content:
    content = content.split(" ")
    processed_content.append(" ".join(stem(content)))
term_df_list = generate_dictionary(term_list, processed_content)

# Write dictionary.txt
dict_file = open(DICTIONARY_FILEPATH, "w", encoding="utf-8")
for term_df in term_df_list:
    dict_file.write(
        '{0[0]:<10}{0[1]:<30}{0[2]:<10}\n'.format(term_df))
dict_file.close()
