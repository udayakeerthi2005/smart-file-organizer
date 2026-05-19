import os

from config.settings import FILE_CATEGORIES


def get_category(file_name):
    extension = os.path.splitext(file_name)[1].lower()

    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category

    return "Others"