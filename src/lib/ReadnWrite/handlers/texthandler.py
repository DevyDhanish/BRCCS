from .filehandler import FileHandler

class TextHandler(FileHandler):
    def read_file(self, file_path):
        with open(file_path, "r") as file:
            return file.read()

    def write_to_file(self, file_path, data):
        with open(file_path, "w") as file:
            file.write(str(data))
        return