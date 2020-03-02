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
        if (query_token not in OPERATORS and (query_token not in BRACKETS)):
            postfix_expression.append(STEMMER.stem(query_token).lower())
        elif query_token == 'NOT':
            temp_stack.append(query_token)
        elif query_token == 'AND':
            while (len(temp_stack) > 0 and temp_stack[-1] == 'NOT'):
                postfix_expression.append(temp_stack.pop())
            temp_stack.append(query_token)        
        elif query_token == 'OR':
            while (len(temp_stack) > 0 and (temp_stack[-1] == 'NOT' or temp_stack[-1] == 'AND')):
                postfix_expression.append(temp_stack.pop())
            temp_stack.append(query_token)    
        elif query_token == '(':
            temp_stack.append(query_token)
        else:
            while (len(temp_stack) > 0 and (temp_stack[-1] != '(')):
                postfix_expression.append(temp_stack.pop())
            temp_stack.pop()           

    while (len(temp_stack) > 0):
        postfix_expression.append(temp_stack.pop())


    print(postfix_expression)
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
                intermediate_result = eval_NOT(term)
            elif token == 'AND':
                first = operands.pop()
                second = operands.pop()
                intermediate_result = eval_AND(posting_file, first, second)
            elif token == 'OR':
                first = operands.pop()
                second = operands.pop()
                intermediate_result = eval_OR(posting_file, first, second)
            operands.append(intermediate_result)    

                            
    final_result = operands.pop()
    print(final_result)
    return final_result                          

def eval_NOT(posting_file, first):
    pass    

def eval_OR(posting_file, first, second):
    pass 

def eval_AND(posting_file, first, second):
    pass

def get_posting_list(posting_file, offset):
    with open(posting_file, 'rb') as file:
        file.seek(offset)
        return pickle.load(file)

reverse_polish_expression("bill OR Gates AND (vista OR XP) AND NOT mac")
