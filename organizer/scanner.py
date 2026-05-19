import os


def scan_folder(path):
    try:
        files = os.listdir(path)
        return files

    except FileNotFoundError:
        print("Folder not found.")
        return []

    except PermissionError:
        print("Permission denied.")
        return []

    except Exception as error:
        print(f"Unexpected error while scanning folder: {error}")
        return []