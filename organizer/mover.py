import os
import shutil

from organizer.renamer import get_unique_file_path


def move_file(source_path, destination_folder, file_name):
    try:
        os.makedirs(destination_folder, exist_ok=True)

        destination_path = get_unique_file_path(destination_folder, file_name)

        shutil.move(source_path, destination_path)

        return destination_path

    except Exception as error:
        print(f"Error moving {file_name}: {error}")
        return None