This is the README file for A0161476B and A0161401Y's submission

== Python Version ==

We're using Python Version 3.6 for this assignment.

== General Notes about this assignment ==

Give an overview of your program, describe the important algorithms/steps 
in your program, and discuss your experiments in general.  A few paragraphs 
are usually sufficient.

== Files included with this submission ==

- index.py: To index the corpus and form dictionary and postings stored on disk
- search.py: To evaluate the results for search query and store them in output file
- dictionary.py: To store the term with its offset[of posting list] and document frequency
- skippointer.py Skip Pointer implementation to store skip pointers in each posting list with rule
- terms_eval.py: Merging algorithms for OR, NOT, AND [with skip pointer logic where possible]
- util.py: Helper functions for getting terms, postings list, formatting, parsing and evaluating query
- dictionary.txt: To store the dictionary of the corpus in text file
- posting.txt: To store the posting lists with skip pointer impl in text file

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
