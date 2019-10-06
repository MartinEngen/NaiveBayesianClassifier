import glob
import math
import os
from functools import reduce
import numpy as np
import eel as eel

from Group import get_document_words, Group, Vocabulary, generate_unique_vocab
from Utils import get_subfolder_paths, get_group_name
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

    import operator
    verdict = max(result.items(), key=operator.itemgetter(1))[0]
    return verdict


def check_group_performance(all_groups, documents_by_group):
    series_result = []

    for index, document_group in enumerate(documents_by_group):
        relevant_files = [f for f in glob.glob(document_group + "**/*", recursive=True)][-100:]
        sum_correct = 0
        checking_num_files = len(relevant_files)
        for f in relevant_files:
            verdict = classify_text(all_groups, f)

            if verdict in document_group:
                sum_correct += 1

        print(f'{document_group} - success rate: {sum_correct / checking_num_files}')
        series_result.append(sum_correct / checking_num_files)
    mean_result = np.mean(series_result)
    print(f'Total Result: {np.mean(mean_result)}')

    return {
        'mean_result': mean_result,
        'series_result': series_result
    }


if __name__ == '__main__':
    eel.init('web')  # GUI related
    NEWSGROUP_FOLDER = "20_newsgroups"

    vocab = Vocabulary()
    series = []
    documents_by_group = get_subfolder_paths(NEWSGROUP_FOLDER)

    # Create new groups
    all_groups = generate_groups(NEWSGROUP_FOLDER)
    total_files = get_total_file_count(all_groups)

    category_result = []
    total_result = {
        'name': 'average result',
        'data': []
    }

    for i in range(len(documents_by_group)):
        category_result.append({
            'name': get_group_name(documents_by_group[i]),
            'data': []
        })

    for i in range(0, 1000, 100):
        print(f'checking range {i} - {i + 100}')

        [group.generate_vocabulary(i, i + 100, vocab) for group in all_groups]
        generate_unique_vocab(vocab)
        [group.generate_group_p(total_files, vocab) for group in all_groups]
        result = check_group_performance(all_groups, documents_by_group)

        for i in range(len(documents_by_group)):
            category_result[i]['data'].append(result['series_result'][i])

        total_result['data'].append(round(result['mean_result'], 2))

    print(total_result)

    chart_data = {
        'category_result': category_result,
        'total_result': total_result
    }


    @eel.expose
    def get_training_result():
        return {
            'chartData': chart_data
        }


    eel.start('main.html')
