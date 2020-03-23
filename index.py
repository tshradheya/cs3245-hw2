#!/usr/bin/python3
import re
import nltk
import sys
import getopt
import os
import pickle

from dictionary import Dictionary
import util


def usage():
    print("usage: " + sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file")

def build_index(in_dir, out_dict, out_postings):
    """
    build index from documents stored in the input directory,
    then output the dictionary file and postings file
    """
    print('indexing...')

    indexing_doc_files = sorted(map(int, os.listdir(in_dir)))
    dictionary = Dictionary(out_dict)

    temp_dictionary = dict()
    # For each document get the terms and add it into the temporary in-memory posting lists
    for document in indexing_doc_files:

        terms = util.read_document(in_dir, document)
        tf_for_doc = dict()

        for term in terms:
            if term in tf_for_doc:
                tf_for_doc[term] += 1
            else:
                tf_for_doc[term] = 1

            matched = False
            if term in temp_dictionary:
                doc_list = temp_dictionary[term]
                for x in doc_list:
                    if x[0] == document:
                        temp_dictionary[term].remove(x)
                        temp_dictionary[term].append((x[0], x[1] + 1))
                        matched = True
                        break
                if not matched:
                    temp_dictionary[term].append((document, 1))
            else:
                temp_dictionary[term] = list()
                temp_dictionary[term].append((document, 1))

        dictionary.add_normalised_doc_length(document, tf_for_doc)
        dictionary.add_doc_count()

    # Save dictionary on disk by getting offset in postings file
    with open(out_postings, 'wb') as posting_file:
        for token, docs_list in sorted(temp_dictionary.items()):
            offset = posting_file.tell()
            dictionary.add_term(token, len(docs_list), offset)
            pickle.dump(sorted(docs_list), posting_file)

    dictionary.save()

input_directory = output_file_dictionary = output_file_postings = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-i': # input directory
        input_directory = a
    elif o == '-d': # dictionary file
        output_file_dictionary = a
    elif o == '-p': # postings file
        output_file_postings = a
    else:
        assert False, "unhandled option"

if input_directory == None or output_file_postings == None or output_file_dictionary == None:
    usage()
    sys.exit(2)

build_index(input_directory, output_file_dictionary, output_file_postings)
