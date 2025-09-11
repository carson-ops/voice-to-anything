# FUTURE UPDATES:
# - Add GUI
# - Add option to choose model size
# - Summarize to important calendar events, notes, meetings, etc.


# import required libraries
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
import whisper
import time
import os 
from transformers import pipeline
import keyboard
import numpy as np

os.system("title VOICE-TO-ANYTHING")

# Sampling frequency
freq = 44100

default_filename = "finished_recording.wav"
default_audio_filename = "M_0880_14y6m_1.wav"
default_transcription_file = "transcription.txt"

default_ai_model = "turbo"
model = whisper.load_model(default_ai_model)

summarization = pipeline("summarization", model="facebook/bart-large-cnn")

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu(settings):
    clear_console()
    print("""           OPTIONS
    [1] Transcribe Audio [Recording]  
    [2] Transcribe Audio [File] 
    [3] Summarize Audio [Recording] | Not in
    [4] Summarize Audio [File] 
    [5] Settings
    [6] Exit

    """)
    choice = input("Enter your choice: ")
    if choice == '1':
        transcribe_audio(settings)
    elif choice == '2':
        transcribe_audio_file(settings)
    elif choice == '3':
        summarize_audio(settings)
    elif choice == '4':
        summarize_audio_file(settings)
    elif choice == '5':
        settings_menu(settings)
    elif choice == '6':
        clear_console()
        os._exit(0)
    else:
        main_menu(settings) 

# FUNCTIONS

def save_transcription(result, transcription_filename):
    save_option = input("\nWould you like to save this transcription? (y/n): ").lower()
    if save_option == 'y':
        with open(transcription_filename, "w") as f:
            f.write(f"TRANSCRIPTION: \n{result['text']}")
    elif save_option == 'n':
        print("Transcription not saved.")
    else:
        print("Invalid input. Transcription not saved.")

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

def chunk_text(text, max_length=3000):
    words = text.split()       # split into individual words ['word1', 'word2', ...]
    chunks = []                # list to store finished chunks
    current_chunk = ""         # string we're currently building

    for word in words: # itterating through each word
        if len(current_chunk) + len(word) + 1 <= max_length: # number length of current chunk + number length of current word + 1 for account space until above max length
            # Add the word to the current chunk (plus a space)
            current_chunk += " " + word
        else:
            # Current chunk is full -> store it
            chunks.append(current_chunk.strip()) # store chunk in list and strip leading spaces.
            # Start a new chunk with this word
            current_chunk = word

    # Add the last chunk if there is one
    if current_chunk: # check remaing text and add it to list of chunks
        chunks.append(current_chunk.strip())

    return chunks

def summarize_long_text(text):
    chunks = chunk_text(text, max_length=3000) # puts text into chunks max 3k characters
    summaries = [] # holds the chunks in a list

    for i, chunk in enumerate(chunks): # loop to summarize each chunk | enum lets us loop over a list and keep track of the index of each item | basically looping over each chunk and keeping track of which chunk we're on
        print(f"Summarizing chunk {i+1}/{len(chunks)}...")
        summary = summarization(
            chunk, max_length=130, min_length=30, do_sample=False
        )[0]['summary_text'] # summarizing process
        summaries.append(summary) # add summary to list

    # Combine partial summaries into one final pass if there are multiple chunks
    combined_summary = " ".join(summaries)
    if len(chunks) > 1: # if we have more thank 1 chunk, summarize the stiched chunks of summaries
        combined_summary = summarization(
            combined_summary, max_length=150, min_length=50, do_sample=False
        )[0]['summary_text']

    return combined_summary


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

# CONFIGURATION / SETTINGS

def settings_menu(settings):
    clear_console()
    print(f"""         SETTINGS
    [1] Change Filename | Current: {settings['filename']}
    [2] Change Transcription File | Current: {settings['transcription_file']}
    [3] Change Audio File | Current: {settings['audio_filename']}
    [4] Back to Main Menu

    """)
    choice = input("Enter your choice: ")
    if choice == '1':
        new_filename = input("Enter new filename (with .wav extension): ").strip()
        settings['filename'] = new_filename
        settings_menu(settings)
    elif choice == '2':
        new_transcription_file = input("Enter new transcription filename (with .txt extension): ").strip()
        settings['transcription_file'] = new_transcription_file
        settings_menu(settings)
    elif choice == '3':
        new_audio_file = input("Enter new audio filename (with .wav extension): ").strip()
        settings['audio_filename'] = new_audio_file
        settings_menu(settings)
    elif choice == '4':
        main_menu(settings)
    else:
        settings_menu(settings) # restart settings if invalid input

if __name__ == "__main__":
    settings = {
        "filename": default_filename,
        "audio_filename": default_audio_filename,
        "transcription_file": default_transcription_file
    }
    main_menu(settings)