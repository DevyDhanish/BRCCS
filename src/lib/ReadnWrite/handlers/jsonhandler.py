from .filehandler import FileHandler
from src.lib.Logger.logger import Logger
import json


class JsonHandler(FileHandler):

    def read_file(self, file_path):
        try:
            with open(file_path, "r") as jsonfile:
                json_data = json.load(jsonfile)
                return json_data
        except FileNotFoundError:
            Logger.logerr(f"File not found: {file_path}")
        except json.JSONDecodeError:
            Logger.logerr(f"Error decoding JSON from file: {file_path}")
        except Exception as e:
            Logger.logerr(f"An error occurred while reading the file: {e}")

    def write_to_file(self, file_path, data):
        try:
            with open(file_path, "w") as file:
                json.dump(data, file)
        except TypeError:
            Logger.logerr(f"Data {data} is in the wrong format for JSON")
        except Exception as e:
            Logger.logerr(f"An error occurred while writing to file {file_path}: {e}")