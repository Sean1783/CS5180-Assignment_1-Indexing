#-------------------------------------------------------------------------
# AUTHOR: Sean Archer
# FILENAME: title of the source file
# SPECIFICATION: description of the program
# FOR: CS 5180- Assignment #1
# TIME SPENT: how long it took you to complete the assignment
#-----------------------------------------------------------*/


#Importing some Python libraries
import csv
import math


def create_index():
    documents = []

    #Reading the data in a csv file
    with open('collection.csv', 'r') as csvfile:
      reader = csv.reader(csvfile)
      for i, row in enumerate(reader):
             if i > 0:  # skipping the header
                documents.append (row[0])

    #Conducting stopword removal for pronouns/conjunctions. Hint: use a set to define your stopwords.
    stop_words = ('the', 'to', 'and', 'a', 'They', 'her', 'I', 'She', 'their')

    #Conducting stemming. Hint: use a dictionary to map word variations to their stem.
    stemming = {'loves' : 'love',
                'dogs' : 'dog',
                'cats' : 'cat',
                }

    formatted_documents = []
    for document in documents:
        formatted_documents.append(format_document(document, stop_words, stemming))

    #Identifying the index terms.
    index_terms = set()
    for document in formatted_documents:
        index_terms = index_terms.union(create_index_terms_set(document, stop_words, stemming))

    #Building the document-term matrix by using the tf-idf weights.
    doc_term_matrix = []
    for term in index_terms:
        idf = generate_idf(formatted_documents, term)
        row = {term: []}
        for document in formatted_documents:
            tf = generate_tf(document, term)
            row[term].append(tf*idf)
        doc_term_matrix.append(row)

    #Printing the document-term matrix.
    for term in doc_term_matrix:
        print(term)


def format_document(document, stop_words, stemming_dictionary):
    split_text = document.split(' ')
    formatted_document = []

    for word in split_text:
        if word not in stop_words:
            if word in stemming_dictionary:
                formatted_document.append(stemming_dictionary[word])
            else:
                formatted_document.append(word)

    return formatted_document


def create_index_terms_set(formatted_document, stop_words, stemming_dictionary):
    document_terms = set()
    for word in formatted_document:
        if word not in stop_words:
            if word in stemming_dictionary:
                document_terms.add(stemming_dictionary[word])
            else:
                document_terms.add(word)
    return document_terms


def generate_tf(formatted_document, term):
    raw_frequency_count = 0
    for word in formatted_document:
        if word == term:
            raw_frequency_count += 1
    return raw_frequency_count / len(formatted_document)


def document_term_frequency(formatted_document, term):
    if term in formatted_document:
        return 1
    else:
        return 0


def generate_total_dtf(formatted_documents, term):
    total_dtf = 0
    for document in formatted_documents:
        total_dtf = total_dtf + document_term_frequency(document, term)
    return total_dtf


def generate_idf(formatted_documents, term):
    total_dtf = generate_total_dtf(formatted_documents, term)
    return math.log((len(formatted_documents) / total_dtf), 10)

