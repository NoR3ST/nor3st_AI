import subprocess
import logging as log
log.getLogger(__name__)
log.basicConfig(level=log.DEBUG)
log.basicConfig(level=log.DEBUG, format="'%(asctime)s - %(message)s'")


class Education:
    def __init__(self, request, voice_path, url = None):
        self.student_voice_path = voice_path
        self.url = url
        self.result = {}
        
    def __enter__(self):
        if self.url == "text":
            self.result["answer"] = self.user_voice_to_text()
            return self.result

    def __exit__(self, exc_type, exc_value, traceback):
        pass
    
    
    def user_voice_to_text(self):
        command = [
            'whisper',
            f'{self.student_voice_path}',
            '--language',
            'Korean',
            '--model',
            'tiny'
        ]
        try:
            result = subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            return (f"오류 발생: {e}")
