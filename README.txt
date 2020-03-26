This is the README file for A0161476B-A0161401Y's submission

== Python Version ==

We're using Python Version 3.6 for this assignment.

== General Notes about this assignment ==

a) Indexing - We start off by iterating through all documents one by one. For each document, we get the tokenized sentences. For each of these sentences, we get the stemmed words. For each of the unique words, we store a document list that maintains the documents ids in which each word is found. In the indexing phase, we also compute the normalized length of each document and store it in the dictonary.
Once we have computed the document list for every term in the vocabulary we form the dictionary file by storing the term, document frequency (given by length of list) and the offset to the posting list. As mentioned before, the dictonary also keeps track of the normalized length of each document AND the number of documents N.
The posting file stores the posting/document list for each term in the vocabulary.

Algorithm:

1. For every document in corpus get all terms which are normalised and stemmed.
2. We keep track of the number of times each term appears in the document.
3. We also keep track of the number of times each term appears in the current document.
4. Using step 3, after we have processed all terms in each document, we compute the normalized length of that document.
5. We also keep track of the number of documents (N) that we have encountered.

b) Searching - Given a query, we first tokenize it using PORTER STEMMER. We then iterate through every tokenized term in the query. For each of these terms, we retrive the posting list and compute the tf-idf score for the term and each document in the posting list using lnc-ltc and store the score for each document. We then get the resultant score for each document by dividing the previous score with the normalized length of the document and the normalized query vector length.

Algorithm:

1. Open queries and output file.
2. For each query, tokenize the query to get the terms.
3. Build the vector for the tokenized query.
4. Compute the cosine similarity score for the query vector and each document vector
5. Use a heap to get the top 10 ranked documents and return this result.

== Files included with this submission ==

- index.py: To index the corpus and form dictionary and postings stored on disk
- search.py: To evaluate the results for search query and store them in output file
- dictionary.py: To store the term with its offset[of posting list] and document frequency. It also keeps track of the length of each document.
- util.py: Helper functions for getting terms, postings list, formatting, parsing and evaluating query
- dictionary.txt: To store the dictionary of the corpus in text file
- postings.txt: To store the posting lists. Each posting list contains the docId and the term frequency of the term in that document.

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

- https://towardsdatascience.com/
- Tutorial on using Pickle to load and store python data in files
- StackOverflow for Python queries

== Email ==

e0072573@u.nus.edu
e0072498@u.nus.edu
