import json
import os


from lib.ReadnWrite.RnW import ReaderAndWriter

Data = "..\\data"
Audio = "..\\data\\Audio"
Video = "..\\data\\Video"
Images = "..\\data\\Images"

idx = {
    "Images" : [],
    "Audios" : [],
    "Videos" : []
}


def get_full_path(rel_dir, filename):
    return os.path.abspath(os.path.join(rel_dir, filename))

def index_audios():
    items = os.listdir(Audio)

    for item_name in items:
        data = {}
        data["name"] = item_name
        data["path"] = get_full_path(Audio, item_name)
        data["format"] = item_name.split(".")[-1]

        idx["Audios"].append(data)

def index_videos():
    items = os.listdir(Video)

    for item_name in items:
        data = {}
        data["name"] = item_name
        data["path"] = get_full_path(Video, item_name)
        data["format"] = item_name.split(".")[-1]

        idx["Videos"].append(data)

def index_images():
    items = os.listdir(Images)

    for item_name in items:
        data = {}

        data["name"] = item_name
        data["path"] = get_full_path(Images, item_name)
        data["format"] = item_name.split(".")[-1]

        idx["Images"].append(data)

def main():
    index_audios()
    index_videos()
    index_images()

    rnw = ReaderAndWriter()

    rnw.write_to_file(os.path.abspath(os.path.join(Data, "data_index.json")), idx)

if __name__ == "__main__":
    main()