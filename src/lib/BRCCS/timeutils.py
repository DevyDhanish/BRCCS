import random
import time

from src.lib.Logger.logger import Logger

class TimeUtils:

    # /* this is old and not used any more*\
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

    # converts seconds to "%H:%M:%S" format
    @staticmethod
    def seconds_to_timestamp(sec):
        try:
            return time.strftime("%H:%M:%S", time.gmtime(sec))
        except TypeError:
            Logger.logerr(f"{sec} is in wrong format nigga.")
            return 0

    # converts "%H:%M:%S" to seconds
    @staticmethod
    def timestamp_to_seconds(time_stamp):

        try:
            time_struct = time.strptime(time_stamp, "%H:%M:%S")
            return time_struct.tm_hour * 3600 + time_struct.tm_min * 60 + time_struct.tm_sec
        except TypeError:
            Logger.logerr(f"{time_stamp} is in wrong format nigga.")
            return ""

        except ValueError:
            Logger.logerr(f"yo ts {time_stamp} does not match format '%H:%M:%S'")
            return ""

    # generated a random timestamp between min and max
    @staticmethod
    def random_timestamp(min_stamp : str, max_stamp : str):

        try:
            min_secs = TimeUtils.timestamp_to_seconds(min_stamp)
            max_secs = TimeUtils.timestamp_to_seconds(max_stamp)

            rand_secs = random.randint(min_secs, max_secs)

            return TimeUtils.seconds_to_timestamp(rand_secs)

        except TypeError:
            Logger.logerr(f"{(min, max)} is in wrong format nigga.")
            return ""

        except ValueError:
            Logger.logerr(f"yo ts {(min, max)} does not match format '%H:%M:%S'")
            return ""
