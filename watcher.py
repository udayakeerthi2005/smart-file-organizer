import time
import threading

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from config.settings import get_source_folder
from main import organize_files


observer = None
watcher_thread = None
watcher_running = False


class FileCreatedHandler(FileSystemEventHandler):

    def on_created(self, event):

        if event.is_directory:
            return

        print(f"Detected new file: {event.src_path}")

        try:
            time.sleep(1)
            organize_files()

        except Exception as error:
            print(f"Watcher error: {error}")


def _run_observer():

    global observer, watcher_running

    source_folder = get_source_folder()

    event_handler = FileCreatedHandler()

    observer = Observer()

    observer.schedule(
        event_handler,
        source_folder,
        recursive=False
    )

    observer.start()

    watcher_running = True

    print(f"Watching folder: {source_folder}")

    try:
        while watcher_running:
            time.sleep(1)

    finally:

        if observer:
            observer.stop()
            observer.join()
            observer = None

        watcher_running = False

        print("Watcher stopped.")


def start_watcher():

    global watcher_thread, watcher_running

    if watcher_running:
        print("Watcher already running.")
        return

    watcher_thread = threading.Thread(
        target=_run_observer,
        name="WatcherThread"
    )

    watcher_thread.daemon = True

    watcher_thread.start()


def stop_watcher():

    global watcher_running

    if not watcher_running:
        print("Watcher is not running.")
        return

    watcher_running = False


def is_watcher_running():
    return watcher_running


if __name__ == "__main__":

    start_watcher()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        stop_watcher()