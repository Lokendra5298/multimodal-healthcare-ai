# gradio_app.py


import os
import gradio as gr
from dotenv import load_dotenv

from vision_analyzer import encode_image, analyze_image_with_query
from speech_to_text import transcribe_with_groq
from text_to_speech import text_to_speech_with_groq

load_dotenv()

# Models
STT_MODEL = "whisper-large-v3"
VISION_MODEL = "qwen/qwen3.8-27b"

SYSTEM_PROMPT = """
You are an AI health information assistant.

Describe relevant visible findings and possible explanations
without claiming a confirmed diagnosis.

Provide safe, general advice and recommend medical evaluation
when appropriate. Mention urgent warning signs if relevant.

Use simple, compassionate English.
Keep your response concise, preferably two or three sentences.
Do not claim to be a real doctor.
"""

def process_inputs(audio_filepath, image_filepath):

    if not audio_filepath and not image_filepath:
        raise gr.Error("Please record audio or upload an image.")

    # Step 1: Speech to Text
    transcription = ""

    if audio_filepath:
        transcription = transcribe_with_groq(
            STT_MODEL,
            audio_filepath
        )

    # Step 2: Generate AI response
    query = f"""
    {SYSTEM_PROMPT}

    Patient's question: {transcription or 'Describe the uploaded image.'}
    """

    doctor_response = analyze_image_with_query(
        query=query,
        model=VISION_MODEL,
        encoded_image=encode_image(image_filepath) if image_filepath else None,
        image_path=image_filepath
    )

    # Step 3: Text to Speech
    audio_output = text_to_speech_with_groq(
        doctor_response,
        "doctor_response.wav"
    )

    return transcription, doctor_response, audio_output


# Gradio Interface
iface = gr.Interface(
    fn=process_inputs,

    inputs=[
        gr.Audio(
            sources=["microphone", "upload"],
            type="filepath",
            label="Patient Voice"
        ),

        gr.Image(
            type="filepath",
            label="Upload Medical Image"
        )
    ],

    outputs=[
        gr.Textbox(label="Patient Speech to Text"),
        gr.Textbox(label="AI Health Assistant Response"),
        gr.Audio(label="Doctor Voice", type="filepath")
    ],

    title="AI Doctor with Vision and Voice",

    description=(
        "Record your symptoms or upload an image to receive "
        "AI-generated health information with a spoken response. "
        "This educational application does not provide medical diagnoses."
    ),

    flagging_mode="never"
)

if __name__ == "__main__":
    iface.launch()