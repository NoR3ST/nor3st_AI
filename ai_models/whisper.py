import whisper

class Whisper(object):
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Whisper, cls).__new__(cls)
            cls._instance.MODEL = whisper.load_model("tiny")
            
        return cls._instance