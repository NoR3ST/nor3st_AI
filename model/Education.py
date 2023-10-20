from ai_models.whisper import Whisper

class Education:
    def __init__(self, request):
        self.model = Whisper().MODEL
        self.student_voice = request.files["voice"]
        self.result = {}
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        pass
    
    
    def user_voice_to_text(self):
        self.result["answer"] = self.model.transcribe(f'static/{self.student_voice.filename}')


    def user_voice_to_score(self):
	    # self.result["score"] = self.model
        pass