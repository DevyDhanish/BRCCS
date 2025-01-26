class VideoStructure:

    video_structure = {
        "Video" : [],
        "Audio" : []
    }

    def add_video(self, name, start_at, end_at, frm, to, path, of_type = ""):

        data = {
            "name" : name,
            "start_at" : start_at,
            "end_at" : end_at,
            "from" : frm,
            "to" : to,
            "of_type" : of_type,
            "path" : path
        }

        self.video_structure["Video"].append(data)


    def add_audio(self, name, start_at, end_at, frm, to, path, of_type = ""):

        data = {
            "name" : name,
            "start_at" : start_at,
            "end_at" : end_at,
            "from": frm,
            "to": to,
            "of_type" : of_type,
            "path" : path
        }

        self.video_structure["Audio"].append(data)


    def get_video_structure(self):
        return self.video_structure
