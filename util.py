import nltk
import os
import pickle
from math import log, sqrt
import heapq

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
                terms.append(STEMMER.stem(word.lower()))

        return terms


def format_result(result):
    """
    Formats result as required for output file
    :param result: In format [1, 10]
    :return: '1 10' formatted string
    """
    formatted_res = list()
    for val in result:
        formatted_res.append(val)

    formatted_res = " ".join(map(str, formatted_res))
    return formatted_res


def query_eval(dictionary, query, posting_file):
    query_tokens = nltk.tokenize.word_tokenize(query)

    tf_query = dict()
    document_score = dict()
    for token in query_tokens:
        norm_token = STEMMER.stem(token.lower())
        if norm_token in tf_query:
            tf_query[norm_token] += 1
        else:
            tf_query[norm_token] = 1

    for token in query_tokens:
        norm_token = STEMMER.stem(token.lower())

        offset = dictionary.get_offset_of_term(norm_token)
        if offset != -1:
            postings = get_posting_list(posting_file, offset)
        else:
            postings = list()

        df = dictionary.get_df(norm_token)

        if df == 0 or df == -1:
            idf = 0
        else:
            idf = log(dictionary.get_doc_count() / df, 10)

        tf_query[norm_token] = idf * (1 + log(tf_query[norm_token], 10))

        for posting in postings:
            doc_id = posting[0]
            tf_doc = 1.0 + log(posting[1], 10)

            if doc_id not in document_score:
                document_score[doc_id] = 0
            document_score[doc_id] += tf_query[norm_token] * tf_doc

    norm_query = 0
    for term, wt in tf_query.items():
        norm_query += (wt * wt)

    norm_query = sqrt(norm_query)

    for docId, score in document_score.items():
        doc_norm_len = dictionary.get_normalised_doc_length(docId)
        document_score[docId] = score / (norm_query * doc_norm_len)

    res = heapq.nlargest(10, document_score, key=document_score.__getitem__)

    return res
