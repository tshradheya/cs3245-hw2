This is the README file for A0161476B-A0161401Y's submission

== Python Version ==

We're using Python Version 3.6 for this assignment.

== General Notes about this assignment ==

The assignment was done in three main parts:

a) Indexing - We start off by iterating through all documents one by one. For each document, we get the tokenized sentences.
For each of these sentences, we get the stemmed words. For each of the unique words, we store a document
list that maintains the documents ids in which each word is found. Once we have computed the document list for every
term in the vocabulary we form the dictionary file by storing the term, document frequency (given by length of list) and the offset.
We used a temporary posting file initially so that we could store the skip pointers after all the processing was done.
The posting file stores the posting/document list for each term in the vocabulary.
Each element of the document list is a tuple of <documentId, index_of_next_skip_doc>.

Algorithm:
1. For every document in corpus get all terms which are normalised and stemmed.
2. Add all terms into a temp posting list which contains `term: set() of docIds`. Also use $all_docs$ to store all docIds
3. Sort the dictionary. From this temp posting list post process to get skip indexes
4. For each term, get and store the posting list one by one getting the pointer of where it is stored and updating that in dictionary
5. Save dictionary

Format of Dictionary: {term: (docFreq, ptrPostingList)}
Format of SkipPostingList: [(docId, skipIdx)]. SkipIdx is 0 if not possible to skip



b) Searching - Given a query, we first tokenize it and then get the reverse polish notation using the Shunting yard algorithm.
We then evaluate the postfix expression to compute the result of the query. We used skip pointers to optimize when AND operation
between two terms. We also optimized the AND NOT operation by treating it as a separate case.
We did not compute NOT of a term directly. Instead, we checked if a NOT operation is followed by AND.
If so, we avoid the expensive NOT operation and iterate through the lists to perform the AND NOT operation.
Other operations very implemented in the known methods.

Algorithm:
1. Open queries and output file
2. For each query, convert to postfix expression
3. Evaluate postfix expression using AND(skip ptr is possible), OR, NOT and AND NOT(for optimisation if possible)
4. Format and store result into output file


c) Skip Pointers - We used the heuristics defined in the class. We used √L evenly spaced skip pointers in the posting list.
We stored the skip pointers in the posting list as a post-processing step. While evaluating query, skip pointer is only used
when the list is directly queried from posting list. We get posting list update the skip idx and store it back into the postings list.
We have mechanism to store, load and use skip pointers
It cant be used when a intermediate result of other terms is being evaluated.


Analysis:

1. Optimise using AND NOT: This was done by checking postfix expression and if possible it helped us reduce a lot of time.
For our test queries the time taken by eval_NOT reduced from 0.068 to 0.040  cause of AND_NOT optimisation
2. Store the skip_idx in posting list itself. This helped save memory by not adding another skiplist and has fewer seek() calls to disk
3. To make search faster we optimised code by using cProfile to find the slow parts and speeding them up.
4. Using sentence tokeniser on sentences rather than lines in files gave more representative dictionary with fewer faults
5. Skip pointers helped make our test queries faster by  7% on average
More details can be found in ESSAY.txt

== Files included with this submission ==

- index.py: To index the corpus and form dictionary and postings stored on disk
- search.py: To evaluate the results for search query and store them in output file
- dictionary.py: To store the term with its offset[of posting list] and document frequency
- skippointer.py Skip Pointer implementation to store skip pointers in each posting list with rule
- terms_eval.py: Merging algorithms for OR, NOT, AND [with skip pointer logic where possible]
- util.py: Helper functions for getting terms, postings list, formatting, parsing and evaluating query
- dictionary.txt: To store the dictionary of the corpus in text file
- posting.txt: To store the posting lists with skip pointer impl in text file

- README.txt: The file you are looking at which gives a overview
- ESSAY.txt: File containing succinct answers to some questions

== Statement of individual work ==

Please put a "x" (without the double quotes) into the bracket of the appropriate statement.

[x] We, A0161476B and A0161401Y, certify that we have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, we
expressly vow that we have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.

== References ==

- Shunting Yard Algorithm [http://www.martinbroadhurst.com/shunting-yard-algorithm-in-python.html]
- Tutorial on using Pickle to load and store python data in files
- StackOverflow for Python queries

== Email ==

e0072573@u.nus.edu
e0072498@u.nus.edu

