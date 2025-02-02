from .filehandler import FileHandler
from src.lib.Logger.logger import Logger

import moviepy

class AudioHandler(FileHandler):
    def read_file(self, file_path):
        try:
            return moviepy.AudioFileClip(file_path)
        except FileNotFoundError:
            Logger.logerr(f"File not found bruz : {file_path}")
        except Exception as e:
            Logger.logerr(f"An errzz occurred while reading the file: {e}")

    def write_to_file(self, file_path, data):
        try:
            data.write_audiofile(file_path)
        except Exception as e:
            Logger.logerr(f"An errzz occurred while writing to file {file_path}: {e}")