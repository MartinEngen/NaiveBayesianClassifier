from collections import Counter

from Stopwords import stopwords
from Utils import get_subfolder_paths, get_group_name, replace_unwanted_characters
import glob


class Vocabulary:
    def __init__(self):
        self.words = set()


class Group:
    def __init__(self, group_name, folder_path):
        """
        Initialize the group object
        :param group_name: group name, should be conistent with subfolder
        :param folder_path: path to the folder which contains all documents to this group
        """
        self.name = group_name
        self.words = []
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

    def generate_group_p(self, total_amount_documents, vocab):

        # All words:
        vocab_length = len(vocab.words)
        words_length = len(self.words)

        for word in vocab.words:
            self.vocabulary_percent[word] = 1.0

        for word in self.words:
            if word in vocab.words:
                self.vocabulary_percent[word] += 1.0
        for word in vocab.words:
            self.vocabulary_percent[word] /= words_length + vocab_length

        self.group_p = self.file_count / total_amount_documents

    def generate_vocabulary(self, train_from_document: int, train_on_n_documents: int, vocab: Vocabulary):
        group_words = []
        for document_path in self.relevant_documents[train_from_document:train_on_n_documents]:
            words = get_document_words(document_path)
            group_words.extend(words)

        self.words.extend(group_words)
        vocab.words.update(group_words)


def get_document_words(document_path: str) -> list:
    opened_document = open(document_path, "r")

    document_by_lines = opened_document.read().lower().split("\n\n")
    document_cleaned_relevant_lines: iter = map(replace_unwanted_characters, document_by_lines[1:])
    words_in_per_line: iter = map(lambda x: x.split(" "), document_cleaned_relevant_lines)
    all_words: list = [val for sublist in words_in_per_line for val in sublist]

    # Close the document
    opened_document.close()
    return all_words


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


def generate_unique_vocab(vocab: Vocabulary):
    vocab.words = (set(vocab.words))
