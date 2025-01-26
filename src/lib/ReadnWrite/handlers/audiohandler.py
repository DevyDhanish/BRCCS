from .filehandler import FileHandler

import moviepy

class AudioHandler(FileHandler):
    def read_file(self, file_path):
        return moviepy.AudioFileClip(file_path)

    def write_to_file(self, file_path, data):
        data.write_audiofile(file_path)