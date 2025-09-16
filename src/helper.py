import os
import whisper
from transformers import pipeline
from scipy.io.wavfile import write
import sounddevice as sd
import keyboard
import numpy as np
import time
from main import save_transcription, summarize_long_text ,main_menu

default_ai_model = "turbo"
model = whisper.load_model(default_ai_model)

default_filename = "finished_recording.wav"
default_audio_filename = "M_0880_14y6m_1.wav"
default_transcription_file = "transcription.txt"

freq = 44100


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def record_audio(filename): # Enter to stop recording
    
    recording = [] # list to hold chunks of audio data

    with sd.InputStream(samplerate=freq, channels=1, dtype='float32') as stream:
        while True:
            data, overflowed = stream.read(1024) # reads 1024 samples at a time

            # Check if data has something and is not empty
            if data is not None and len(data) > 0:
                recording.append(data)

            if overflowed: # performance issue warning
                print("Warning: Audio buffer overflowed! Not good")

            if keyboard.is_pressed("enter"): # kills recording
                time.sleep(0.5) # slight delay to ensure all data is captured
                print("Recording stopped.")
                break

    # Combine all recorded chunks into a single NumPy array
    audio_data = np.vstack(recording) # switched from concat to vstack. Chuncks is a list of (1024, 1) arrays, so vstack works better because it refuses to add arrays of different dimensions

    # Convert float32 to int16 | GPT assisted
    write(filename, freq, (audio_data * 32767).astype(np.int16)) 
    input(f"Recording saved to {filename} | Press Enter to continue...")
    return filename

# AUDIO FUNCTIONS

def transcribe_audio(settings):
    clear_console()
    filename = settings.get("filename", default_filename)
    transcription_filename = settings.get("transcription_file", default_transcription_file)

    print(f"Recording... Press 'Enter' to end recording\n")

    record_audio(filename) # read above function for details
    
    clear_console()


    # Transcribe w/ Whisper
    result = model.transcribe(filename)
    clear_console()

    print(result["text"])
    save_transcription(result, transcription_filename)

    main_menu(settings) # END of function


def transcribe_audio_file(settings):
    clear_console()
    filename = settings.get("audio_filename", default_audio_filename)
    transcription_filename = settings.get("transcription_file", default_transcription_file)
    result = model.transcribe(filename)
    print(result["text"])
    save_transcription(result["text"], transcription_filename)

    main_menu(settings) # END of function


def summarize_audio(settings): 
    clear_console()
    filename = settings.get("filename", default_filename)
    transcription_file = settings.get("transcription_file", default_transcription_file)

    print(f"Recording... Press 'Enter' to end recording\n")
    record_audio(filename)  # read above function for details

    clear_console()

    result = model.transcribe(filename)
    text = result["text"]
    summary = summarize_long_text(text)
    print(f"SUMMARY: \n{summary}\n")

    save_transcription(summary, transcription_file)

    main_menu(settings) # END of function

def summarize_audio_file(settings):
    clear_console()
    filename = settings.get("audio_filename", default_audio_filename)
    transcription_filename = settings.get("transcription_file", default_transcription_file)
    result = model.transcribe(filename)
    text = result["text"]
    summary = summarize_long_text(text)
    clear_console()
    print(f"SUMMARY: \n{summary}\n")
    save_transcription(summary, transcription_filename)

    main_menu(settings) # END of function