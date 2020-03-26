import pickle
from collections import defaultdict


class PostingsFile(object):
    def __init__(self, file_name):
        self.disk_file = file_name
        self.postings = defaultdict(list)

    def format_posting(self, temp_postings):
        for key, docs in temp_postings.items():
            for docId, df in docs.items():
                self.postings[key].append((docId, df))

    def save(self, dictionary):
        with open(self.disk_file, 'wb') as posting_file:
            for token, docs_list in sorted(self.postings.items()):
                offset = posting_file.tell()
                dictionary.add_term(token, len(docs_list), offset)
                pickle.dump(sorted(docs_list), posting_file)
        posting_file.close()

    def get_postings(self):
        return self.postings

    def get_posting_list(self, offset):
        """
        Gets posting list for a given offset in file
        :param offset: the offset to seek to in file
        :return: Posting list with TF [(1, 5), (10, 4)]
        """
        with open(self.disk_file, 'rb') as file:
            file.seek(offset)
            return pickle.load(file)

