from tinydb import TinyDB, Query
from collections import Counter
import os
import glob



def clean_document(document_file):
    document = document_file.read().split("\n\n")
    document_metadata = document[0]
    cleaned_one = document[1:] #.replace('\n', ' ').lower().split(" ")
    print(cleaned_one)


if __name__ == '__main__':
    file = open("data/sample1.txt", "r")
    NEWSGROUP_FOLDER = "20_newsgroups"
    sp = file.read().replace('\n',' ').lower().split(" ")
    a = Counter(sp)
    subfolders = [f.path for f in os.scandir(NEWSGROUP_FOLDER) if f.is_dir()]

    """
    for folder in subfolders:
        files = [f for f in glob.glob(folder + "**/*", recursive=True)]
        print(files)
        for f in files:
            print(f)
            file = open(f, "r")
            sp = file.read().replace('\n', ' ').lower().split(" ")
            a = Counter(sp)
            print(a)
        print(folder)
    """

    folder = subfolders[0]
    files = [f for f in glob.glob(folder + "**/*", recursive=True)]
    print(files)
    for f in files:
        file = open(f, "r")
        clean_document(file)
        #print(f)
        """
        file = open(f, "r")
        print("*************************************")
        print(file.read().split("\n\n")[0])
        sp = file.read().replace('\n', ' ').lower().split(" ")
        a = Counter(sp)
        #print(a)
        """