import base64
from flask import Flask, request, send_file, jsonify, send_from_directory
from flask_cors import CORS
from ai_models.my_senior import MySenior
from ai_models.pronunciationAssessment import convert_score, mp32pcm, pronunciation_assessment
from ai_models.voice_vietnamese import korean_to_vietnamse, make_entire_voice
from model.Education import Education
from ai_models.lectureVoiceMaker import lectureVoiceMaker
from ai_models.audioPreprocessing import match_target_amplitude, only_voice
from ai_models.my_senior import MySenior
from ai_models.simulation import Simulation 
import os
from io import BytesIO
from pydub import AudioSegment
import uuid

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=["GET"])
def hello():
    return "hello"


        
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
    
# @app.route("/save_doc", methods=["POST"])
# def save_doc():
#     try:
#         with MySenior(request=request, url="save_doc") as senior:
#             return senior["result"]
        
#     except Exception as e:
#         return jsonify({"error": str(e)})

# @app.route("/question", methods=["POST"])
# def question_to_senior():
#     try:
#         with MySenior(request=request, url="question") as senior:
#             return senior["answer"]
        
#     except Exception as e:
#         return jsonify({"error": str(e)})

@app.route("/get_score", methods=["POST"])
def make_score():
    
    voice = request.files["voice"]
    script = request.form["script"]

    # 파일 없는 경우
    if voice is None:
        return '파일이 존재하지 않습니다.'
    else:  # 파일 있는 경우 
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], voice.filename)
        audio = AudioSegment.from_file(voice).export(file_path, format="mp3")
        
        # 오디오 전처리
        audio_file = AudioSegment.from_mp3(file_path)
        audio_file = match_target_amplitude(audio_file, -11.0)
        preprocessed_audio = only_voice(audio_file)

        score = 0 
        transcribed_text = ""
        
        if preprocessed_audio is None:  # 침묵일 때
            score = 0

        else:
            preprocessed_audio_name = voice.filename.replace('.mp3', '') + '_preprocessed.mp3'
            preprocessed_audio_filepath = os.path.join(app.config['UPLOAD_FOLDER'], preprocessed_audio_name)
            preprocessed_audio.export(preprocessed_audio_filepath, format='mp3')

            # 발음평가
            pcm_file_name = voice.filename.replace('.mp3', '') + '_preprocessed' +  '_pcm.pcm'
            pcm_file_path = os.path.join(app.config['UPLOAD_FOLDER'], pcm_file_name)
            pcm_file = mp32pcm(preprocessed_audio_filepath, pcm_file_path)

            score = pronunciation_assessment(pcm_file, script)
            score = convert_score((float(score)))

            with Education(request, url="text") as result:
                transcribed_text = result["answer"]

        result = {"score": score, "answer": transcribed_text}

        return jsonify(result) 
    

@app.route("/simulation/question", methods=["POST"])
def simulation():
    try:
        voice = request.files["voice"]
        if voice:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], voice.filename)
            voice.save(file_path)
        with Simulation(request=request) as simulation:
            return simulation
        
    except Exception as e:
        return jsonify({"error": str(e)})
    

# @app.route("/get_sentence2voice_viet", methods=["POST"])
# def get_sentence2voice(): 
#     try:
#         # 요청에서 파일과 저장 위치를 가져옵니다.
#         recieved_file = request.files["sentence_file"]
#         file_name = request.form["filename"]

#         # 파일 저장 경로를 설정합니다.
#         filename = f"{file_name}.json"        
#         # recieved_filepath = os.path.join(app.config['UPLOAD_FOLDER'], "lecture_source/prototype", filename)
#         print('\n\n', filename, '\n\n')
#         recieved_filepath = app.config['UPLOAD_FOLDER'] + "/lecture_source/prototype"
#         if not os.path.exists(recieved_filepath):
#             os.makedirs(recieved_filepath)

#         # 파일을 저장합니다. #### 
#         recieved_file.save(recieved_filepath + '/' + filename)
#         final_recieved_filepath = recieved_filepath + '/' + filename

#         lecturevoicemaker = lectureVoiceMaker(final_recieved_filepath, file_name)
#         text = lecturevoicemaker.full_text_list
#         korean = text[0]['korean']  
        
#         voice = lecturevoicemaker.make_entire_voice(korean)
#         vietnamese = lecturevoicemaker.korean_to_vietnamse(korean)

#         # 파일 객체를 읽고 인코딩합니다.
#         audio_data = open(voice, 'rb').read()
#         encoded_audio = base64.b64encode(audio_data).decode()

#         # JSON 응답 생성
#         response_data = {
#             'audio': encoded_audio,
#             'filename': file_name,
#             'vietnamese' : vietnamese
#         }
#         return jsonify(response_data)

#     except Exception as e:
#         return jsonify({"error": str(e)})

@app.route("/get_sentence2voice_viet", methods=["POST"])
def get_sentence2voice(): 
    try:
        korean = request.form["korean"]
        # korean = data.decode('utf-8')

        voice = make_entire_voice(korean)
        vietnamese = korean_to_vietnamse(korean)

        # 파일 객체를 읽고 인코딩합니다.
        audio_data = open(voice, 'rb').read()
        encoded_audio = base64.b64encode(audio_data).decode()

        # JSON 응답 생성
        response_data = {
            'audio': encoded_audio,
            'vietnamese' : vietnamese
        }
        return jsonify(response_data)

    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/simulation/question_text", methods=["POST"])
def simulation_text():
    try:
        voice = request.files["voice"]
        if voice:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], "simulation_test.mp3")
            audio = AudioSegment.from_file(voice).export(file_path, format="mp3")

        with Simulation(request=request) as simulation:
            return simulation

    except Exception as e:
        return jsonify({"error": str(e)})
    