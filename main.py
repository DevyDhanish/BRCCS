import os
from src.generator import generate
from src.lib.ReadnWrite.RnW import ReaderAndWriter
from src.lib.Logger.logger import Logger
from src.data_indexer import index_data
from src.data_organizer import organize
import random
import argparse


PARAMS = {}

def get_random(min, max):
    return random.randint(min, max)

def randomize_params():

    PARAMS["total_video_duration"] = get_random(
        PARAMS["min_total_video_duration"],
        PARAMS["max_total_video_duration"]
    )

    PARAMS["clip_duration"] = get_random(
        1,
        PARAMS["max_clip_duration"]
    )

    PARAMS["audio_duration"] = get_random(
        1,
        PARAMS["max_audio_duration"]
    )

    PARAMS["video_density"] = get_random(
    10,
        PARAMS["max_clip_density"]
    )

    PARAMS["img_density"] = get_random(
        0,
        PARAMS["max_img_density"]
    )

    PARAMS["audio_density"] = get_random(
        10,
        PARAMS["max_audio_density"]
    )

def create_vid():
    rw = ReaderAndWriter()

    PARAMS = rw.read_file("param.json")

    if PARAMS["randomize_params"] == 1:
        randomize_params()

    Logger.logwarn(f"Producing {PARAMS['randomize_params']} video")

    for _ in range(PARAMS["produce_videos"]):
        generate(PARAMS["total_video_duration"],
                 PARAMS["clip_duration"],
                 PARAMS["audio_duration"],
                 PARAMS["video_density"],
                 PARAMS["audio_density"],
                 PARAMS["img_density"],
                 os.path.abspath(PARAMS["data_index_directory"]),
                 PARAMS["output_directory"])

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--args", help="C - create, O - organize, I - index", required=True)

    args = parser.parse_args()

    args = args.args.lower() # Dumb ass nigga

    if args == "c":
        create_vid()

    if args == "o":
        organize()

    if args == "i":
        index_data()

    if args == "co":
        organize()
        create_vid()

    if args == "coi":
        organize()
        index_data()
        create_vid()

    if args == "oi":
        organize()
        index_data()

