import random
import time

class TimeFrames:
    def generate_time_frames(self, total_duration, clip_duration):

        # if clip_duration == 0:
        #     clip_duration = random.randint(1, total_duration // 2)

        # if clip_density * clip_duration < total_duration:
        #     print(f"Not enough density to generate {total_duration} sec clip, make sure (density * clip duration) >= total duration")
        #     return

        random_clip_duration = False

        if clip_duration == 0:
            random_clip_duration = True
            clip_duration = random.randint(1, total_duration // 2)

        start = 0
        end = clip_duration

        frames = []

        total_sec = 0

        while total_sec < total_duration:

            if random_clip_duration:
                clip_duration = random.randint(1, total_duration // 2)

            total_sec += end - start

            frames.append((abs(start), abs(end)))

            start = end

            if total_duration - start < clip_duration:
                end = start + (total_duration - start)

            else:
                end = start + clip_duration

        return frames

    def convert_sec_to_time_frame(self, sec):
        return time.strftime("%H:%M:%S", time.gmtime(sec))

    def convert_time_frame_to_sec(self, time_frame):
        time_struct = time.strptime(time_frame, "%H:%M:%S")

        return time_struct.tm_hour * 3600 + time_struct.tm_min * 60 + time_struct.tm_sec