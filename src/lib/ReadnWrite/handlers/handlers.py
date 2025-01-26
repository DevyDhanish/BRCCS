from .filehandler import FileHandler

from .jsonhandler import JsonHandler
from .texthandler import TextHandler
from .imagehandler import ImageHandler
from .videohandler import VideoHandler
from .audiohandler import AudioHandler

def _get_handler(handler_type) -> FileHandler:
    handlers = {
        "json" : JsonHandler(),
        "txt" : TextHandler(),
        "png" : ImageHandler(),
        "jpeg" : ImageHandler(),
        "gif" : ImageHandler(),
        "jpg" : ImageHandler(),
        "mp3" : AudioHandler(),
        "mp4" : VideoHandler(),
    }

    try:
        handler = handlers[handler_type]
        return handler

    except KeyError:
        print(f"Handler for type {handler_type} does not exist")