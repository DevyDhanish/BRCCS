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

    count = 0
    for item_name in items:
        data = {}
        data["name"] = item_name
        data["path"] = get_full_path(Audio, item_name)
        data["format"] = item_name.split(".")[-1]

        idx["Audios"].append(data)
        count += 1

    return count

def index_videos():
    items = os.listdir(Video)

    count = 0
    for item_name in items:
        data = {}
        data["name"] = item_name
        data["path"] = get_full_path(Video, item_name)
        data["format"] = item_name.split(".")[-1]

        idx["Videos"].append(data)
        count += 1

    return count

def index_images():
    items = os.listdir(Images)

    count = 0
    for item_name in items:
        data = {}

        data["name"] = item_name
        data["path"] = get_full_path(Images, item_name)
        data["format"] = item_name.split(".")[-1]

        idx["Images"].append(data)
        count += 1

    return count

def main():
    rnw = ReaderAndWriter()
    # see how many we had before

    old_idx = {}
    try:
        old_idx = rnw.read_file(os.path.abspath(os.path.join(Data, "data_index.json")))
    except FileNotFoundError:
        print("No old data_idx")

    old_vid_amt = len(old_idx["Videos"])
    old_aud_amt = len(old_idx["Audios"])
    old_img_amt = len(old_idx["Images"])

    idx_aud = index_audios()
    print(f"Indexed {idx_aud - old_aud_amt} new audios")

    idx_vids = index_videos()
    print(f"Indexed {idx_vids - old_vid_amt} new videos")

    idx_img = index_images()
    print(f"Indexed {idx_img - old_img_amt} new images")

    rnw.write_to_file("data_index.json", idx)

if __name__ == "__main__":
    main()