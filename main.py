from tinydb import TinyDB, Query
from collections import Counter
import os
import glob
import re, locale
import math

def replace_unwanted_characters(line: str) -> str:
    return re.sub(r'([^\s\w]|_)+', u' ',
                  line.replace('\n', ' ').replace('\t', ' '),
                  flags=re.UNICODE)

def clean_document(document_file) -> Counter:
    document = document_file.read().lower().split("\n\n")
    document_metadata = document[0]
    cleaned_lines = list(map(replace_unwanted_characters, document[1:]))
    list_of_lines = map(lambda x: x.split(" "), cleaned_lines)
    flattened_list_of_lines = [val for sublist in list_of_lines for val in sublist]

    filtered_list = filter(lambda x: x != '', flattened_list_of_lines)
    return Counter(filtered_list)

def get_document_words(document_file) -> list:
    document = document_file.read().lower().split("\n\n")
    document_metadata = document[0]
    cleaned_lines = list(map(replace_unwanted_characters, document[1:]))
    list_of_lines = map(lambda x: x.split(" "), cleaned_lines)
    flattened_list_of_lines = [val for sublist in list_of_lines for val in sublist]
    filtered_list = list(filter(lambda x: x != '', flattened_list_of_lines))

    return filtered_list


if __name__ == '__main__':
    file = open("data/sample1.txt", "r")
    NEWSGROUP_FOLDER = "20_newsgroups"
    sp = file.read().replace('\n',' ').lower().split(" ")
    subfolders = [f.path for f in os.scandir(NEWSGROUP_FOLDER) if f.is_dir()]

    percent_word_given_group = {}
    p_word_given_group = {}
    p_group = {}
    total_files = 0

    # Training
    for folder in subfolders:
        files = [f for f in glob.glob(folder + "**/*", recursive=True)]
        group_name = folder.split("\\")[-1]
        p_word_given_group[group_name] = {}

        # Count File Length
        total_files += len(files)
        p_group[group_name] = len(files)

        for f in files:
            file = open(f, "r")
            counted_words_in_file: Counter = clean_document(file)

            for countItem in counted_words_in_file:
                if countItem in p_word_given_group[group_name]:
                    p_word_given_group[group_name][countItem] += counted_words_in_file[countItem]
                else:
                    p_word_given_group[group_name][countItem] = counted_words_in_file[countItem]

            file.close()
        sum_words = sum(p_word_given_group[group_name].values())
        vocabulary_length = len(p_word_given_group[group_name])
        percent_word_given_group[group_name] = {}
        # Calculating Percent

        for current_word in p_word_given_group[group_name]:
            current_word_count = p_word_given_group[group_name][current_word]
            current_word_percent = current_word_count / (sum_words + vocabulary_length)
            percent_word_given_group[group_name][current_word] = current_word_percent

    for group in p_group:
        documents_in_group = p_group[group]
        p_group[group] = documents_in_group / total_files

    check_folder = subfolders[1]
    check_files = [f for f in glob.glob(check_folder + "**/*", recursive=True)][-6:-1]

    for file in check_files:
        max_group = 0
        max_p = 1

        document_file = open(file, "r")
        document_words = get_document_words(document_file)

        for group_name in p_group:
            p = math.log(p_group[group_name])

            for word in document_words:
                if word in percent_word_given_group[group_name]:
                    p += math.log(percent_word_given_group[group_name][word])

            p = p * (-1)
            print(f'{group_name} = {p}')
            if p > max_p or max_p == 1:

                max_p = p
                max_group = group_name

        print(f'result: {max_group} - target {check_folder}')

    # import pprint
    #print("hello")
    # pp = pprint.PrettyPrinter()
    # pp.pprint(p_group)
    # pp.pprint(check_files)
    # pp.pprint(sorted_x)
    # print(p_word_given_group)
