import pickle


class PostingsFile(object):
    def __init__(self, file_name):
        self.disk_file = file_name
        self.postings = dict()

    def format_posting(self, temp_postings):
        for key, docs in temp_postings.items():
            for docId, df in docs.items():
                if key in self.postings:
                    self.postings[key].append((docId, df))
                else:
                    self.postings[key] = list()
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
        :param posting_file: postings.txt disk file
        :param offset: the offset to seek to in file
        :return: Posting list [(1, 0), (10,0)]
        """
        with open(self.disk_file, 'rb') as file:
            file.seek(offset)
            return pickle.load(file)
