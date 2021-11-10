import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "C:/Users/LENOVO PC/Downloads/qwiklabs-gcp-04-d1bbb64f28a3-891e3b96c684.json"

from google.cloud import texttospeech
#from google.cloud import translate
from google.cloud import translate_v2 as translate

##Convert one language to another.

translate_client = translate.Client()

Lang_List = translate_client.get_languages()

# Detects the Facts about the text

output = translate_client.translate('Andrea is my best friend.', target_language='fr', model='base')

# To print the Results

print(u"Text: {}".format(output["input"]))

translated_text = output["translatedText"]

print(u"Translation: {}".format(translated_text))

print(u"Detected source language: {}".format(output
["detectedSourceLanguage"]))

print(u"Model: {}".format(output["model"]))


##Convert Translated Text to Speech

# Instantiates a client
tts_client = texttospeech.TextToSpeechClient()

# Set the text input to be synthesized
synthesis_input = texttospeech.SynthesisInput(text = translated_text)

# Build the voice request, select the language code ("en-US") and the ssml
# voice gender ("neutral")
voice = texttospeech.VoiceSelectionParams(
    language_code="fr-CA", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)

# Select the type of audio file you want returned
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

# Perform the text-to-speech request on the text input with the selected
# voice parameters and audio file type
response = tts_client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)

# The response's audio_content is binary.
with open("output.mp3", "wb") as out:
    # Write the response to the output file.
    out.write(response.audio_content)
    print('Audio content written to file "output.mp3"')






