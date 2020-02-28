import pickle

class Postings(object):
    """
    Class for Posting List for terms
    """
    def __init__(self, disk_file):
        self.postings_list = []
        self.disk_file = disk_file
