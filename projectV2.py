import string
# Ricordarsi che per usare queste librerie nltk, bisogna installare i database, che vengono salvati in /home/thomas/nltk_data...
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

import time

stop_words = set(stopwords.words("english"))
punctuation = set(string.punctuation)
stemmer = PorterStemmer()

"""
    - Implementare il nasted dictionary -- FATTO

        {
        "term1": {
            1: [2, 5],
            2: [1, 7, 9]
        },
        "term2": {
            1: [3, 8],
            3: [2]
        },
        "term3": {
            2: [4],
            3: [1, 6]
        }
    }


    - We don't use hash table because with hash we can't look for prefixes --FATTO

    - maintaining multiple indexes can make insertion and modification more complex, 
        as you have to update both indexes. However, the tradeoff is often worth it 
        in terms of improved query performance.
        Inverted indexes are optimized for efficient querying, so it's usually 
        more important to optimize for fast search rather than fast insertion/modification.

    -  For terms with a large number of distinct postings lists, the hash table 
        can be replaced with a balanced tree to reduce the memory footprint and improve 
        lookup times.

    - my_dict = {('my_key', [1, 2]): 'my_value'}
        This will be the structure of out permuted index



"""

def permutation_word(word_original : string):
    perm = list()
    word = word_original + "$"
    perm.append(word)
    for i in range(1, len(word)):
        word_1 = word[i:]
        word_2 = word[0:i]
        word_3 = word_1 + word_2
        perm.append(word_3)
    
    return (word_original, tuple(perm))
         


