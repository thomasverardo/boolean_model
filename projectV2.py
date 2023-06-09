import time
from index import Index


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



"""


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

indexes = Index()
indexes.create_indexes(documents)
# inverted_doc.create_permuted_index(documents)

# print(inverted_doc)

new_doc = "Ehi, how it is my friend Giovanni? I like his cats"

indexes.add_doc(new_doc)

# print(inverted_doc)

query = "semper AND commodo"

# print("Result of query '", query, "': ", inverted_doc.query(query))

query_phrase = "Lorem ipsum dolor sit"
print("Result of query prof '",query_phrase,"': ",indexes.phrase_query(query_phrase))

# print("Time for query: ", timeit_test(inverted_doc.query(query), 100000000))
# print("Time for query phrase: ", timeit_test(inverted_doc.phrase_query(query_phrase), 100000000))


query_wrong = "lorum ipsimum"
print("Result of query '",query_wrong, "': ", indexes.phrase_query_sc(query_wrong))
# print("Time for query with sc: ", timeit_test(inverted_doc.phrase_query_sc(query_wrong), 100000))



indexes.create_permuted_index(documents)

wildcard_query = "lor*m"
indexes.wildcard_query(wildcard_query)

print("aaa")

