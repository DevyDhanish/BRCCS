import time
from os import write

from moviepy import *
from .lib.ReadnWrite.RnW import ReaderAndWriter

import os
import shutil

data_shit_pool_dir = "..\\data\\data_shit_pool"
audio_save_path = "..\\data\\Audio"
img_save_path = "..\\data\\Images"
video_save_path = "..\\data\\Video"


rw = ReaderAndWriter()

def extract_audio(video):
    audio_clip = rw.read_file(video)

    if audio_clip.audio is not None:
        return audio_clip.audio

    return None

def get_extension(file_path):
    ext = file_path.split(".")[-1]

    expected_exts = ["mp4", "mp3", "png", "jpg", "jpeg", "wav"]

    if ext not in expected_exts:
        print(f"{ext} is not in expected_exts")
        return ""

    return ext

def delete_item():
    pass

def move_file(old, new):

    if old is None or new is None:
        return

    shutil.move(old, new)

def do_the_thing():
    all_files = os.listdir(data_shit_pool_dir)

    for files in all_files:

        full_path = os.path.abspath(os.path.join(data_shit_pool_dir, files))

        print(f"Found file {files}")

        ext = get_extension(full_path)

        if ext not in ["mp4", "mov"]:
            # save the file to it's desired location

            if ext in ["png", "jpg", "jpeg"]:
                move_file(full_path, os.path.abspath(os.path.join(img_save_path, files)))
                print(f"Moved {files} to {img_save_path}")

            if ext in ["mp3", "wav"]:
                move_file(full_path, os.path.abspath(os.path.join(audio_save_path, files)))
                print(f"Moved {files} to {audio_save_path}")

            break

        # the following will only work if it's a video
        audio = extract_audio(full_path)

        audio_file_name = files + ".mp3"

        # save the audio
        rw.write_to_file(os.path.abspath(os.path.join(audio_save_path, audio_file_name)), audio)
        print(f"Saved extracted audio {audio_file_name} at {audio_save_path}")

        # move the video
        move_file(full_path, os.path.abspath(os.path.join(video_save_path, files)))
        print(f"Moved {files} to {video_save_path}")

def organize():

    while len(os.listdir(data_shit_pool_dir)) > 0:

        try:
            do_the_thing()
        except PermissionError:
            print("trying again for some file")