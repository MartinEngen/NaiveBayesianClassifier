import os
import re


def get_subfolder_paths(folder_relative_path: str) -> list:
    """
    Gets all subfolders of a given path
    :param folder_relative_path: Relative path of folder to find subfolders of
    :return: list of relative paths to any subfolders
    """
    return [f.path for f in os.scandir(folder_relative_path) if f.is_dir()]


def get_group_name(group_path: str) -> str:
    return group_path.split("\\")[-1]


def replace_unwanted_characters(line: str) -> str:
    return re.sub(
        r'([^\s\w]|_)+',
        u' ',
        line.replace('\n', ' ').replace('\t', ' '),
        flags=re.UNICODE
    )

def clean_document(document_file) -> list:
    document = document_file.read().lower().split("\n\n")
    cleaned_lines = list(map(replace_unwanted_characters, document[1:]))
    # lambda x, y: x + y, a, b
    list_of_lines = map(lambda x: x.split(" "), cleaned_lines)
    flattened_list_of_lines = [val for sublist in list_of_lines for val in sublist]

    return filter(lambda x: x != '', flattened_list_of_lines)
