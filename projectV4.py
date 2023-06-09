import time
from indexV4 import Index
import pickle
from cisi import CISI
import numpy as np
import pandas as pd


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

    - my_dict = {
        ('my_key', [1, 2]):
            2: [4],
            3: [1, 6]
            }


        now= {
            ('my', ('my$', 'y$m', '$my')):
                2: [4],
                3: [1, 6]
        }
        This will be the structure of our permuted index


    - phrase_query, the method implemented in class that works with indexes i and j, performs as my 
        method that uses intersection and union method; my method is easly to understand


    - When constructing bst, we have to start from the middle of all words.

    

    - this without lemmatination and not removing stop words, is best suited for
        phrases that are small and with stop words like "no harn in"
"""


def timeit_test(fun, times):
    start = time.time()
    for i in range(times):
        fun
    end = time.time()
    finish = (end-start)/times
    return finish


def read_files(file_names):

    documents = []
    try:
        for file in file_names:
            with open("data/gutenberg/"+file, "r") as f:
                documents.append((file,f.read()))
            f.close()
    except:
        print("File doesn't exist")
    
    return documents

def load_index(it_exixt = False):

    if not it_exixt:
        file_name = ["alice_in_wonderland", "moby_dick", "romeo_and_juliet", "pride_and_prejudice"]
        # file_name = ["moby dick"]
        documents = read_files(file_name)

        gut_index = Index(documents)

        with open("data/indexV4.pickle", "wb") as f:
            pickle.dump(gut_index, f)
    
    else:
        with open("data/indexV4.pickle", "rb") as f:
            gut_index = pickle.load(f)

    return gut_index


def test_phrase(gut_index):

    query_df = pd.read_csv("data/gutenberg/query.csv", header=None)
    result = []
    for row in query_df.iloc:
        query = row[0]
        title = row[1]
        result.append(gut_index.phrase_query(query))
    query_df["result"] = result

    return query_df


def test_wildcard(gut_index, wild: list):
    result = {}
    for query in wild:
        result[query] = gut_index.wildcard_query(query)
    
    result_df = pd.DataFrame(result.items())
    return result_df

def test_boolean(gut_index, boolean: list):
    result = {}
    for query in boolean:
        result[query] = gut_index.boolean_query(query)
    
    result_df = pd.DataFrame(result.items())
    return result_df
    


#           MAIN


# with open("data/lorem_ipsum", "r") as f:
#     documents = [line.split("\n")[0] for line in f]
# f.close()


# indexes = Index(documents)

# print(indexes.print_inorder())

# new_doc = "Ehi, how it is my friend Giovanni? I like his cats"

# # indexes.add_doc(new_doc)


# query = "semper AND commodo OR accumsan"

# print("Result of query '", query, "': ", indexes.boolean_query(query))

# query_phrase = "Lorem ipsum dolor sit"
# print("Result of query prof '",query_phrase,"': ",indexes.phrase_query(query_phrase))

# # # print("Time for query: ", timeit_test(inverted_doc.query(query), 100000000))
# # # print("Time for query phrase: ", timeit_test(inverted_doc.phrase_query(query_phrase), 100000000))


# query_wrong = "lorum ipsimum dolor sut"
# print("Result of query '",query_wrong, "': ", indexes.phrase_query_sc(query_wrong))
# # # print("Time for query with sc: ", timeit_test(inverted_doc.phrase_query_sc(query_wrong), 100000))


# wildcard_query = "tem*"
# print(indexes.wildcard_query(wildcard_query))

# print("aaa")








gut_index = load_index(True)


# print(gut_index.boolean_query("Romeo and juliet"))

# # print(cicero.phrase_query("they saw many whales sporting in the ocean"))
# print(gut_index.phrase_query("they saw many whales"))
# print(gut_index.wildcard_query("div*"))

# new_doc = "Ehi, how it is my friend Giovanni? I like his cats"

# cicero.add_doc(new_doc)


print(test_boolean(gut_index, ["romeo and juliet", "romeo or juliet", 
                               "romeo and not juliet", "chapter", "william and watson"]))

print(test_phrase(gut_index))

print(test_wildcard(gut_index, ["rom*", "*om", "r*m"]))

print(gut_index.phrase_query_sc("Thud with a koss I die."))








# with open("data/articles2.pkl", "rb") as f:
#     articles = pickle.load(f)

# with open("data/queries2.pkl", "rb") as f:
#     queries = pickle.load(f)

# with open("data/relevance.pkl", "rb") as f:
#     relevance = pickle.load(f)

# bol = Index(articles)
# print("Query: ",queries[0], " --> ",bol.phrase_query(queries[0]))







# cisi = CISI()
# ## Here we check some statistics and info of CISI dataset

# print('Read %s documents, %s queries and %s mappings from CISI dataset' % 
#       (len(cisi.doc_set), len(cisi.qry_set), len(cisi.rel_set)))

# number_of_rel_docs = [len(value) for key, value in cisi.rel_set.items()]
# print('Average %.2f and %d min number of relevant documents by query ' % 
#       (np.mean(number_of_rel_docs), np.min(number_of_rel_docs)))

# print('Queries without relevant documents: ', 
#       np.setdiff1d(list(cisi.qry_set.keys()),list(cisi.rel_set.keys())))






print("ciao")