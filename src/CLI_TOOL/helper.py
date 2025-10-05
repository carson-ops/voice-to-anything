from main import summarize_long_text
import os
import time
import numpy as np
import whisper
from scipy.io.wavfile import write
import sounddevice as sd
import keyboard
from gpt4all import GPT4All


default_ai_model = "turbo"
model = whisper.load_model(default_ai_model)
int_model =  GPT4All("Phi-3-mini-4k-instruct.Q4_0.gguf")

# START OF DEFAULT DIRECTORIES
default_filename = "finished_recording.wav"
default_audio_filename = "M_0880_14y6m_1.wav"
default_transcription_file = "transcription.txt"

review_dir = "Reivew"
os.makedirs(review_dir, exist_ok=True) # wow how could I overlook this

default_notes_file = os.path.join(review_dir, "notes.txt") # Review/notes.txt
default_calendar_file = os.path.join(review_dir, "calendar_dates.txt")
# END OF DEFAULT DIRECTORIES

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


def save_transcription(text, transcription_filename):
    save_option = input("\nWould you like to save this transcription/summarization? (y/n): ").lower()
    if save_option == 'y':
        with open(transcription_filename, "w", encoding="utf-8") as f:
            f.write(f"TRANSCRIPTION: \n{text}")
    elif save_option == 'n':
        print("Transcription not saved.")
    else:
        print("Invalid input. Transcription not saved.")

# AUDIO FUNCTIONS

def transcribe_audio(settings):
    clear_console()
    filename = settings.get("filename", default_filename)
    transcription_filename = settings.get("transcription_file", default_transcription_file)

    print("Recording... Press 'Enter' to end recording\n")

    record_audio(filename) # read above function for details

    clear_console()

    # Transcribe w/ Whisper
    result = model.transcribe(filename)
    text = result["text"]
    clear_console()

    print(text)
    save_transcription(text, transcription_filename)

    notes_file = settings.get("notes_file", default_notes_file)
    calendar_file = settings.get("calendar_file", default_calendar_file)
    calendar_notes(text, notes_file, calendar_file)

    return


def transcribe_audio_file(settings):
    clear_console()
    filename = settings.get("audio_filename", default_audio_filename)
    transcription_filename = settings.get("transcription_file", default_transcription_file)
    result = model.transcribe(filename)
    text = result["text"]

    print(result["text"])
    save_transcription(text, transcription_filename)

    notes_file = settings.get("notes_file", default_notes_file)
    calendar_file = settings.get("calendar_file", default_calendar_file)
    calendar_notes(text, notes_file, calendar_file)

    return


def summarize_audio(settings):
    clear_console()
    filename = settings.get("filename", default_filename)
    transcription_file = settings.get("transcription_file", default_transcription_file)

    print("Recording... Press 'Enter' to end recording\n")
    record_audio(filename)  # read above function for details

    clear_console()

    result = model.transcribe(filename)
    text = result["text"]
    summary = summarize_long_text(text)
    print(f"SUMMARY: \n{summary}\n")

    save_transcription(summary, transcription_file)

    notes_file = settings.get("notes_file", default_notes_file)
    calendar_file = settings.get("calendar_file", default_calendar_file)
    calendar_notes(text, notes_file, calendar_file)
    

    return

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

    notes_file = settings.get("notes_file", default_notes_file)
    calendar_file = settings.get("calendar_file", default_calendar_file)
    calendar_notes(text, notes_file, calendar_file)

    return

def calendar_notes(text, notes_file, calendar_file):

    notes_userin = input("\nDo you want to scan this transcription/summarization for notes (will be stored in a .txt file)? (y/n): ").lower()
    if notes_userin == 'y' or notes_userin == 'yes':
        output = int_model.generate(f"Store the notes using a dash and newlines. Scan this text for any Notes to review.:\n{text}\n If no meaningful notes are found then say, No important notes found.")
        output = output.partition("<|endoftext|>")[0] # kill the stupid nonsense generation that it does to reach token quota | also took longer than expected because I forgot to assign a output again to this line -_-
        # print(output)
        with open(notes_file, "w") as f:
            f.write(output)
    else:
        pass

    calendar_userin = input("\nDo you want to scan this transcription/summarization for Calendar plans (will be stored in a .txt file)? (y/n): ").lower()
    if calendar_userin == 'y' or calendar_userin == 'yes':
        output = int_model.generate(f"Scan this text for important events to put in a calendar:\n{text}\nIf there is important calenar events store it like this, Date | Time | Event/Plan; state this first then put the calendar events. If there is not any important events then say, No important events found.")
        output = output.partition("<|endoftext|>")[0] # Used .partition() instead of .split() because we only need to stop at index before <|endoftext|> we dont need to keep finding more <|endoftext|> after we already found one, why? because we "delete" everything after the 1st <|endoftext|>
        # print(output)
        with open(calendar_file, "w") as f:
            f.write(output)
    else:
        pass