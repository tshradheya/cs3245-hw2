import nltk
import os
import pickle

STEMMER = nltk.stem.PorterStemmer()

def read_document(directory, doc):
    terms = []
    with open(os.path.join(directory, str(doc))) as in_file:
        content = in_file.read()
        sentences = nltk.tokenize.sent_tokenize(content)
        for sentence in sentences:
            words = nltk.tokenize.word_tokenize(sentence)
            for word in words:
                terms.append(STEMMER.stem(word.lower()))

        return terms

def reverse_polish_expression(query):
    # Parse
    # Convert to Postfix
    query_tokens = nltk.tokenize.word_tokenize(query)
    # print(tokens)
    postfix_expression = []
    temp_stack = []
    OPERATORS = ['NOT', 'AND', 'OR']
    BRACKETS = ['(', ')']

    for query_token in query_tokens:
        if query_token not in OPERATORS and (query_token not in BRACKETS):
            postfix_expression.append(STEMMER.stem(query_token).lower())
        elif query_token == 'NOT':
            temp_stack.append(query_token)
        elif query_token == 'AND':
            while len(temp_stack) > 0 and temp_stack[-1] == 'NOT':
                postfix_expression.append(temp_stack.pop())
            temp_stack.append(query_token)        
        elif query_token == 'OR':
            while len(temp_stack) > 0 and (temp_stack[-1] == 'NOT' or temp_stack[-1] == 'AND'):
                postfix_expression.append(temp_stack.pop())
            temp_stack.append(query_token)    
        elif query_token == '(':
            temp_stack.append(query_token)
        else:
            while len(temp_stack) > 0 and (temp_stack[-1] != '('):
                postfix_expression.append(temp_stack.pop())
            temp_stack.pop()           

    while len(temp_stack) > 0:
        postfix_expression.append(temp_stack.pop())

    # print(postfix_expression)
    return postfix_expression

def execute_query(query, dictionary, posting_file):
    # Use stack to evaluate
    # Merge for AND, OR, NOT
    OPERATORS = ['NOT', 'AND', 'OR']
    operands = []

    for token in query:
        if token not in OPERATORS:
            operands.append(token)

        elif len(operands) > 0:
            intermediate_result = []
            if token == 'NOT':
                term = operands.pop()
                intermediate_result = eval_NOT(posting_file, dictionary, term)
            elif token == 'AND':
                first = operands.pop()
                second = operands.pop()
                intermediate_result = eval_AND(posting_file, dictionary, first, second)
            elif token == 'OR':
                first = operands.pop()
                second = operands.pop()
                intermediate_result = eval_OR(posting_file, dictionary, first, second)
            operands.append(intermediate_result)    

    final_result = operands.pop()
    # print(final_result)
    return final_result                          

def eval_NOT(posting_file, dictionary, first):
    result = list()
    if isinstance(first, str):
        first_offset = dictionary.get_offset_of_term(first)
        first_list = get_posting_list(posting_file, first_offset)
    else:
        first_list = first

    all_docs_offset = dictionary.get_offset_of_term("$all_docs$")
    all_docs_list = get_posting_list(posting_file, all_docs_offset)

    idx_f = 0
    idx_s = 0

    while idx_f < len(first_list) and idx_s < len(all_docs_list):
        f = first_list[idx_f][0]
        s = all_docs_list[idx_s][0]
        if f == s:
            idx_f += 1
            idx_s += 1
        else:
            result.append(all_docs_list[idx_s])
            idx_s += 1

    while idx_s < len(all_docs_list):
        result.append(all_docs_list[idx_s])
        idx_s += 1

    return result

def eval_OR(posting_file, dictionary, first, second):
    result = list()

    if isinstance(first, str):
        first_offset = dictionary.get_offset_of_term(first)
        first_list = get_posting_list(posting_file, first_offset)
    else:
        first_list = first

    if isinstance(second, str):
        second_offset = dictionary.get_offset_of_term(second)
        second_list = get_posting_list(posting_file, second_offset)
    else:
        second_list = second

    idx_f = 0
    idx_s = 0

    while idx_f < len(first_list) and idx_s < len(second_list):
        f = first_list[idx_f][0]
        s = second_list[idx_s][0]
        if f == s:
            result.append(first_list[idx_f])
            idx_f += 1
            idx_s += 1
        elif f < s:
            idx_f += 1
            result.append(first_list[idx_f])
        else:
            idx_s += 1
            result.append(second_list[idx_s])

    while idx_f < len(first_list):
        result.append(first_list[idx_f])
        idx_f += 1

    while idx_s < len(second_list):
        result.append(second_list[idx_s])
        idx_s += 1

    return result

def eval_AND(posting_file, dictionary, first, second):
    result = list()

    if isinstance(first, str):
        first_offset = dictionary.get_offset_of_term(first)
        first_list = get_posting_list(posting_file, first_offset)
    else:
        first_list = first

    if isinstance(second, str):
        second_offset = dictionary.get_offset_of_term(second)
        second_list = get_posting_list(posting_file, second_offset)
    else:
        second_list = second

    idx_f = 0
    idx_s = 0

    while idx_f < len(first_list) and idx_s < len(second_list):
        f = first_list[idx_f][0]
        s = second_list[idx_s][0]
        if f == s:
            result.append(first_list[idx_f])
            idx_f += 1
            idx_s += 1
        elif f < s:
            idx_f += 1
        else:
            idx_s += 1

    return result

def format_result(result):
    print(result)
    formatted_res = list()
    for val in result:
        formatted_res.append(val[0])

    formatted_res = " ".join(map(str, formatted_res)) + "\n"
    return formatted_res

def get_posting_list(posting_file, offset):
    with open(posting_file, 'rb') as file:
        file.seek(offset)
        return pickle.load(file)
