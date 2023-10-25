from flask import Flask, request, send_file, jsonify
from model.Education import Education
from ai_models.lectureVoiceMaker import lectureVoiceMaker
from ai_models.chatbot_gpt import MySenior
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
        
    with Education(request, url="text") as result:
        transcribed_text = result["answer"]["segments"][0]["text"]
        return transcribed_text
        
@app.route("/save_sentences_with_voice", methods=["POST"])
def save_sentences_with_voice():
    try:
        # 요청에서 파일과 저장 위치를 가져옵니다.
        recieved_file = request.files["sentence_file"]
        save_location = request.form["save_location"]

        # 파일 저장 경로를 설정합니다.
        filename = f"{save_location}.json"
        recieved_filepath = os.path.join("lecture_source/prototype", filename)

        # 파일을 저장합니다.
        recieved_file.save(recieved_filepath)
        
        meta_data_path = os.path.join("lecture_source/file_meta_data", filename)
        with lectureVoiceMaker(recieved_filepath, save_location) as voiceMaker :
            return jsonify({"code": 200, "message": "File saved successfully", "meta_file_location": meta_data_path})
        
    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route("/save_doc", methods=["POST"])
def save_doc():
    try:
        with MySenior(request=request, url="save_doc") as senior:
            return senior["result"]
        
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/question", methods=["POST"])
def save_doc():
    try:
        with MySenior(request=request, url="question") as senior:
            return senior["answer"]
        
    except Exception as e:
        return jsonify({"error": str(e)})