from .filehandler import FileHandler

import moviepy

class ImageHandler(FileHandler):
    def read_file(self, file_path):
        return moviepy.ImageClip(file_path)

    def write_to_file(self, file_path, data):
        data.save_frame(file_path)