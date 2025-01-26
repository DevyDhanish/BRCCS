# RnW : Read and Write Top class use this class to read and write data to disk

from .handlers import handlers
from .handlers.filehandler import FileHandler

class ReaderAndWriter:

# private methods
    def _get_handler(self, file_ext) -> FileHandler:
        return handlers._get_handler(file_ext)

    def read_file(self, file_path : str):
        file_ext = file_path.split(".")[-1] # get the file extension
        handler = self._get_handler(file_ext)
        return handler.read_file(file_path)

    def write_to_file(self, file_path, data):
        file_ext = file_path.split(".")[-1]
        handler = self._get_handler(file_ext)
        handler.write_to_file(file_path, data)