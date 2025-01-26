import datetime
import os.path
import time
import random

from lib.ReadnWrite.RnW import ReaderAndWriter
from lib.BRCCS.videostructure import VideoStructure
from lib.BRCCS.timeframes import TimeFrames
from lib.BRCCS.editor import Editor

data_index_directory = "..\\data"
output_directory = "..\\outputs"

vs = VideoStructure()
tf = TimeFrames()
rw = ReaderAndWriter()

def video_structure(frames, video_pool : list):

    for frame in frames:
        rand_video = video_pool[random.randint(0, len(video_pool) - 1)]
        vs.add_video(rand_video["name"], tf.convert_sec_to_time_frame(frame[0]), tf.convert_sec_to_time_frame(frame[1]), rand_video["path"])

def audio_structure(frames, audio_pool : list):
    for frame in frames:
        rand_video = audio_pool[random.randint(0, len(audio_pool) - 1)]
        vs.add_audio(rand_video["name"], tf.convert_sec_to_time_frame(frame[0]), tf.convert_sec_to_time_frame(frame[1]), rand_video["path"])

def image_structure(frames, image_pool : list):
    for frame in frames:
        rand_video = image_pool[random.randint(0, len(image_pool) - 1)]
        vs.add_video(rand_video["name"], tf.convert_sec_to_time_frame(frame[0]), tf.convert_sec_to_time_frame(frame[1]), rand_video["path"])

if __name__ == "__main__":
    # Read the data index file
    data_index = rw.read_file(os.path.join(data_index_directory, "data_index.json"))

    # Define duration variables
    total_duration_seconds = 10
    clip_duration_seconds = 1

    # meta data directory
    meta_data_dir = os.path.abspath(os.path.join(data_index_directory, "meta_data.png"))
    vs.add_video("meta_data.png", tf.convert_sec_to_time_frame(0), tf.convert_sec_to_time_frame(total_duration_seconds), meta_data_dir)

    # Generate and process frames for videos
    video_frames = tf.generate_time_frames(total_duration_seconds, clip_duration_seconds)
    video_structure(video_frames, data_index["Videos"])

    # Generate and process frames for audio
    audio_frames = tf.generate_time_frames(total_duration_seconds, clip_duration_seconds)
    audio_structure(audio_frames, data_index["Audios"])

    # Generate and process frames for images
    image_frames = tf.generate_time_frames(total_duration_seconds, clip_duration_seconds)
    image_structure(image_frames, data_index["Images"])

    # add the meta data at the last tooo
    vs.add_video("meta_data.png", tf.convert_sec_to_time_frame(total_duration_seconds),
                 tf.convert_sec_to_time_frame(total_duration_seconds + 1), meta_data_dir)

    # Create output folder with a unique name
    folder_name = f"Brainrot_{datetime.date.today()}_{time.strftime('%H%M%S', time.localtime())}"
    output_folder_path = os.path.abspath(os.path.join(output_directory, folder_name))
    os.makedirs(output_folder_path)

    # Define filenames for video structure and final video
    video_structure_filename = f"{folder_name}_video_structure.json"
    final_video_filename = f"{folder_name}_final_video.mp4"

    # Write video structure to file
    rw.write_to_file(os.path.join(output_folder_path, video_structure_filename), vs.get_video_structure())

    # Read the video structure back from file
    video_structure_data = rw.read_file(os.path.join(output_folder_path, video_structure_filename))

    # Initialize the video editor
    video_editor = Editor()

    # Create a clip using the video structure
    video_editor.create_clip_using_video_structure(video_structure_data)

    # Composite the final video and audio
    final_video = video_editor.composite_video()
    final_audio = video_editor.composite_audio()

    # Add the audio to the video
    final_video_with_audio = video_editor.set_audio(final_video, final_audio)

    # Write the final video to the output folder
    rw.write_to_file(os.path.join(output_folder_path, final_video_filename), final_video_with_audio)



    # todo
    # add a "from" - "to" for a video so that it takes a random portion of the video.
    # change the algorithm that decided how many videos to take






    # data_idx = rw.read_file(os.path.join(data_idx_dir, "data_index.json"))
    #
    # total_duration = 10
    # clip_duration = 1
    #
    # frames = tf.generate_time_frams(total_duration, clip_duration)
    # video_structure(frames, data_idx["Videos"])
    #
    # frames = tf.generate_time_frams(total_duration, clip_duration)
    # audio_structure(frames, data_idx["Audios"])
    #
    # frames = tf.generate_time_frams(total_duration, clip_duration)
    # image_structure(frames, data_idx["Images"])
    #
    # folder_name = "Brainrot_" + str(datetime.date.today()) + "_" + str(time.strftime("%H%M%S", time.localtime()))
    #
    # full_path = os.path.abspath(os.path.join(output_dir, folder_name))
    #
    # os.makedirs(full_path)
    #
    # vid_struct_file_name = folder_name + "vid_struct.json"
    # vid_file_name = folder_name + "brccs_vid.mp4"
    #
    # rw.write_to_file(os.path.join(full_path, vid_struct_file_name), vs.get_video_structrue())
    #
    # video_struct = rw.read_file(os.path.join(full_path, vid_struct_file_name))
    #
    # editor = Editor()
    #
    # editor.create_clip_using_video_struc(video_struct)
    #
    # final_vid = editor.composite_video()
    # final_audio = editor.composite_audio()
    #
    # final_vid = editor.set_audio(final_vid, final_audio)
    #
    # rw.write_to_file(os.path.join(full_path, vid_file_name), final_vid)