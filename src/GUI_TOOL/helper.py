from main import summarize_long_text, record_audio
import os
import time
import numpy as np
import whisper
from scipy.io.wavfile import write
import sounddevice as sd



default_ai_model = "turbo"
model = whisper.load_model(default_ai_model)

default_filename = "finished_recording.wav"
default_audio_filename = "M_0880_14y6m_1.wav"
default_transcription_file = "transcription.txt"

freq = 44100


def save_transcription(text, transcription_filename):
    with open(transcription_filename, 'w') as f:
        f.write(f"TRANSCRIPTION:\n{text}")

# AUDIO FUNCTIONS

def transcribe_audio(settings):
    filename = settings.get("filename", default_filename)
    transcription_filename = settings.get("transcription_file", default_transcription_file)

    print("Recording... Press 'Enter' to end recording\n")

    audio = record_audio(filename) # read above function for details



    # Transcribe w/ Whisper
    result = model.transcribe(audio)
    

    print(result["text"])
    save_transcription(result, transcription_filename)



def transcribe_audio_file(settings):
    
    filename = settings.get("audio_filename", default_audio_filename)
    transcription_filename = settings.get("transcription_file", default_transcription_file)
    result = model.transcribe(filename)
    print(result["text"])
    save_transcription(result, transcription_filename)



def summarize_audio(settings):
    
    filename = settings.get("filename", default_filename)
    transcription_file = settings.get("transcription_file", default_transcription_file)

    print("Recording... Press 'Enter' to end recording\n")
    
    audio = record_audio(filename)  # read above function for details

    

    result = model.transcribe(audio)
    text = result["text"]
    summary = summarize_long_text(text)
    print(f"SUMMARY: \n{summary}\n")

    save_transcription(summary, transcription_file)


def summarize_audio_file(settings):
    
    filename = settings.get("audio_filename", default_audio_filename)
    transcription_filename = settings.get("transcription_file", default_transcription_file)
    result = model.transcribe(filename)
    text = result["text"]
    summary = summarize_long_text(text)
    
    print(f"SUMMARY: \n{summary}\n")
    save_transcription(summary, transcription_filename)