class inverted_index:

    def __init__(self):
        self.inverted_index = {}
        self.permuted_index = {}
        self.n_docs_2 = 0
        self.n_docs = 0

    # def __init__(self, documents):
    #     self.inverted_index = {}
    #     for doc_id, doc in enumerate(documents):
    #         i = 0
    #         for term in word_tokenize(doc):   # also doc.split() can be used but it's difficult to caputure punctuation
    #             term = term.casefold() #lowercase, more aggressive that lower()
    #             term_split = term.split('\'')  # split apostrophe words and then save only important words
    #             for term_no_ap in term_split:
    #                 if term_no_ap not in stop_words and term_no_ap not in punctuation and term_no_ap != '': #remove stop words and punctation
    #                     term_no_ap = stemmer.stem(term_no_ap)
    #                     if self.inverted_index.get(term_no_ap) is not None:
    #                         if self.inverted_index[term_no_ap].get(doc_id) is not None:
    #                             self.inverted_index[term_no_ap][doc_id].append(i) 
    #                         else:
    #                             self.inverted_index[term_no_ap][doc_id] = [i]
    #                     else:
    #                         self.inverted_index[term_no_ap] = {}
    #                         self.inverted_index[term_no_ap][doc_id] = [i]


    #             i += 1

    #     self.n_docs = len(documents)

    def __str__(self):
        return str(self.inverted_index)

    def create_indexes(self, documents):

        for doc_id, doc in enumerate(documents):
            for term in word_tokenize(doc):   # also doc.split() can be used but it's difficult to caputure punctuation
                i = 0 #It's the position int he document of the term
                term = term.casefold() #lowercase, more aggressive that lower()
                term_split = term.split('\'')  # split apostrophe words and then save only important words
                for term_no_ap in term_split:
                    if term_no_ap not in stop_words and term_no_ap not in punctuation and term_no_ap != '': #remove stop words and punctation
                        term_no_ap = stemmer.stem(term_no_ap)
                        if self.inverted_index.get(term_no_ap) is not None:
                            if self.inverted_index[term_no_ap].get(doc_id) is not None:
                                self.inverted_index[term_no_ap][doc_id].append(i) 
                            else:
                                self.inverted_index[term_no_ap][doc_id] = [i]
                        else:
                            self.inverted_index[term_no_ap] = {}
                            self.inverted_index[term_no_ap][doc_id] = [i]


                i += 1
        self.n_docs = len(documents)

        return self.inverted_index
    
    
    def create_permuted_index(self, documents):

        for doc_id, doc in enumerate(documents):
            for term in word_tokenize(doc):
                i = 0
                term = term.casefold()
                term_split = term.split('\'')
                for term_no_ap in term_split:
                    if term_no_ap not in stop_words and term_no_ap not in punctuation and term_no_ap != '': #remove stop words and punctation
                        term_no_ap = stemmer.stem(term_no_ap)

                        # permutation process
                        tuple_key = permutation_word(term_no_ap)

                        if self.permuted_index.get(tuple_key) is not None:
                            if self.permuted_index[tuple_key].get(doc_id) is not None:

                                self.permuted_index[tuple_key][doc_id].append(i)
                            else:
                                self.permuted_index[tuple_key][doc_id] = [i]
                        else:
                            self.permuted_index[tuple_key] = {}
                            self.permuted_index[tuple_key][doc_id] = [i]

                i += 1
        self.n_docs_2 = len(documents)

        return self.permuted_index

    
    def add_doc(self, doc):

        new_doc_id = self.n_docs
        i = 0
        for term in word_tokenize(doc):
            # print(term)
            term = term.casefold() #more aggressive that lower()
            term_split = term.split('\'')  # split apostrophe words and then save only important words
            for term_no_ap in term_split:
                if term_no_ap not in stop_words and term_no_ap not in punctuation and term_no_ap != '': #remove stop words and punctation
                    term_no_ap = stemmer.stem(term_no_ap)
                    if self.inverted_index.get(term_no_ap) is not None:
                        if self.inverted_index[term_no_ap].get(new_doc_id) is not None:
                            self.inverted_index[term_no_ap][new_doc_id].append(i) 
                        else:
                            self.inverted_index[term_no_ap][new_doc_id] = [i]
                    else:
                        self.inverted_index[term_no_ap] = {}
                        self.inverted_index[term_no_ap][new_doc_id] = [i]


            i += 1        

        self.n_docs = new_doc_id + 1


    def query(self, query_string):

        # Use set intersection, union and difference because more performant 

        split_query = [stemmer.stem(term) for term in query_string.split(" ")]
        all_docs = set([d for d in range(self.n_docs)])

        if split_query[0].casefold() == "not":
            res = all_docs.difference(self.inverted_index[split_query[1]].keys())
        else:
            res = set(self.inverted_index[split_query[0]].keys())
        for i in range(len(split_query)):
            if split_query[i].lower() == "and":
                if split_query[i+1].lower() == "not":
                    not_doc = all_docs.difference(self.inverted_index[split_query[i+2]].keys())
                    res = res.intersection(not_doc)
                else:
                    res = res.intersection(self.inverted_index[split_query[i+1]].keys())

            elif split_query[i].lower() == "or":
                if split_query[i+1].lower() == "not":
                    not_doc = all_docs.difference(self.inverted_index[split_query[i+2]].keys())
                    res = res.union(not_doc)
                else:
                    res = res.union(self.inverted_index[split_query[i+1]].keys())
            
        return res
    
    
    

    def _phrase_query(self, terms):
        """
        Private method to perform a phrase query on the inverted index.
        Given a list of terms, returns a list of documents that contain all of the terms in the specified order.
        """
        docs = self.inverted_index[terms[0]]
        for term in terms[1:]:
            new_docs = {}
            postings = self.inverted_index[term]
            for doc_id, positions in postings.items():
                if doc_id in docs:
                    prev_positions = docs[doc_id]
                    new_positions = []
                    i = 0
                    j = 0
                    while i < len(prev_positions) and j < len(positions):
                        if positions[j] == prev_positions[i] + 1:
                            new_positions.append(positions[j])
                            i += 1
                            j += 1
                        elif positions[j] > prev_positions[i] + 1:
                            i += 1
                        else:
                            j += 1
                    if new_positions:
                        new_docs[doc_id] = new_positions
            docs = new_docs
        return list(docs.keys())
    
    def edit_distance(self, u, v):
        """
        Computes the Levenshtein distance between two strings.
        Returns the minimum number of insertions, deletions, and substitutions required to transform u into v.
        """
        nrows = len(u) + 1
        ncols = len(v) + 1
        M = [[0] * ncols for i in range(0, nrows)]
        for i in range(0, nrows):
            M[i][0] = i
        for j in range(0, ncols):
            M[0][j] = j
        for i in range(1, nrows):
            for j in range(1, ncols):
                candidates = [M[i-1][j] + 1, M[i][j-1] + 1]
                if u[i-1] == v[j-1]:
                    candidates.append(M[i-1][j-1])
                else:
                    candidates.append(M[i-1][j-1] + 1)
                M[i][j] = min(candidates)
        return M[-1][-1]

    def find_nearest(self, word, dictionary, keep_first=False):
        """
        Finds the closest match to a word in a dictionary using the Levenshtein distance.
        If keep_first is True, only considers words in the dictionary that start with the same letter as the word.
        """
        if keep_first:
            dictionary = list(filter(lambda w: w[0] == word[0], dictionary))
        distances = map(lambda x: self.edit_distance(word, x), dictionary) # [1, 3, 2]
        return min(zip(distances, dictionary))[1] # [(1, 'hello'), (2, ...) ] 
    
    def phrase_query_sc(self, query):
        """
        Performs a phrase query on the inverted index.
        Given a query string, returns a list of documents that contain all of the words in the specified order.
        If a word is not found in the inverted index, suggests the closest match using the Levenshtein distance.
        """
        terms = [stemmer.stem(term) for term in query.split(" ")]
        dictionary = list(self.inverted_index.keys())
        postings = []
        for term in terms:
            if term in dictionary:
                postings.append(term)
            else:
                sub = self.find_nearest(term, dictionary, keep_first=True)
                print("{} not found. Did you mean {}?".format(term, sub))
                postings.append(sub)
        
        return self._phrase_query(postings)
        

    def phrase_query(self, query):
        terms = [stemmer.stem(term) for term in query.split(" ")]
        return self._phrase_query(terms)
    



