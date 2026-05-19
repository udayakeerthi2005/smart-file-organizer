import os
import shutil

from organizer.history_manager import load_move_history, clear_move_history
from organizer.renamer import get_unique_file_path


def undo_last_organization():
    history = load_move_history()

    if not history:
        print("No move history found.")
        return

    for record in reversed(history):
        original_path = record["original_path"]
        new_path = record["new_path"]

        if os.path.exists(new_path):
            original_folder = os.path.dirname(original_path)
            file_name = os.path.basename(original_path)

            os.makedirs(original_folder, exist_ok=True)

            safe_original_path = get_unique_file_path(original_folder, file_name)

            shutil.move(new_path, safe_original_path)

            print(f"Restored: {new_path} -> {safe_original_path}")

    clear_move_history()

    print("Undo completed successfully.")


if __name__ == "__main__":
    undo_last_organization()