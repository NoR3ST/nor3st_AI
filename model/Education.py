from ai_models.whisper import Whisper
import logging as log
log.getLogger(__name__)
log.basicConfig(level=log.DEBUG)
log.basicConfig(level=log.DEBUG, format="'%(asctime)s - %(message)s'")


class Education:
    def __init__(self, request, url = None):
        self.model = Whisper().MODEL
        self.student_voice = request.files["voice"]
        self.url = url
        self.result = {}
        
    def __enter__(self):
        if self.url == "text":
            self.result["answer"] = self.user_voice_to_text()
            return self.result

    def __exit__(self, exc_type, exc_value, traceback):
        pass
    
    
    def user_voice_to_text(self):
        return self.model.transcribe(f'static/{self.student_voice.filename}')