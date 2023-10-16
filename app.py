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
        
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
    
## docker run -v D:\nor3st\nor3st_AI:/app -p 3000:5000 app