import datetime
import os.path
import time
import random

from .lib.ReadnWrite.RnW import ReaderAndWriter
from .lib.BRCCS.videostructure import VideoStructure
from .lib.BRCCS.timeutils import TimeUtils
from .lib.BRCCS.editor import Editor
from .lib.BRCCS.filestypes import IMAGE, AUDIO, VIDEO

vs = VideoStructure()
rw = ReaderAndWriter()

# def video_structure(frames, video_pool : list):
#
#     for frame in frames:
#         rand_video = video_pool[random.randint(0, len(video_pool) - 1)]
#         vs.add_video(rand_video["name"], tf.convert_sec_to_time_frame(frame[0]), tf.convert_sec_to_time_frame(frame[1]), rand_video["path"])
#
# def audio_structure(frames, audio_pool : list):
#     for frame in frames:
#         rand_video = audio_pool[random.randint(0, len(audio_pool) - 1)]
#         vs.add_audio(rand_video["name"], tf.convert_sec_to_time_frame(frame[0]), tf.convert_sec_to_time_frame(frame[1]), rand_video["path"])
#
# def image_structure(frames, image_pool : list):
#     for frame in frames:
#         rand_video = image_pool[random.randint(0, len(image_pool) - 1)]
#         vs.add_video(rand_video["name"], tf.convert_sec_to_time_frame(frame[0]), tf.convert_sec_to_time_frame(frame[1]), rand_video["path"])


def add_asset_info(density, asset_pool, of_type):

    for i in range(density):

        if of_type == VIDEO or of_type == IMAGE:
            rand_idx = random.randint(0, len(asset_pool) - 1)
            vs.add_video(asset_pool[rand_idx]["name"],
                         TimeUtils.seconds_to_timestamp(0),
                         TimeUtils.seconds_to_timestamp(0),
                         TimeUtils.seconds_to_timestamp(0),
                         TimeUtils.seconds_to_timestamp(0),
                         asset_pool[rand_idx]["path"],
                         random.choice(["left", "right", "center"]),
                         random.choice(["top", "bottom", "center"]),
                         of_type)
        else:
            rand_idx = random.randint(0, len(asset_pool) - 1)
            vs.add_audio(asset_pool[rand_idx]["name"],
                         TimeUtils.seconds_to_timestamp(0),
                         TimeUtils.seconds_to_timestamp(0),
                         TimeUtils.seconds_to_timestamp(0),
                         TimeUtils.seconds_to_timestamp(0),
                         asset_pool[rand_idx]["path"],
                         of_type)

def randomize(vid_struct, duration, total_duration):

    vid = vid_struct["Video"]
    aud = vid_struct["Audio"]

    # video
    for vids in vid:

        if vids["of_type"] == IMAGE:
            start = random.randint(0, total_duration - duration)
            end = start + duration
            vids["start_at"] = TimeUtils.seconds_to_timestamp(start)
            vids["end_at"] = TimeUtils.seconds_to_timestamp(end)

        if vids["of_type"] == VIDEO:
            clip_duration = int(rw.read_file(vids["path"]).duration)
            start = random.randint(0, total_duration - duration)
            end = start + duration
            frm = random.randint(0, abs(clip_duration - duration))
            to = frm + duration

            if clip_duration > duration:
                vids["start_at"] = TimeUtils.seconds_to_timestamp(start)
                vids["end_at"] = TimeUtils.seconds_to_timestamp(end)
                vids["from"] = TimeUtils.seconds_to_timestamp(frm)
                vids["to"] = TimeUtils.seconds_to_timestamp(to)

            else:
                vids["start_at"] = TimeUtils.seconds_to_timestamp(0)
                vids["end_at"] = TimeUtils.seconds_to_timestamp(clip_duration)
                vids["from"] = TimeUtils.seconds_to_timestamp(0)
                vids["to"] = TimeUtils.seconds_to_timestamp(clip_duration)

    # audio

    for auds in aud:

        if auds["of_type"] == AUDIO:
            clip_duration = int(rw.read_file(auds["path"]).duration)
            start = random.randint(0, total_duration - duration)
            end = start + duration
            frm = random.randint(0, abs(clip_duration - duration))
            to = frm + duration

            if clip_duration > duration:

                auds["start_at"] = TimeUtils.seconds_to_timestamp(start)
                auds["end_at"] = TimeUtils.seconds_to_timestamp(end)
                auds["from"] = TimeUtils.seconds_to_timestamp(frm)
                auds["to"] = TimeUtils.seconds_to_timestamp(to)

            else:
                auds["start_at"] = TimeUtils.seconds_to_timestamp(start)
                auds["end_at"] = TimeUtils.seconds_to_timestamp(end)
                auds["from"] = TimeUtils.seconds_to_timestamp(0)
                auds["to"] = TimeUtils.seconds_to_timestamp(round(clip_duration))


