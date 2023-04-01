
dict = []
with open("data/english3.txt", "r") as f:
    for row in f:
        dict.append(row[:-2])
    # dict = f.readlines()


print(dict)