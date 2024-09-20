#-------------------------------------------------------------------------
# AUTHOR: Sean Archer
# FILENAME: indexing.py
# SPECIFICATION: Creates and displays the document-term matrix for a set of documents.
# FOR: CS 5180- Assignment #1
# TIME SPENT: 6 hours.
#-----------------------------------------------------------*/


import csv
import math


def create_index():
    documents = []

    with open('collection.csv', 'r') as csvfile:
      reader = csv.reader(csvfile)
      for i, row in enumerate(reader):
             if i > 0:  # skipping the header
                documents.append (row[0])

    stop_words = ('the', 'to', 'and', 'a', 'They', 'her', 'I', 'She', 'their')

    stemming = {'loves' : 'love',
                'cats': 'cat',
                'dogs' : 'dog'
                }

    transformed_document_collection = transform_document_collection(documents, stop_words, stemming)
    terms = []
    create_index_terms_list(transformed_document_collection, terms)

    docTermMatrix = [[] for _ in range(len(documents))]

    for term in terms:
        idf = generate_idf(transformed_document_collection, term)
        doc_index = 0
        for document in transformed_document_collection:
            tf = generate_tf(document, term)
            tf_idf = tf*idf
            docTermMatrix[doc_index].append(round(tf_idf, 3))
            doc_index += 1

    document_titles = ["d" + str(i+1) for i in range(len(documents))]
    print_2d_table(terms, document_titles, docTermMatrix)


def print_2d_table(terms, doc_titles, data):
    col_width = max(len(str(item)) for row in [terms] + data for item in row) + 4
    row_label_width = max(len(str(label)) for label in doc_titles) + 4
    print(" " * row_label_width + "".join(f"{header:<{col_width}}" for header in terms))
    for i, row_label in enumerate(doc_titles):
        row = f"{row_label:<{row_label_width}}" + "".join(f"{item:<{col_width}}" for item in data[i])
        print(row)


def create_index_terms_list(transformed_doc_collection, index_list):
    for document in transformed_doc_collection:
        for term in document:
            if term not in index_list:
                index_list.append(term)


def transform_document(document, stop_word_set, stem_map):
    source_document = document.split(' ')
    transformed_document = []
    for i in range(len(source_document)):
        if source_document[i] not in stop_word_set:
            if source_document[i] in stem_map:
                transformed_document.append(stem_map[source_document[i]])
            else:
                transformed_document.append(source_document[i])
    return transformed_document


def transform_document_collection(documents, stemming, stop_words):
    transformed_collection = []
    for document in documents:
        transformed_collection.append(transform_document(document, stemming, stop_words))
    return transformed_collection


def generate_tf(transformed_document, term):
    raw_frequency_count = 0
    for word in transformed_document:
        if word == term:
            raw_frequency_count += 1
    return raw_frequency_count / len(transformed_document)


def document_term_frequency(transformed_document, term):
    if term in transformed_document:
        return 1
    else:
        return 0


def generate_total_dtf(transformed_documents, term):
    total_dtf = 0
    for document in transformed_documents:
        total_dtf = total_dtf + document_term_frequency(document, term)
    return total_dtf


def generate_idf(transformed_documents, term):
    total_dtf = generate_total_dtf(transformed_documents, term)
    return math.log((len(transformed_documents) / total_dtf), 10)
