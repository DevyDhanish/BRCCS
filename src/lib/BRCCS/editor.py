import random

import moviepy
from ..ReadnWrite.RnW import ReaderAndWriter
from .timeutils import TimeUtils
from src.lib.Logger.logger import Logger
from src.lib.BRCCS.filestypes import IMAGE, AUDIO, VIDEO
from moviepy import *

class Editor:

    video = []
    audio = []

    # def position_video(self, video, pos_x = "", pos_y = ""):
    #         return video.with_position((pos_x, pos_y))

    def extract_clip(self, file, from_, to):

        if file is not None and from_ != 0 and to != 0:
            return file.subclipped(from_, to)

        return file

    def add_video(self, video_data : VideoFileClip,
                  start : int,
                  end : int,
                  clipping : bool,
                  frm : int,
                  to : int,
                  pos_x = "",
                  pos_y = ""):

        if clipping:
            video_data = self.extract_clip(video_data, frm, to)

        self.video.append(video_data.with_start(start)
                          .with_duration(end - start)
                          .without_audio()
                          .with_position((pos_x, pos_y)))

    def add_audio(self, audio_data : AudioFileClip,
                  start : int,
                  end : int,
                  clipping : int,
                  frm : int,
                  to : int):

        clip = audio_data

        if clipping:
            clip = self.extract_clip(audio_data, frm, to)

        # Calculate the duration needed to extend
        original_duration = clip.duration
        required_duration = end - start

        if original_duration < required_duration:
            # Create a silent audio clip of the required extra duration
            extra_duration = required_duration - original_duration
            silent_clip = AudioClip(lambda t: 0, duration=extra_duration).with_fps(clip.fps)
            # Combine the original audio with the silent clip
            clip = concatenate_audioclips([clip, silent_clip])

        audio_with_timing = clip.with_start(start).with_duration(required_duration)
        self.audio.append(audio_with_timing)

    def composite_video(self):

        if len(self.video) > 0:
            return moviepy.CompositeVideoClip(self.video)

        Logger.logwarn("No videos to composite")

    def composite_audio(self):

        if len(self.audio) > 0:
            return moviepy.CompositeAudioClip(self.audio)

        Logger.logwarn("No audios to composite")

    def create_timeline_by_video_structure(self, video_struct):

        # add all the video
        rw = ReaderAndWriter()

        for video in video_struct["Video"]:

            video_file = rw.read_file(video["path"])

            start_stamp = TimeUtils.timestamp_to_seconds(video["start_at"])
            end_stamp = TimeUtils.timestamp_to_seconds(video["end_at"])
            frm_stamp = TimeUtils.timestamp_to_seconds(video["from"])
            to_stamp = TimeUtils.timestamp_to_seconds(video["to"])
            pos_x = video["pos_x"]
            pos_y = video["pos_y"]

            Logger.logwarn(f"Processing : {video}")

            if video["of_type"] == IMAGE:
                self.add_video(video_file,
                               start_stamp,
                               end_stamp,
                               False,
                               0,
                               0,
                               pos_x,
                               pos_y)

            else:
                self.add_video(video_file,
                               start_stamp,
                               end_stamp,
                               True,
                               frm_stamp,
                               to_stamp,
                               pos_x,
                               pos_y)


        for audio in video_struct["Audio"]:

            audio_file = rw.read_file(audio["path"])

            start_stamp = TimeUtils.timestamp_to_seconds(audio["start_at"])
            end_stamp = TimeUtils.timestamp_to_seconds(audio["end_at"])
            frm_stamp = TimeUtils.timestamp_to_seconds(audio["from"])
            to_stamp = TimeUtils.timestamp_to_seconds(audio["to"])

            Logger.logwarn(f"Processing {audio}")

            self.add_audio(audio_file,
                           start_stamp,
                           end_stamp,
                           True,
                           frm_stamp,
                           to_stamp)

    def set_audio(self, video_data, audio_data):
        return video_data.with_audio(audio_data)

    @staticmethod
    def get_clip_duration(clip_file):
        try:
            return clip_file.duration
        except TypeError:
            Logger.logerr(f"{clip_file} is not a VideoClipFile nigga")
            return 0