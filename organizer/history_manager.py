import os
import json

from config.settings import HISTORY_FILE_PATH


def save_move_history(original_path, new_path):
    os.makedirs(os.path.dirname(HISTORY_FILE_PATH), exist_ok=True)

    history = load_move_history()

    history.append({
        "original_path": original_path,
        "new_path": new_path
    })

    with open(HISTORY_FILE_PATH, "w") as file:
        json.dump(history, file, indent=4)


def load_move_history():
    if not os.path.exists(HISTORY_FILE_PATH):
        return []

    try:
        with open(HISTORY_FILE_PATH, "r") as file:
            return json.load(file)

    except json.JSONDecodeError:
        return []


def clear_move_history():
    os.makedirs(os.path.dirname(HISTORY_FILE_PATH), exist_ok=True)

    with open(HISTORY_FILE_PATH, "w") as file:
        json.dump([], file, indent=4)