from flask import Flask, render_template, redirect, url_for, request
import requests
import json
import boto3
from google.cloud import translate_v2 as translate
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "gcpcreds.json"

app = Flask(__name__)

def texttospeech(text):
    # This function here takes the text input and creates audio file for it
    # AWS Polly
    from botocore.config import Config
    polly = boto3.client('polly',config=Config(region_name='us-east-1'))
    response = polly.synthesize_speech(Text = text, VoiceId = 'Joanna', OutputFormat = 'mp3')
    file = open('static/audio/speech.mp3', 'wb')
    file.write(response['AudioStream'].read())
    file.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
      f = request.files['file']
      f.save(f.filename)
      print(f)
      with open(f.filename, 'r') as k:
        lines = k.read()
        k.close()
      texttospeech(lines)
      return '<script>alert("Audio file prepared!");</script>'
    return render_template('index.html')

@app.route('/translation', methods=['GET', 'POST'])
def translation():
    if request.method == 'POST':
        text = request.form['translate_text']
        target_language = 'es'
        print(text)
        translate_client = translate.Client()
        lang_list = translate_client.get_languages()
        # print(lang_list)
        output = translate_client.translate(text, target_language=target_language, model='base')
        print(output)
        ot = output['translatedText']
        # texttospeech(ot)
    return render_template('translation.html', ot=ot)
    
if __name__ == '__main__':
	app.run(debug=True)