#!/usr/bin/python3
import sys
import getopt
from dictionary import Dictionary
import util
import time

def usage():
    print("usage: " + sys.argv[0] + " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results")

def run_search(dict_file, postings_file, queries_file, results_file):
    """
    using the given dictionary file and postings file,
    perform searching on the given queries file and output the results to a file
    """
    print('running search on the queries...')

    dictionary = Dictionary(dict_file)
    dictionary.load()

    with open(queries_file, 'r') as query_file:
        with open(results_file, 'w') as output_file:
            for query in query_file:
                if query is not None:
                    processed_query = util.reverse_polish_expression(query)
                    result = util.execute_query(processed_query, dictionary, postings_file)
                    result = util.format_result(result)
                    output_file.write(result)


dictionary_file = postings_file = file_of_queries = output_file_of_results = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o:')
except getopt.GetoptError:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-d':
        dictionary_file  = a
    elif o == '-p':
        postings_file = a
    elif o == '-q':
        file_of_queries = a
    elif o == '-o':
        file_of_output = a
    else:
        assert False, "unhandled option"

if dictionary_file == None or postings_file == None or file_of_queries == None or file_of_output == None :
    usage()
    sys.exit(2)

test = time.time()
run_search(dictionary_file, postings_file, file_of_queries, file_of_output)
print(time.time() - test)
