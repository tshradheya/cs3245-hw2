from math import sqrt
import pickle
import util

class SkipPointer(object):
    def __init__(self, rule):
        self.rule = rule

    def get_length_of_skip(self, posting_list):
        if self.rule == "ROOT_L":
            return int(sqrt(len(posting_list)))

    def set_skip_for_posting_list(self, posting_file, temp_file, dictionary):
        with open(temp_file, 'rb') as f:
            with open(posting_file, 'wb') as postings_disk:
                for term in dictionary.get_terms():
                    offset = dictionary.get_offset_of_term(term)
                    posting_list = util.get_posting_list(temp_file, offset)

                    length_of_skip = self.get_length_of_skip(posting_list)

                    temp_list = list(posting_list[0])
                    temp_list[1] = length_of_skip
                    posting_list[0] = tuple(temp_list)
                    prev = length_of_skip

                    for i in range(length_of_skip, len(posting_list), length_of_skip):
                        temp_list = list(posting_list[i])
                        temp_list[1] = length_of_skip + prev
                        posting_list[i] = tuple(temp_list)
                        prev = posting_list[i][1]

                    offset = postings_disk.tell()
                    dictionary.update_offset(term, offset)
                    pickle.dump(posting_list, postings_disk)
