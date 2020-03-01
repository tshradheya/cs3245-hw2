import nltk
import os
import pickle

STEMMER = nltk.stem.PorterStemmer()

def read_document(directory, doc):
    terms = []
    with open(os.path.join(directory, str(doc))) as in_file:
        content = in_file.read()
        sentences = nltk.tokenize.sent_tokenize(content)
        print(sentences[0])
        for sentence in sentences:
            words = nltk.tokenize.word_tokenize(sentence)
            for word in words:
                terms.append(STEMMER.stem(word.lower()))

        return terms

def process_query(query):
    # Parse
    # Convert to Postfix
    pass


def execute_query(query, dictionary, posting_file):
    # Use stack to evaluate
    # Merge for AND, OR, NOT
    res = eval_AND(posting_file, first, second)
    pass


def eval_AND(posting_file, first, second):
    pass

def get_posting_list(posting_file, offset):
    with open(posting_file, 'rb') as file:
        file.seek(offset)
        return pickle.load(file)

