import subprocess
import logging as log
log.getLogger(__name__)
log.basicConfig(level=log.DEBUG)
log.basicConfig(level=log.DEBUG, format="'%(asctime)s - %(message)s'")


class Education:
    def __init__(self, request, url = None):
        self.student_voice = request.files["voice"].filename
        if not self.student_voice:
            self.student_voice = "simulation_test.wav"
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
            f'static/{self.student_voice}',
            '--language',
            'Korean',
            '--model',
            'tiny'
        ]
        try:
            result = subprocess.run(command, check=True)
            filename = f"{self.student_voice.split('.')[0]}.txt"
            if self.student_voice == "simulation_test.wav":
                filename = "simulation_test.txt"
            with open(filename, 'r') as result:            
                return result.read().replace("\n", "")
        except subprocess.CalledProcessError as e:
            return (f"오류 발생: {e}")
