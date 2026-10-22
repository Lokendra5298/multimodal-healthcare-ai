# voice_of_the_doctor.py


import os
import io
import wave
import textwrap
from dotenv import load_dotenv
from groq import Groq

# Initialize Groq
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

tts_model = "canopylabs/orpheus-v1-english"


def text_to_speech_with_groq(input_text, output_filepath):

    # Split long text into chunks
    chunks = textwrap.wrap(
        input_text,
        width=180,
        break_long_words=True
    )

    if not chunks:
        raise ValueError("Input text cannot be empty.")

    # For short text, save directly
    if len(chunks) == 1:
        response = client.audio.speech.create(
            model=tts_model,
            voice="daniel",
            input=chunks[0],
            response_format="wav"
        )

        response.write_to_file(output_filepath)
        print(f"Audio saved: {output_filepath}")
        return output_filepath

    # For long text, combine audio chunks
    audio_parts = []
    audio_params = None

    for chunk in chunks:
        response = client.audio.speech.create(
            model=tts_model,
            voice="daniel",
            input=chunk,
            response_format="wav"
        )

        with wave.open(io.BytesIO(response.read()), "rb") as wav:
            params = wav.getparams()

            if audio_params is None:
                audio_params = params
            elif params[:4] != audio_params[:4]:
                raise ValueError("Incompatible audio formats.")

            audio_parts.append(wav.readframes(wav.getnframes()))

    # Save combined WAV
    with wave.open(output_filepath, "wb") as output:
        output.setparams(audio_params._replace(nframes=0))

        for audio in audio_parts:
            output.writeframesraw(audio)

    print(f"Audio saved: {output_filepath}")
    return output_filepath


# Test
if __name__ == "__main__":

    input_text = "Hello, I am your AI doctor. How can I help you today?"
    output_filepath = "doctor_voice.wav"
    text_to_speech_with_groq(input_text, output_filepath)