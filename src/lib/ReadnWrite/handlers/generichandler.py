from .filehandler import FileHandler

from src.lib.Logger.logger import Logger

class GenericHandler(FileHandler):

    def read_file(self, file_path):
        Logger.logerr(f"ts handler for {file_path} does not exist bruu 😂")
        return ""

    def write_to_file(self, file_path, data):
        Logger.logerr(f"write where nigga, the handler does not exist for file type {file_path} 😭")