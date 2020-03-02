import pickle

class Dictionary(object):
    def __init__(self, disk_file):
        self.terms = {}
        self.disk_file = disk_file

    def get_terms(self):
        return self.terms

    def add_term(self, term, docFreq, offset):
        self.terms[term] = [docFreq, offset]

    def get_offset_of_term(self, term):
        if term in self.terms:
            return self.terms[term][1]
        else:
            return -1

    def save(self):
        with open(self.disk_file, 'wb') as f:
            pickle.dump(self.terms, f)

    def load(self):
        with open(self.disk_file, 'rb') as f:
            self.terms = pickle.load(f)
