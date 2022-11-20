import whisper

# You can choose your model from - see it on readme file and update the modelname
modelname = "base"
model = whisper.load_model(modelname)

import gradio as gr 
import time

def SpeechToText(audio):
    if audio == None : return "" 
    time.sleep(1)

    audio = whisper.load_audio(audio)
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # Detect the Max probability of language ?
    _, probs = model.detect_language(mel)
    language = max(probs, key=probs.get)

    #  Decode audio to Text
    options = whisper.DecodingOptions(fp16 = False)
    result = whisper.decode(model, mel, options)
    return (language , result.text)


gr.Interface(
    title = 'OpenAI Whisper implementation on Gradio Web UI', 
    fn=SpeechToText, 
    
    inputs=[
        gr.Audio(source="microphone", type="filepath")
    ],
    outputs=[
        "label",
        "textbox",
    ],
    live=True
).launch(
    debug=False,
    share=True
)