import os

from config.settings import DUPLICATE_FOLDER, ORGANIZED_FOLDERS, get_source_folder
from organizer.categorizer import get_category
from organizer.scanner import scan_folder
from organizer.mover import move_file
from organizer.logger_manager import setup_logger, log_info, log_error
from organizer.duplicate_checker import is_duplicate, load_existing_hashes
from organizer.history_manager import save_move_history

def organize_files():
    setup_logger()
    SOURCE_FOLDER = get_source_folder()

    seen_hashes = load_existing_hashes(SOURCE_FOLDER, ORGANIZED_FOLDERS)

    files = scan_folder(SOURCE_FOLDER)

    total_items = len(files)
    files_processed = 0
    moved_files = 0
    duplicate_files = 0
    error_count = 0
    skipped_folders = 0

    if not files:
        print("No files found.")
        log_info("No files found.")
        return

    for file in files:
        source_path = os.path.join(SOURCE_FOLDER, file)

        if os.path.isfile(source_path):
            files_processed += 1

            try:
                if is_duplicate(source_path, seen_hashes):
                    destination_folder = os.path.join(SOURCE_FOLDER, DUPLICATE_FOLDER)

                    destination_path = move_file(source_path, destination_folder, file)

                    if destination_path:
                        duplicate_files += 1
                        message = f"{file} moved to {destination_path}"
                        print(message)
                        log_info(message)
                    else:
                        error_count += 1
                        message = f"Failed to move duplicate file {file}"
                        print(message)
                        log_error(message)

                    continue

                category = get_category(file)

                destination_folder = os.path.join(SOURCE_FOLDER, category)

                destination_path = move_file(source_path, destination_folder, file)

                if destination_path:
                    duplicate_files += 1
                    save_move_history(source_path, destination_path)

                    message = f"{file} moved to {destination_path}"
                    print(message)
                    log_info(message)
                else:
                    error_count += 1
                    message = f"Failed to move {file}"
                    print(message)
                    log_error(message)

            except Exception as error:
                error_count += 1
                message = f"Error processing {file}: {error}"
                print(message)
                log_error(message)

        else:
            skipped_folders += 1

    print_summary(
        total_items,
        files_processed,
        moved_files,
        duplicate_files,
        error_count,
        skipped_folders
    )


def print_summary(total_items, files_processed, moved_files, duplicate_files, error_count, skipped_folders):
    print("\n========== SUMMARY REPORT ==========")
    print(f"Total items scanned: {total_items}")
    print(f"Files processed: {files_processed}")
    print(f"Moved files: {moved_files}")
    print(f"Duplicate files: {duplicate_files}")
    print(f"Errors: {error_count}")
    print(f"Skipped folders: {skipped_folders}")
    print("====================================")


if __name__ == "__main__":
    organize_files()