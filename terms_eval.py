import util
from math import sqrt

ALL_DOCS = "$all_docs$"

def eval_NOT(posting_file, dictionary, first):
    result = list()
    if isinstance(first, str):
        first_offset = dictionary.get_offset_of_term(first)
        first_list = util.get_posting_list(posting_file, first_offset)
    else:
        first_list = first

    all_docs_offset = dictionary.get_offset_of_term(ALL_DOCS)
    all_docs_list = util.get_posting_list(posting_file, all_docs_offset)

    idx_f = 0
    idx_s = 0

    len_first_list = len(first_list)
    len_all_docs_list = len(all_docs_list)

    while idx_f < len_first_list and idx_s < len_all_docs_list:
        first_doc_id = first_list[idx_f][0]
        second_doc_id = all_docs_list[idx_s][0]
        if first_doc_id == second_doc_id:
            idx_f += 1
            idx_s += 1
        else:
            result.append(all_docs_list[idx_s])
            idx_s += 1
    while idx_s < len_all_docs_list:
        result.append(all_docs_list[idx_s])
        idx_s += 1

    return result

def eval_OR(posting_file, dictionary, first, second):
    result = list()

    if isinstance(first, str):
        first_offset = dictionary.get_offset_of_term(first)
        first_list = util.get_posting_list(posting_file, first_offset)
    else:
        first_list = first

    if isinstance(second, str):
        second_offset = dictionary.get_offset_of_term(second)
        second_list = util.get_posting_list(posting_file, second_offset)
    else:
        second_list = second

    idx_f = 0
    idx_s = 0

    len_first_list = len(first_list)
    len_second_list = len(second_list)

    while idx_f < len_first_list and idx_s < len_second_list:
        first_doc_id = first_list[idx_f][0]
        second_doc_id = second_list[idx_s][0]
        if first_doc_id == second_doc_id:
            result.append(first_list[idx_f])
            idx_f += 1
            idx_s += 1
        elif first_doc_id < second_doc_id:
            result.append(first_list[idx_f])
            idx_f += 1
        else:
            result.append(second_list[idx_s])
            idx_s += 1

    while idx_f < len_first_list:
        result.append(first_list[idx_f])
        idx_f += 1

    while idx_s < len_second_list:
        result.append(second_list[idx_s])
        idx_s += 1

    return result

def eval_AND(posting_file, dictionary, first, second):
    result = list()

    if not isinstance(first, str) and not isinstance(second, str):
        result = eval_AND_Lists(first, second)
    elif isinstance(first, str) and not isinstance(second, str):
        offset = dictionary.get_offset_of_term(first)
        term_list = util.get_posting_list(posting_file, offset)
        result = eval_AND_List_And_Term(second, term_list)
    elif not isinstance(first, str) and isinstance(second, str):
        offset = dictionary.get_offset_of_term(second)
        term_list = util.get_posting_list(posting_file, offset)
        result = eval_AND_List_And_Term(first, term_list)
    else:

        first_offset = dictionary.get_offset_of_term(first)
        first_list = util.get_posting_list(posting_file, first_offset)

        second_offset = dictionary.get_offset_of_term(second)
        second_list = util.get_posting_list(posting_file, second_offset)

        idx_f = 0
        idx_s = 0

        len_first_list = len(first_list)
        len_second_list = len(second_list)

        while idx_f < len_first_list and idx_s < len_second_list:
            first_doc_id = first_list[idx_f][0]
            second_doc_id = second_list[idx_s][0]

            first_skip_idx = first_list[idx_f][1]
            second_skip_idx = second_list[idx_s][1]
            if first_doc_id == second_doc_id:
                result.append(first_list[idx_f])
                idx_f += 1
                idx_s += 1
            elif first_doc_id < second_doc_id:
                if first_skip_idx != 0 and first_skip_idx < len_first_list and first_list[first_skip_idx][0] <= second_doc_id:
                    idx_f = first_skip_idx
                else:
                    idx_f += 1
            else:
                if second_skip_idx != 0 and second_skip_idx < len_second_list and second_list[second_skip_idx][0] <= first_doc_id:
                    idx_s = second_skip_idx
                else:
                    idx_s += 1

    return result

