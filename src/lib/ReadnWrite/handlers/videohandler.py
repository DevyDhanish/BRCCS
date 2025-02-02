from .filehandler import FileHandler

from src.lib.Logger.logger import Logger

import moviepy

class VideoHandler(FileHandler):

    def read_file(self, file_path):
        try:
            return moviepy.VideoFileClip(file_path)
        except FileNotFoundError:
            Logger.logerr(f"File not found: {file_path}")
        except Exception as e:
            Logger.logerr(f"An error occurred while reading the file: {e}")

    def write_to_file(self, file_path, data):
        try:
            data.write_videofile(file_path)
        except Exception as e:
            Logger.logerr(f"An error occurred while saving the frame to {file_path}: {e}")

    #
    # def read_file(self, file_path):
    #     return moviepy.VideoFileClip(file_path)
    #
    # def write_to_file(self, file_path, data):
    #     data.write_videofile(file_path)

