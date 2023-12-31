from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move
from time import sleep

import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


#folder to track e.g. Windows: "C:\\Users\\UserName\\Downloads"
source_dir = r"C:\Users\deand\Downloads"
dest_dir_music = r"C:\Users\deand\Desktop\Audio"
dest_dir_video = r"C:\Users\deand\Desktop\Video"
dest_dir_image = r"C:\Users\deand\Desktop\Images"
dest_dir_documents =r"C:\Users\deand\Desktop\Other Docs"
dest_dir_pdf = r"C:\Users\deand\Desktop\PDF"
dest_dir_docs = r"C:\Users\deand\Desktop\Docs"
dest_dir_exe = r"C:\Users\deand\Desktop\exe"


image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]

video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]

audio_extensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]

document_extensions = [ ".odt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv", ".zip"]

exe_extensions= [".exe"]

pdf_extensions = [".pdf"]  

docs_extensions= [".doc", ".docx"]                     


def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    # * IF FILE EXISTS, ADDS NUMBER TO THE END OF THE FILENAME
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name


def move_file(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        rename(oldName, newName)
    move(entry, dest)


class MoverHandler(FileSystemEventHandler):
    # ? THIS FUNCTION WILL RUN WHENEVER THERE IS A CHANGE IN "source_dir"
    # ? .upper is for not missing out on files with uppercase extensions
    def on_modified(self, event):
        with scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                self.check_audio_files(entry, name)
                self.check_video_files(entry, name)
                self.check_image_files(entry, name)
                self.check_document_files(entry, name)
                self.check_pdf_files(entry,name)
                self.check_docs_files(entry,name)
                self.check_exe_files(entry,name)

    def check_audio_files(self, entry, name):  # * Checks all Audio Files
        for audio_extension in audio_extensions:
            if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
                if entry.stat().st_size < 10_000_000 or "SFX" in name:  # ? 10Megabytes
                    dest = dest_dir_sfx
                else:
                    dest = dest_dir_music
                move_file(dest, entry, name)
                logging.info(f"Moved audio file: {name}")

    def check_video_files(self, entry, name):  # * Checks all Video Files
        for video_extension in video_extensions:
            if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                move_file(dest_dir_video, entry, name)
                logging.info(f"Moved video file: {name}")

    def check_image_files(self, entry, name):  # * Checks all Image Files
        for image_extension in image_extensions:
            if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                move_file(dest_dir_image, entry, name)
                logging.info(f"Moved image file: {name}")

    def check_document_files(self, entry, name):  # * Checks all Document Files
        for documents_extension in document_extensions:
            if name.endswith(documents_extension) or name.endswith(documents_extension.upper()):
                move_file(dest_dir_documents, entry, name)
                logging.info(f"Moved document file: {name}")

    def check_pdf_files(self, entry, name):  # * Checks all PDF Files
        for pdf_ext in pdf_extensions:
            if name.endswith(pdf_ext) or name.endswith(pdf_ext.upper()):
                move_file(dest_dir_pdf, entry, name)
                logging.info(f"Moved document file: {name}")  

    def check_docs_files(self, entry, name):  # * Checks all Doc & Docx Files
        for docs_ext in docs_extensions:
            if name.endswith(docs_ext) or name.endswith(docs_ext.upper()):
                move_file(dest_dir_docs, entry, name)
                logging.info(f"Moved document file: {name}")  

    def check_exe_files(self, entry, name):  # * Checks all Exe Files
        for exe_ext in exe_extensions:
            if name.endswith(exe_ext) or name.endswith(exe_ext.upper()):
                move_file(dest_dir_exe, entry, name)
                logging.info(f"Moved document file: {name}")                                   


# ! NO NEED TO CHANGE BELOW CODE
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
