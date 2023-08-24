import argparse
import os

import gradio as gr
import pyperclip
import whisper
import shutil
import tempfile


available_models = ['tiny.en', 'tiny', 'base.en', 'base', 'small.en', 'small', 'medium.en', 'medium', 'large']

def parse_arguments():
    parser = argparse.ArgumentParser(description="OpenAI Whisper implementation on Gradio Web UI")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    return parser.parse_args()


def load_whisper_model(model_name):
    if model_name not in available_models:
        raise ValueError(f"Invalid model name: {model_name}. Available models: {available_models}")
    return whisper.load_model(model_name)


def process_audio(audio, model):
    if audio is None: return None, None

    # Check if audio is a temporary file object
    if hasattr(audio, 'name'):
        audio_path = audio.name
    else:
        audio_path = audio

    # Ensure the file path is valid
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"File not found: {audio_path}")

    audio = whisper.load_audio(audio_path)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    return mel, model


def detect_language_and_decode(mel, model):
    _, probs = model.detect_language(mel)
    language = max(probs, key=probs.get)
    options = whisper.DecodingOptions(fp16=False)
    result = whisper.decode(model, mel, options)
    return language, result.text


def SpeechToText(audio, file, model_name="base", copy_to_clipboard=False):
    if audio is None and file is None:
        return ("", "")
    input_audio = audio if audio is not None else file
    model = load_whisper_model(model_name)
    mel, model = process_audio(input_audio, model)
    if mel is None: return ("", "")
    language, text = detect_language_and_decode(mel, model)
    if copy_to_clipboard:
        pyperclip.copy(text)
    return language, text


def launch_app(debug):
    print("Starting the Gradio Web UI")
    gr.Interface(
        title='OpenAI Whisper implementation on Gradio Web UI',
        fn=SpeechToText,
        inputs=[
            gr.Audio(source="microphone", type="filepath", label="Microphone"),
            gr.File(type="file", label="Or Drag and Drop Audio File"),
            gr.Dropdown(choices=available_models, label="Model Selection", value="base"),
            gr.Checkbox(label="Copy text to clipboard")
        ],
        outputs=[
            "label",
            "textbox",
        ],
        live=True
    ).launch(debug=debug)


if __name__ == "__main__":
    args = parse_arguments()
    launch_app(debug=args.debug)
