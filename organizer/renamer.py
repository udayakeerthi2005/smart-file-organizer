import os


def get_unique_file_path(destination_folder, file_name):
    destination_path = os.path.join(destination_folder, file_name)

    if not os.path.exists(destination_path):
        return destination_path

    name, extension = os.path.splitext(file_name)

    counter = 1

    while True:
        new_file_name = f"{name}_{counter}{extension}"
        new_destination_path = os.path.join(destination_folder, new_file_name)

        if not os.path.exists(new_destination_path):
            return new_destination_path

        counter += 1