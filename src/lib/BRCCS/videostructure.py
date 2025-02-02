
"""
VideoStructure defines the setup of a video, including which video to play, where to play it from, its duration,
and the placement of elements. The editor.create_video_from_video_structure method uses this structure to create the final .mp4
video

if you wanna do any modification to the video. rather than calling editors methods to modify a video
just modify the video structure and the editor will recreate the video with new changes.
"""
class VideoStructure:

    """
    Example video structure

    {
        "Video" :   # list of all the videos to use
        [
            {
                "name" : "video1"
                .
                .                       # you get understand ts right ?
                "path" : "somewhere"
            }
        ]

        "Audio" :   # same as video but fewer parameters
        [
            {
                "name" : "audio1"
                .
                .
                "path" : "somewhere"
            }
        ]
    }

    """

    timeline_structure = {
        "Video" : [],
        "Audio" : []
    }

    def add_video(self, name : str,
                  start_at : str,
                  end_at : str,
                  frm : str,
                  to : str,
                  path : str,
                  pos_x : str,
                  pos_y : str,
                  of_type = ""):

        # ts
        data = {
            "name" : name,
            "start_at" : start_at,
            "end_at" : end_at,
            "from" : frm,
            "to" : to,
            "pos_x" : pos_x,
            "pos_y" : pos_y,
            "of_type" : of_type,
            "path" : path
        }

        self.timeline_structure["Video"].append(data)


    # Add audio unit
    def add_audio(self, name : str,
                  start_at : str,
                  end_at : str,
                  frm : str,
                  to : str,
                  path : str,
                  of_type = ""):

        # as ts
        data = {
            "name" : name,
            "start_at" : start_at,
            "end_at" : end_at,
            "from": frm,
            "to": to,
            "of_type" : of_type,
            "path" : path
        }

        self.timeline_structure["Audio"].append(data)


    def get_video_structure(self):
        return self.timeline_structure["Video"]

    def get_audio_structure(self):
        return self.timeline_structure["Audio"]

    def get_timeline_structure(self):
        return self.timeline_structure
