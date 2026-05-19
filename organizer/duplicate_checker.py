import os
import hashlib


def calculate_file_hash(file_path):
    hash_object = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_object.update(chunk)

    return hash_object.hexdigest()


def load_existing_hashes(source_folder, organized_folders):
    seen_hashes = set()

    for folder in organized_folders:
        folder_path = os.path.join(source_folder, folder)

        if not os.path.exists(folder_path):
            continue

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)

                try:
                    if os.path.getsize(file_path) == 0:
                        continue

                    file_hash = calculate_file_hash(file_path)
                    seen_hashes.add(file_hash)

                except Exception:
                    continue

    return seen_hashes


def is_duplicate(file_path, seen_hashes):
    if os.path.getsize(file_path) == 0:
        return False

    file_hash = calculate_file_hash(file_path)

    if file_hash in seen_hashes:
        return True

    seen_hashes.add(file_hash)
    return False