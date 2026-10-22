# AI Healthcare Assistant with Vision and Voice

An **educational multimodal AI health-information demo** built with **Gradio** and the **Groq API**. Users can record or upload an audio question, optionally upload a photo, and receive a text answer and a spoken response.

> **Medical disclaimer:** This is a software demonstration, not a medical device. Its outputs are not diagnoses or treatment recommendations. Do not rely on it for emergencies or clinical decisions. Avoid uploading identifying or sensitive patient information unless you have appropriate authorization and privacy safeguards.

## Features

- Record audio in the browser or upload an existing audio file.
- Transcribe speech with Groq Whisper.
- Analyze an uploaded image using an **image-capable** Groq model.
- Generate a concise, cautious health-information response.
- Convert the response to WAV speech using Groq Orpheus (`daniel` male voice).
- Play the response in a Gradio web interface.

## Project structure

```text
p5_healcare_vlm_stt/
├── vision_analyzer.py      # Image encoding and LLM requests
├── vision_analyzer.py     # Groq speech-to-text
├── text_to_speech.py      # Groq text-to-speech
├── gradio_app.py               # Browser UI and orchestration
├── requirements.txt
├── README.md
└── .env                        # Local secret; do not commit
```

## Requirements

- Python 3.10+ (Python 3.12 works with appropriately compatible installed packages)
- A Groq API key and internet access
- Access to the selected Groq models in your organization
- A modern browser with microphone permission for browser recording

No `sudo`, PyAudio, PortAudio, `sounddevice`, FFmpeg, gTTS, or ElevenLabs is needed for the **browser-based** pipeline described here.

## Installation

From the project folder:

```bash
python3 -m venv .venv
source .venv/bin/activate           # Linux/macOS
python -m pip install -r requirements.txt
```

For Windows, activate with `.venv\Scripts\activate`.

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Keep this key private. Add `.env`, `.venv/`, `__pycache__/`, and generated `.wav` files to `.gitignore` before pushing the repository.

## Configure Groq models

Model IDs and availability change. Check [Groq's model list](https://console.groq.com/docs/models) and [vision docs](https://console.groq.com/docs/vision) before running. Set the model IDs in your scripts to models **available to your organization** and compatible with each task.

| Task | Example setting | File |
|---|---|---|
| Speech recognition | `whisper-large-v3` | `voice_of_the_patient.py` / `gradio_app.py` |
| Image + text reasoning | A Groq model explicitly supporting **image inputs** | `gradio_app.py` |
| Speech synthesis | `canopylabs/orpheus-v1-english` | `voice_of_the_doctor.py` |
| Speech voice | `daniel` (male; **not guaranteed Indian-accented**) | `voice_of_the_doctor.py` |

**Important:** The example `qwen/qwen3.8-27b` discussed during development must be checked for *image input support* and availability in your Groq console before use. Do not substitute a text-only model for a vision model.

The Orpheus model may require organization-admin approval of its terms. If you see `model_terms_required`, visit the link returned in the API error (often [Orpheus Playground](https://console.groq.com/playground?model=canopylabs%2Forpheus-v1-english)) and ask the organization admin to accept the terms.

## Run the web app

```bash
python gradio_app.py
```

Open the local URL printed by Gradio (often `http://127.0.0.1:7860`).

1. Record a question using the browser microphone or upload an audio recording.
2. Optionally upload an image.
3. Submit the request.
4. Review the transcription, text response, and generated voice.

If Python is on a remote machine, forward the Gradio port over SSH, e.g. `ssh -L 7860:127.0.0.1:7860 user@server`. The browser handles microphone recording; the remote Python server does not need microphone drivers.

## Run individual components

```bash
python voice_of_the_doctor.py
```

This calls Groq TTS and saves `doctor_voice.wav` if model access is enabled. To test speech recognition, place a supported recording in your project folder and call `transcribe_with_groq("whisper-large-v3", "patient_voice_test.wav")` from Python.

## Common errors

| Error | What to do |
|---|---|
| `model_terms_required` | Have the Groq organization admin accept the selected model's terms. |
| `model_not_found` or unsupported image input | Check the model ID and capabilities in your Groq console; select a currently available vision model. |
| `PortAudio library not found` | Use Gradio browser recording; do not import `sounddevice` in the browser workflow. |
| `BinaryAPIResponse` has no `.content` | Use `response.read()` or `response.write_to_file(path)` for Groq binary speech output. |
| WAV header / `struct.error` | For short TTS output, save directly; when combining WAV chunks, construct the output format carefully and do not carry over an invalid frame count. |
| `GROQ_API_KEY` missing | Check `.env` location and spelling, then restart the process. |
| Browser microphone unavailable | Allow microphone access and use `localhost`/HTTPS as appropriate. |

## Technical notes

- The TTS module splits long responses to respect the model's per-request text limit. Test chunk merging against your installed SDK and model output format.
- For multiple simultaneous requests, create a unique temporary output filename for each response; avoid sharing one fixed `doctor_response.wav` filename.
- Restrict file type/size, securely handle uploads, clean up temporary files, and add authentication before deploying publicly.
- An AI-generated response should not claim a confirmed diagnosis from an image or impersonate a licensed clinician.

## Resources

- [Groq documentation](https://console.groq.com/docs/overview)
- [Groq Speech-to-Text](https://console.groq.com/docs/speech-to-text)
- [Groq Text-to-Speech](https://console.groq.com/docs/text-to-speech)
- [Gradio documentation](https://www.gradio.app/docs)

## License

Add a license file of your choosing before redistributing this project.
