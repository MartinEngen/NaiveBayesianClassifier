import glob
import math
import os
from functools import reduce

import eel as eel

from Group import get_document_words, Group
from Utils import get_subfolder_paths
from Group import generate_groups
from typing import NewType, Sequence

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
        result[group.name] = group_p

    # print(result)
    import operator
    verdict = max(result.items(), key=operator.itemgetter(1))[0]

    # print(f'verdict: {verdict}')
    # For each group, get the SUM
    return verdict


if __name__ == '__main__':
    eel.init('web')  # GUI related
    NEWSGROUP_FOLDER = "20_newsgroups"

    """
    all_groups = generate_groups(NEWSGROUP_FOLDER)
    total_files = get_total_file_count(all_groups)
    [group.generate_vocabulary(100) for group in all_groups]
    [group.generate_group_p(total_files) for group in all_groups]

    documents_by_group = get_subfolder_paths(NEWSGROUP_FOLDER)
    for document_group in documents_by_group:
        relevant_files = [f for f in glob.glob(document_group + "**/*", recursive=True)][-200:]

        sum_correct = 0
        checking_num_files = len(relevant_files)
        for f in relevant_files:
            verdict = classify_text(all_groups, f)

            if verdict in document_group:
                sum_correct += 1
        print(f'Success Rate: {sum_correct / checking_num_files} for {document_group}')

    """

    series = []
    documents_by_group = get_subfolder_paths(NEWSGROUP_FOLDER)
    for index, document_group in enumerate(documents_by_group):
        series.append({
            'name': document_group,
            'data': []
        })



    print(series)

    for i in range(0, 500, 100):
        # Create new groups
        print(i)
        all_groups = generate_groups(NEWSGROUP_FOLDER)
        total_files = get_total_file_count(all_groups)
        [group.generate_vocabulary(i) for group in all_groups]
        [group.generate_group_p(total_files) for group in all_groups]

        for index, document_group in enumerate(documents_by_group):
            relevant_files = [f for f in glob.glob(document_group + "**/*", recursive=True)][-50:]
            sum_correct = 0
            checking_num_files = len(relevant_files)
            for f in relevant_files:
                verdict = classify_text(all_groups, f)

                if verdict in document_group:
                    sum_correct += 1

            series[index]['data'].append(sum_correct / checking_num_files)


    @eel.expose
    def get_training_result():
        print(series)
        return {
            'series': series
        }


    eel.start('main.html')
