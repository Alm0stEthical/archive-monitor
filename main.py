import os
import time
import shutil
import logging
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ArchiveHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(('.rar', '.zip')):
            self.wait_for_file(event.src_path)
            self.extract_and_delete(event.src_path)

    def wait_for_file(self, file_path):
        while True:
            try:
                with open(file_path, 'rb') as file:
                    break
            except IOError:
                logging.warning(f"File {file_path} is in use, waiting...")
                time.sleep(5)

    def extract_and_delete(self, archive_path):
        extract_dir = os.path.splitext(archive_path)[0]
        winrar_path = 'C:\\Program Files\\WinRAR\\WinRAR.exe'
        
        if not os.path.exists(winrar_path):
            logging.error("WinRAR not found at the specified path.")
            return

        try:
            if not os.path.exists(extract_dir):
                os.makedirs(extract_dir)

            result = subprocess.run([winrar_path, 'x', '-o+', archive_path, extract_dir], check=True, capture_output=True, text=True)
            logging.info(result.stdout)
            logging.info(f"Extracted: {archive_path}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to extract {archive_path}: {e}")
            logging.error(f"WinRAR output: {e.stdout}")
            return

        while True:
            try:
                os.remove(archive_path)
                logging.info(f"Deleted: {archive_path}")
                break
            except Exception as e:
                logging.warning(f"Failed to delete {archive_path}: {e}, retrying in 10 seconds...")
                time.sleep(10)

def monitor_directory(directory_to_watch):
    if not os.path.exists(directory_to_watch):
        logging.error(f"The directory {directory_to_watch} does not exist.")
        return

    event_handler = ArchiveHandler()
    observer = Observer()
    observer.schedule(event_handler, directory_to_watch, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    user_downloads_path = os.path.join(os.environ['USERPROFILE'], 'Downloads')
    monitor_directory(user_downloads_path)
