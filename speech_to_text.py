# voice_of_the_patient.py


import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def transcribe_with_groq(stt_model, audio_filepath):

    with open(audio_filepath, "rb") as audio:
        response = client.audio.transcriptions.create(
            model=stt_model,
            file=audio,
            language="en"
        )

    return response.text

# Speech-to-text model
stt_model = "whisper-large-v3"

# Test transcription
if __name__ == "__main__":
    audio_filepath = "patient_voice_test.wav"

    if os.path.isfile(audio_filepath):
        transcription = transcribe_with_groq(stt_model, audio_filepath)
        print("Patient:", transcription)
    else:
        print(f"Audio file not found: {audio_filepath}")