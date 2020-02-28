import pickle

class Dictionary(object):
    def __init__(self, disk_file):
        self.terms = {}
        self.offset_index = {}
        self.disk_file = disk_file

    def get_terms(self):
        return self.terms

    def save(self):
        with open(self.disk_file, 'w') as f:
            pickle.dump(self.terms, f)

    def load(self):
        with open(self.disk_file) as f:
            self.terms = pickle.load(f)
