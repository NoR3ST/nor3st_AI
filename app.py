from flask import Flask, request, send_file
from model.Education import Education
import os

app = Flask(__name__)


UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=["GET"])
def hello():
    return "hello"

@app.route('/get_answer', methods=["GET"])
def get_answer():
    
    voice = request.files["voice"]
    if voice:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], voice.filename)
        voice.save(file_path)
        
    with Education(request) as model:
        model.user_voice_to_text()
        transcribed_text = model.result["answer"]
        return transcribed_text
        
