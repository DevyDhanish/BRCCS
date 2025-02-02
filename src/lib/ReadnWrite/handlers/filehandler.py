from abc import abstractmethod


class FileHandler:

    @abstractmethod 
    def read_file(self, file_path):
        pass

    @abstractmethod
    def write_to_file(self, file_path, data):
        pass