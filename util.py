import nltk
import os
import pickle

STEMMER = nltk.stem.porter.PorterStemmer()


def get_posting_list(posting_file, offset):
    """
    Gets posting list for a given offset in file
    :param posting_file: postings.txt disk file
    :param offset: the offset to seek to in file
    :return: Posting list [(1, 0), (10,0)]
    """
    with open(posting_file, 'rb') as file:
        file.seek(offset)
        return pickle.load(file)


def read_document(directory, doc):
    """
    retrieves the tokenzied/stemmed words in each document
    :param directory: of all corpus documents
    :param doc: documentId to read
    :return: all normalised terms
    """
    terms = []
    with open(os.path.join(directory, str(doc))) as in_file:
        content = in_file.read()
        sentences = nltk.tokenize.sent_tokenize(content)
        for sentence in sentences:
            words = nltk.tokenize.word_tokenize(sentence)
            for word in words:
                terms.append(STEMMER.stem(word).lower())

        return terms


def format_result(result):
    """
    Formats result as required for output file
    :param result: In format [(1, 0), (10, 0)]
    :return: '1 10' formatted string
    """
    formatted_res = list()
    for val in result:
        formatted_res.append(val[0])

    formatted_res = " ".join(map(str, formatted_res))
    return formatted_res

