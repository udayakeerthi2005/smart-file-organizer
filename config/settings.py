SOURCE_FOLDER = "test_folder"

CURRENT_SOURCE_FOLDER = SOURCE_FOLDER

LOG_FILE_PATH = "logs/organizer.log"

HISTORY_FILE_PATH = "data/move_history.json"

DUPLICATE_FOLDER = "Duplicates"

ORGANIZED_FOLDERS = [
    "Documents",
    "Images",
    "Audio",
    "Videos",
    "Archives",
    "Code",
    "Others"
]

FILE_CATEGORIES = {
    "Documents": [
        ".pdf", ".txt", ".doc", ".docx",
        ".ppt", ".pptx", ".xls", ".xlsx",
        ".csv"
    ],

    "Images": [
        ".png", ".jpg", ".jpeg", ".gif",
        ".bmp", ".svg", ".webp"
    ],

    "Audio": [
        ".mp3", ".wav", ".aac", ".flac", ".m4a"
    ],

    "Videos": [
        ".mp4", ".mkv", ".avi", ".mov", ".wmv"
    ],

    "Archives": [
        ".zip", ".rar", ".7z", ".tar", ".gz"
    ],

    "Code": [
        ".py", ".java", ".c", ".cpp",
        ".html", ".css", ".js", ".json"
    ]
}


def set_source_folder(path):
    global CURRENT_SOURCE_FOLDER
    CURRENT_SOURCE_FOLDER = path


def get_source_folder():
    return CURRENT_SOURCE_FOLDER