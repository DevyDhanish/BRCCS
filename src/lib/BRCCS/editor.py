import moviepy
from ..ReadnWrite.RnW import ReaderAndWriter
from .timeframes import TimeFrames
from moviepy import *

class Editor:

    video = []
    audio = []

    def add_video(self, video_data, start, end, is_mute = True):
        self.video.append(video_data.with_start(start).with_duration(end - start).without_audio())

    def add_audio(self, audio_data, start, end, is_mute=False):
        # Calculate the duration needed to extend
        original_duration = audio_data.duration
        required_duration = end - start

        if original_duration < required_duration:
            # Create a silent audio clip of the required extra duration
            extra_duration = required_duration - original_duration
            silent_clip = AudioClip(lambda t: 0, duration=extra_duration).with_fps(audio_data.fps)
            # Combine the original audio with the silent clip
            audio_data = concatenate_audioclips([audio_data, silent_clip])

        audio_with_timing = audio_data.with_start(start).with_duration(required_duration)
        self.audio.append(audio_with_timing)

    def composite_video(self):
        return moviepy.CompositeVideoClip(self.video)

    def composite_audio(self):
        return moviepy.CompositeAudioClip(self.audio)

    def create_clip_using_video_structure(self, video_struct):

        # add all the video

        rw = ReaderAndWriter()
        tf = TimeFrames()

        for video in video_struct["Video"]:
            vid = rw.read_file(video["path"])
            start_stamp = tf.convert_time_frame_to_sec(video["start_at"])
            end_stamp = tf.convert_time_frame_to_sec(video["end_at"])
            self.add_video(vid, start_stamp, end_stamp)


        for audio in video_struct["Audio"]:
            vid = rw.read_file(audio["path"])
            start_stamp = tf.convert_time_frame_to_sec(audio["start_at"])
            end_stamp = tf.convert_time_frame_to_sec(audio["end_at"])
            self.add_audio(vid, start_stamp, end_stamp)


    def set_audio(self, video_data, audio_data):
        return video_data.with_audio(audio_data)