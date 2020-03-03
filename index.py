#!/usr/bin/python3
import re
import nltk
import sys
import getopt
import os
import pickle


from dictionary import Dictionary
from skippointer import SkipPointer
import util

temp_file = "temp_file.txt"
DEBUG_LIMIT = 5
ALL_DOCS = "$all_docs$"


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
    temp_dictionary[ALL_DOCS] = set()
    for document in indexing_doc_files:
        temp_dictionary[ALL_DOCS].add((document, 0))

        terms = util.read_document(in_dir, document)
        for term in terms:
            if term in temp_dictionary:
                doc_set = temp_dictionary[term]
                doc_set.add((document, 0))
            else:
                temp_dictionary[term] = set()
                temp_dictionary[term].add((document, 0))

    with open(temp_file, 'wb') as temp_posting_file:
        for token, docs_set in temp_dictionary.items():
            offset = temp_posting_file.tell()
            dictionary.add_term(token, len(docs_set), offset)
            pickle.dump(sorted(list(docs_set)), temp_posting_file)

    skipPointer = SkipPointer("ROOT_L")
    skipPointer.set_skip_for_posting_list(out_postings, temp_file, dictionary)

    dictionary.save()
    os.remove(temp_file)


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