def eval_AND_Lists(first_list, second_list):
    result = list()
    idx_f = 0
    idx_s = 0

    len_first_list = len(first_list)
    len_second_list = len(second_list)

    skip_first_list = int(sqrt(len_first_list))
    skip_second_list = int(sqrt(len_second_list))

    while idx_f < len_first_list and idx_s < len_second_list:
        first_doc_id = first_list[idx_f][0]
        second_doc_id = second_list[idx_s][0]

        first_skip_idx = idx_f + skip_first_list
        second_skip_idx = idx_s + skip_second_list
        if first_doc_id == second_doc_id:
            result.append(first_list[idx_f])
            idx_f += 1
            idx_s += 1
        elif first_doc_id < second_doc_id:
            if first_skip_idx != 0 and first_skip_idx < len_first_list and first_list[first_skip_idx][0] <= second_doc_id:
                idx_f = first_skip_idx
            else:
                idx_f += 1
        else:
            if second_skip_idx != 0 and second_skip_idx < len_second_list and second_list[second_skip_idx][0] <= first_doc_id:
                idx_s = second_skip_idx
            else:
                idx_s += 1

    return result


def eval_AND_List_And_Term(res_list, term_list):
    result = list()
    idx_f = 0
    idx_s = 0

    len_res_list = len(res_list)
    len_term_list = len(term_list)

    while idx_f < len_res_list and idx_s < len_term_list:
        first_doc_id = res_list[idx_f][0]
        second_doc_id = term_list[idx_s][0]

        skip_ptr = term_list[idx_s][1]
        if first_doc_id == second_doc_id:
            result.append(res_list[idx_f])
            idx_f += 1
            idx_s += 1
        elif first_doc_id < second_doc_id:
            idx_f += 1
        else:
            if skip_ptr != 0 and skip_ptr < len_term_list and term_list[skip_ptr][0] <= first_doc_id:
                idx_s = skip_ptr
            else:
                idx_s += 1

    return result


def eval_AND_NOT(posting_file, dictionary, first, second):
    """
    first AND NOT second
    :param posting_file: posting.txt
    :param dictionary: Dictionary object in memory
    :param first: first postings list
    :param second: second postings list
    :return: merged list
    """
    result = list()

    if not isinstance(first, str) and not isinstance(second, str):
        result = eval_AND_NOT_Lists(first, second)
    elif isinstance(first, str) and not isinstance(second, str):
        offset = dictionary.get_offset_of_term(first)
        term_list = util.get_posting_list(posting_file, offset)
        result = eval_AND_NOT_Lists(term_list, second)
    else:
        if isinstance(first, str):
            first_offset = dictionary.get_offset_of_term(first)
            first_list = util.get_posting_list(posting_file, first_offset)
        else:
            first_list = first

        second_offset = dictionary.get_offset_of_term(second)
        second_list = util.get_posting_list(posting_file, second_offset)

        idx_f = 0
        idx_s = 0

        len_first_list = len(first_list)
        len_second_list = len(second_list)

        while idx_f < len_first_list and idx_s < len_second_list:
            first_doc_id = first_list[idx_f][0]
            second_doc_id = second_list[idx_s][0]

            skip_ptr = second_list[idx_s][1]
            if first_doc_id == second_doc_id:
                idx_f += 1
                idx_s += 1
            elif first_doc_id < second_doc_id:
                result.append(first_list[idx_f])
                idx_f += 1
            else:
                if skip_ptr != 0 and skip_ptr < len_second_list and second_list[skip_ptr][0] <= first_doc_id:
                    idx_s = skip_ptr
                else:
                    idx_s += 1

        while idx_f < len_first_list:
            result.append(first_list[idx_f])
            idx_f += 1

    return result


def eval_AND_NOT_Lists(first_list, second_list):
    result = list()
    idx_f = 0
    idx_s = 0

    len_first_list = len(first_list)
    len_second_list = len(second_list)

    skip_second_list = int(sqrt(len_second_list))

    while idx_f < len_first_list and idx_s < len_second_list:
        first_doc_id = first_list[idx_f][0]
        second_doc_id = second_list[idx_s][0]

        second_skip_idx = idx_s + skip_second_list
        if first_doc_id == second_doc_id:
            idx_f += 1
            idx_s += 1
        elif first_doc_id < second_doc_id:
            result.append(first_list[idx_f])
            idx_f += 1
        else:
            if second_skip_idx != 0 and second_skip_idx < len_second_list and second_list[second_skip_idx][0] <= first_doc_id:
                idx_s = second_skip_idx
            else:
                idx_s += 1

    while idx_f < len_first_list:
        result.append(first_list[idx_f])
        idx_f += 1

    return result
