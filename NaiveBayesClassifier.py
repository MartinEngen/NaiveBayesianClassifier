import glob
import math
import os
from functools import reduce
from Group import get_document_words, Group
from Utils import get_subfolder_paths
from Group import generate_groups
from typing import NewType, Sequence

def train():
    pass


def get_total_file_count(groups: list) -> int:
    return reduce((lambda x, group: len(group.relevant_documents) + x), groups, 0)


def find_group_sum(group: Group, document: list) -> float:
    p = math.log(group.group_p)

    for word in document:
        if word in group.vocabulary_percent:
            p += math.log(group.vocabulary_percent[word])

    return p

def classify_text(all_groups: Sequence[Group], path_to_file: str) -> str:
    document_words = get_document_words(path_to_file)

    result = {}
    for group in all_groups:
        group_p = find_group_sum(group, document_words)
        result[group.name] = group_p * (-1)

    #print(result)
    import operator
    verdict = max(result.items(), key=operator.itemgetter(1))[0]

    print(f'verdict: {verdict}')
    # For each group, get the SUM
    return ''

if __name__ == '__main__':
    NEWSGROUP_FOLDER = "20_newsgroups"
    all_groups = generate_groups(NEWSGROUP_FOLDER)
    total_files = get_total_file_count(all_groups)

    [group.generate_vocabulary() for group in all_groups]
    [group.generate_group_p(total_files) for group in all_groups]

    # Get a file path..
    documents_by_group = get_subfolder_paths(NEWSGROUP_FOLDER)
    #print(documents_by_group)

    for document_group in documents_by_group:
        print(f'Checking {document_group} ----------------------------------------------------')
        relevant_files = [f for f in glob.glob(document_group + "**/*", recursive=True)][-20:-1]
        for f in relevant_files:
            classify_text(all_groups, f)