def randomize_timestamps(clip_struct, duration, total_duration, rand_strt_end, rand_frm_to):

    # videos length
    clip_duration = Editor.get_clip_duration(rw.read_file(clip_struct["path"]))

    # randomize where the clip will start
    if rand_strt_end:

        # clip can start anywhere between 0 and total_duration - duration
        clip_struct["start_at"] = TimeUtils.random_timestamp(
            TimeUtils.seconds_to_timestamp(0),
            TimeUtils.seconds_to_timestamp(total_duration - duration)
        )

        # and obv we don't care where it starts from, but it will end after the specified duration
        clip_struct["end_at"] = TimeUtils.seconds_to_timestamp(
            TimeUtils.timestamp_to_seconds(clip_struct["start_at"]) + duration
        )

    if rand_frm_to:

        # if the video is shorter that what we want then just put the whole video
        if clip_duration < duration:
            clip_struct["from"] = TimeUtils.seconds_to_timestamp(0)
            clip_struct["to"] = TimeUtils.seconds_to_timestamp(clip_duration)
            return

        # random part of the video between 0 to video's length
        clip_struct["from"] = TimeUtils.random_timestamp(
            TimeUtils.seconds_to_timestamp(0),
            TimeUtils.seconds_to_timestamp(clip_duration - duration)
        )

        # and obv `end` will be start + duration
        clip_struct["to"] = TimeUtils.seconds_to_timestamp(
            TimeUtils.timestamp_to_seconds(clip_struct["from"]) + duration
        )

def randomize_clip_timestamps(clips, duration, total_duration):

    for clip in clips:
        # for video and audio randomize (start, end) and (from, to)
        # for images js (start, end)

        if clip["of_type"] == IMAGE:
            randomize_timestamps(clip, duration, total_duration, True, False)

        if clip["of_type"] == VIDEO or clip["of_type"] == AUDIO:
            randomize_timestamps(clip, duration, total_duration, True, True)


def generate(total_duration_seconds, clip_duration_seconds, clip_density, audio_density, img_density, data_index_directory, output_directory):
    # Read the data index file
    data_index = rw.read_file(data_index_directory)

    # # add the meta data as the background
    # # meta data directory
    # # the first meta data will decide how long is the video
    # meta_data_dir = os.path.abspath(os.path.join(data_index_directory, "meta_data.png"))

    vs.add_video("meta_data.png",
                 TimeUtils.seconds_to_timestamp(0),
                 TimeUtils.seconds_to_timestamp(total_duration_seconds),
                 TimeUtils.seconds_to_timestamp(0),
                 TimeUtils.seconds_to_timestamp(0),
                 os.path.abspath(os.path.join("src", "meta_data.png")),
                 "center",
                 "center",
                 IMAGE)

    # create a timeline structure with just the asset info
    print(data_index)
    add_asset_info(clip_density, data_index["Videos"], VIDEO)
    add_asset_info(img_density, data_index["Images"], IMAGE)
    add_asset_info(audio_density, data_index["Audios"], AUDIO)
    rw.write_to_file(os.path.join(".", "check.json"), vs.get_timeline_structure())

    # randomize each clips timeframes

    # this is givving us problem
    randomize_clip_timestamps(vs.get_video_structure(), clip_duration_seconds, total_duration_seconds)
    randomize_clip_timestamps(vs.get_audio_structure(), clip_duration_seconds, total_duration_seconds)


    #randomize(vs.get_timeline_structure(), clip_duration_seconds, total_duration_seconds)

    folder_name = f"Brainrot_{datetime.date.today()}_{time.strftime('%H%M%S', time.localtime())}"
    output_folder_path = os.path.abspath(os.path.join(output_directory, folder_name))
    os.makedirs(output_folder_path)

    # Define filenames for video structure and final video
    video_structure_filename = f"{folder_name}_video_structure.json"
    final_video_filename = f"{folder_name}_final_video.mp4"

    # Write video structure to file
    rw.write_to_file(os.path.join(output_folder_path, video_structure_filename), vs.get_timeline_structure())

    #exit()

    # Read the video structure back from file
    video_structure_data = rw.read_file(os.path.join(output_folder_path, video_structure_filename))

    # Initialize the video editor
    video_editor = Editor()
    # Create a clip using the video structure
    video_editor.create_timeline_by_video_structure(video_structure_data)

    # Composite the final video and audio
    final_video = video_editor.composite_video()
    final_audio = video_editor.composite_audio()

    # Add the audio to the video
    final_video_with_audio = video_editor.set_audio(final_video, final_audio)

    # Write the final video to the output folder
    rw.write_to_file(os.path.join(output_folder_path, final_video_filename), final_video_with_audio)





    #randomize(vs.get_video_structure(), clip_duration_seconds, total_duration_seconds)

        #rw.write_to_file("test_out.json", vs.get_video_structure())

        #exit()

        # use a method to populate the video structure

        # # Generate and process frames for videos
        # video_frames = tf.generate_time_frames(total_duration_seconds, clip_duration_seconds)
        # video_structure(video_frames, data_index["Videos"])
        #
        # # Generate and process frames for audio
        # audio_frames = tf.generate_time_frames(total_duration_seconds, clip_duration_seconds)
        # audio_structure(audio_frames, data_index["Audios"])
        #
        # # Generate and process frames for images
        # image_frames = tf.generate_time_frames(total_duration_seconds, clip_duration_seconds)
        # image_structure(image_frames, data_index["Images"])
        #
        # # add the meta data at the last tooo
        # vs.add_video("meta_data.png", tf.convert_sec_to_time_frame(total_duration_seconds),
        #              tf.convert_sec_to_time_frame(total_duration_seconds + 1), meta_data_dir)

    # Create output folder with a unique name

    # todo
    # add a "from" - "to" for a video so that it takes a random portion of the video.
    # change the algorithm that decided how many videos to take






    # not something usefull just to close all the comments i had
    def close_comment():
        pass

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