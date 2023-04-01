from sortedcontainers import SortedList

def import_dict(filename = "english3.txt"):
    dictio = []
    with open("data/"+str(filename), "r") as f:
        for row in f:
            dictio.append(row[:-2])
            
    return dictio

# nomi propri?
# punteggitura?

#quando aggiorno il dizionario, tutti gli indici si sballano
#   quindi sarebbe da aggiornare gli indici che cambiano

# do tokenization and normalization, stemming

# text_1 = []
# for doc in text:
#     text_1.append(doc.lower())

# dictio = import_dict()

# text = text_1.copy()
# text = [SortedList(t.split()) for t in text]

# index_control = [0 for i in range(len(text))]
# doc_dict = {term: [] for term in dictio}

# for word in dictio:
#     for n_doc in range(len(text)):
#         if word == text[n_doc][index_control[n_doc]]:
#             print(word)
#             index_control[n_doc] += 1
        
            


# # how to link the dictionary with the documents indexing?
# # possible idea: order in alphabetic the words of the documents and scan one time the dictionary
# # another idea: O(n^2) scan documents and dictionary with two for loops
# print(text)

import string
# Ricordarsi che per usare queste librerie nltk, bisogna installare i database, che vengono salvati in /home/thomas/nltk_data...
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

stop_words = set(stopwords.words("english"))
punctuation = set(string.punctuation)
stemmer = PorterStemmer()


def create_inverted_index(documents):


    # inverted_doc = {term.lower() : [] for doc in documents for term in doc.split() if term.lower() not in stop_words}
    inverted_doc = dict()

    for doc_id, doc in enumerate(documents):
        for term in word_tokenize(doc):   # also doc.split() can be used but it's difficult to caputure punctuation
            term = term.lower() #lowercase
            term_split = term.split('\'')  # split apostrophe words and then save only important words
            for term_no_ap in term_split:
                if term_no_ap not in stop_words and term_no_ap not in punctuation and term_no_ap != '': #remove stop words and punctation
                    term_no_ap = stemmer.stem(term_no_ap)
                    if inverted_doc.get(term_no_ap) is not None:
                        inverted_doc[term_no_ap].append(doc_id)
                    else:
                        inverted_doc[term_no_ap] = [doc_id]

    return inverted_doc, len(documents)


def add_doc_on_inverted_index(new_doc, n_docs): 
    new_doc_id = n_docs
    for term in word_tokenize(new_doc):
        # print(term)
        term = term.lower()
        term_split = term.split('\'')  # split apostrophe words and then save only important words
        for term_no_ap in term_split:
            if term_no_ap not in stop_words and term_no_ap not in punctuation and term_no_ap != '':
                term_no_ap = stemmer.stem(term_no_ap)
                if inverted_doc.get(term_no_ap) is not None:
                    inverted_doc[term_no_ap].append(new_doc_id)
                else:
                    inverted_doc[term_no_ap] = [new_doc_id]

    return inverted_doc, n_docs + 1




documents = ["The cat is on the table. NAME",
            "What is the cat's name?",
            "Can you pass me the hammer? I need it!",
            "It was passed"
            #"cliche, clichè",
            #"color, colour"
            ]

inverted_doc, n_docs = create_inverted_index(documents)
# print(inverted_doc)

new_doc = "Ehi, how it is my friend Giovanni? I like his cats"

inverted_doc, n_docs = add_doc_on_inverted_index(new_doc, n_docs)

print(inverted_doc)

query = "not name AND not cat OR ehi"

split_query = [stemmer.stem(term) for term in query.split(" ")]
# query_terms = [stemmer.stem(term) for term in split_query[::2]]
# query_ops = split_query[1::2]

all_docs = set([d for d in range(n_docs)])

if split_query[0].lower() == "not":
    res = all_docs.difference(inverted_doc[split_query[1]])
else:
    res = set(inverted_doc[split_query[0]])
for i in range(len(split_query)):
    if split_query[i].lower() == "and":
        if split_query[i+1].lower() == "not":
            not_doc = all_docs.difference(inverted_doc[split_query[i+2]])
            res = res.intersection(not_doc)
        else:
            res = res.intersection(inverted_doc[split_query[i+1]])

    elif split_query[i].lower() == "or":
        if split_query[i+1].lower() == "not":
            not_doc = all_docs.difference(inverted_doc[split_query[i+2]])
            res = res.union(not_doc)
        else:
            res = res.union(inverted_doc[split_query[i+1]])
    


    # if op.lower() == "not":
    #     all_ids = [i for i in range(n_docs)]
    #     query_terms[0] = all_ids - 
    #Casino perché il not viene prima
        
print(res)

# split_query = [stemmer.stem(term) for term in split_query]


# doc_a = inverted_doc[split_query[0]]
# doc_b = inverted_doc[split_query[1]]

# common_docs = set(doc_a).intersection(doc_b)
# print("Result AND: " + str(common_docs))
