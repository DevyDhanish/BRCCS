from .filehandler import FileHandler

import moviepy

class VideoHandler(FileHandler):
    def read_file(self, file_path):
        return moviepy.VideoFileClip(file_path)

    def write_to_file(self, file_path, data):
        data.write_videofile(file_path)
