import util
from math import sqrt
import pickle

class SkipPointer(object):

    def update_skip(self, posting_file, temp_file, dictionary, rule):
        with open(temp_file, 'rb') as f:
            with open(posting_file, 'wb') as postings:
                for term in dictionary.get_terms():
                    offset = dictionary.get_offset_of_term(term)
                    posting_list = util.get_posting_list(temp_file, offset)

                    length_of_skip = int(sqrt(len(posting_list)))
                    temp_list = list(posting_list[0])
                    temp_list[1] = length_of_skip
                    posting_list[0] = tuple(temp_list)

                    for i in range(1, len(posting_list)):
                        temp_list = list(posting_list[i])
                        temp_list[1] = length_of_skip + posting_list[i-1][1]
                        posting_list[i] = tuple(temp_list)

                    offset = postings.tell()
                    dictionary.update_offset(term, offset)
                    pickle.dump(posting_list, postings)
