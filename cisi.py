


class CISI:
    def __init__(self):
        self.doc_set = process_documents()
        self.qry_set = process_queries()
        self.rel_set = process_relevance()


## Processing DOCUMENTS
def process_documents():
        
    doc_set = {}
    doc_id = ""
    doc_text = ""
    with open('data/cisi/CISI.ALL') as f:
        lines = ""
        for l in f.readlines():
            lines += "\n" + l.strip() if l.startswith(".") else " " + l.strip()
        lines = lines.lstrip("\n").split("\n")
    doc_count = 0
    for l in lines:
        if l.startswith(".I"):
            doc_id = int(l.split(" ")[1].strip())-1
        elif l.startswith(".X"):
            doc_set[doc_id] = doc_text.lstrip(" ")
            doc_id = ""
            doc_text = ""
        else:
            doc_text += l.strip()[3:] + " " # The first 3 characters of a line can be ignored.    

    return doc_set

        
### Processing QUERIES
def process_queries():
    with open('data/cisi/CISI.QRY') as f:
        lines = ""
        for l in f.readlines():
            lines += "\n" + l.strip() if l.startswith(".") else " " + l.strip()
        lines = lines.lstrip("\n").split("\n")

    qry_set = {}
    qry_id = ""
    for l in lines:
        if l.startswith(".I"):
            qry_id = int(l.split(" ")[1].strip()) -1
        elif l.startswith(".W"):
            qry_set[qry_id] = l.strip()[3:]
            qry_id = ""
    
    return qry_set

### Processing QRELS
def process_relevance():
    rel_set = {}
    with open('data/cisi/CISI.REL') as f:
        for l in f.readlines():
            qry_id = int(l.lstrip(" ").strip("\n").split("\t")[0].split(" ")[0]) -1
            doc_id = int(l.lstrip(" ").strip("\n").split("\t")[0].split(" ")[-1])-1
            if qry_id in rel_set:
                rel_set[qry_id].append(doc_id)
            else:
                rel_set[qry_id] = []
                rel_set[qry_id].append(doc_id)

    return rel_set
