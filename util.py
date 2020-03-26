import nltk
import os
from math import log, sqrt
import heapq

STEMMER = nltk.stem.porter.PorterStemmer()

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

def query_eval(query, dictionary, postings):

    query_tokens = nltk.tokenize.word_tokenize(query)

    tf_query = dict()
    document_score = dict()
    query_norm_tokens = list()
    total_docs = dictionary.get_doc_count()

    for token in query_tokens:
        query_norm_tokens.append(STEMMER.stem(token.lower()))

    for norm_token in query_norm_tokens:
        if norm_token in tf_query:
            tf_query[norm_token] += 1
        else:
            tf_query[norm_token] = 1

    for norm_token in query_norm_tokens:

        offset = dictionary.get_offset_of_term(norm_token)
        if offset != -1:
            posting_list = postings.get_posting_list(offset)
        else:
            posting_list = list()

        df = dictionary.get_df(norm_token)

        if df == 0 or df == -1:
            idf = 0
        else:
            idf = log(total_docs / df, 10)

        tf_query[norm_token] = idf * (1 + log(tf_query[norm_token], 10))

        for posting in posting_list:
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

    return heapq.nlargest(10, document_score, key=document_score.__getitem__)



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
