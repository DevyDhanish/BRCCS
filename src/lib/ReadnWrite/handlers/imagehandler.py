from .filehandler import FileHandler

from src.lib.Logger.logger import Logger

import moviepy

class ImageHandler(FileHandler):
    def read_file(self, file_path):
        try:
            return moviepy.ImageClip(file_path)
        except FileNotFoundError:
            Logger.logerr(f"File not found: {file_path}")
        except Exception as e:
            Logger.logerr(f"An error occurred while reading the file: {e}")

    def write_to_file(self, file_path, data):
        try:
            data.save_frame(file_path)
        except Exception as e:
            Logger.logerr(f"An error occurred while saving the frame to {file_path}: {e}")