def timeit_test(fun, times):
    start = time.time()
    for i in range(times):
        fun
    end = time.time()
    finish = (end-start)/times
    return finish
    


#           MAIN

# documents = ["The cat is on the table. NAME, cat",
#             "What is the cat's name? Giuseppe Nigro",
#             "Can you pass me the hammer? I need it!",
#             "It was passed"
#             #"cliche, clichè",
#             #"color, colour"
#             ]

with open("data/lorem_ipsum", "r") as f:
    documents = [line.split("\n")[0] for line in f]
f.close()

inverted_doc = inverted_index()
inverted_doc.create_indexes(documents)
# print(inverted_doc)

new_doc = "Ehi, how it is my friend Giovanni? I like his cats"

inverted_doc.add_doc(new_doc)

# print(inverted_doc)

query = "semper AND commodo"

# print("Result of query '", query, "': ", inverted_doc.query(query))

query_phrase = "semper commodo"
# print("Result of query '",query_phrase,"': ",inverted_doc.phrase_query(query_phrase))

# print("Time for query: ", timeit_test(inverted_doc.query(query), 100000000))
# print("Time for query phrase: ", timeit_test(inverted_doc.phrase_query(query_phrase), 100000000))


query_wrong = "lorum ipsimum"
print("Result of query '",query_wrong, "': ", inverted_doc.phrase_query_sc(query_wrong))
# print("Time for query with sc: ", timeit_test(inverted_doc.phrase_query_sc(query_wrong), 100000))



new_index = inverted_index()
print(new_index.create_permuted_index(documents))

