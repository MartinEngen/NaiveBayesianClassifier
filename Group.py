from collections import Counter

from Stopwords import stopwords
from Utils import get_subfolder_paths, get_group_name, replace_unwanted_characters
import glob


class Group:
    def __init__(self, group_name, folder_path):
        """
        Initialize the group object
        :param group_name: group name, should be conistent with subfolder
        :param folder_path: path to the folder which contains all documents to this group
        """

        self.name = group_name
        self.folder_path: str = folder_path
        self.vocabulary: dict = {}
        self.vocabulary_percent: dict = {}
        self.file_count: int = 0
        self.relevant_documents = self.find_relevant_documents()
        self.group_p = 0

    def find_relevant_documents(self) -> list:
        relevant_files = [f for f in glob.glob(self.folder_path + "**/*", recursive=True)]
        self.file_count = len(relevant_files)
        return relevant_files

    def generate_group_p(self, total_amount_documents):
        self.group_p = self.file_count / total_amount_documents

    def generate_vocabulary(self):
        print(f'generating vocabulary for {self.name}...')
        group_words = []
        for document_path in self.relevant_documents[:990]:
            words = get_document_words(document_path)
            group_words.extend(words)

        self.vocabulary = Counter(group_words)
        total_words = len(group_words)

        for word in self.vocabulary:
            word_p = self.vocabulary[word]/total_words
            self.vocabulary_percent[word] = word_p


def get_document_words(document_path: str) -> list:
    opened_document = open(document_path, "r")

    document_by_lines = opened_document.read().lower().split("\n\n")

    document_cleaned_relevant_lines = map(replace_unwanted_characters, document_by_lines[1:])
    words_in_per_line: iter = map(lambda x: x.split(" "), document_cleaned_relevant_lines)
    all_words: list = [val for sublist in words_in_per_line for val in sublist]

    filters = (no_stopword, no_one_char, no_numbers, no_whitespace)
    words = filter(lambda x: all(f(x) for f in filters), all_words)

    # Close the document
    opened_document.close()
    return list(words)


def generate_groups(newsgroup_folder: str) -> list:
    newsgroup_folders_paths = get_subfolder_paths(newsgroup_folder)
    return [Group(get_group_name(newsgroup_path), newsgroup_path) for newsgroup_path in newsgroup_folders_paths]


def no_whitespace(word):
    return word != ''


def no_stopword(word):
    return word not in stopwords


def no_one_char(word):
    return len(word) > 1


def no_numbers(word):
    return not any(str.isdigit(c) for c in word)
