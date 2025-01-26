from .filehandler import FileHandler
import json

class JsonHandler(FileHandler):

    def read_file(self, file_path):
        with open(file_path, "r") as jsonfile:
            json_data = json.load(jsonfile)
            return json_data

    def write_to_file(self, file_path, data):
        with open(file_path, "w") as file:

            try:
                json.dump(data, file)
            except TypeError:
                print(f"{data} is in wrong format for json")

            return