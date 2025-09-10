# FUTURE UPDATES:
# - Add GUI
# - Add option to save text file of transcription
# - Add option to choose recording duration & stop and start button
# - Add option to choose model size
# - Summarize to important calendar events, notes, meetings, etc.


# import required libraries
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
import whisper
import time
import os; os.system("title VOICE-TO-ANYTHING")


# Sampling frequency
freq = 44100

default_duration = 5 # seconds
default_filename = "src/finished_recording.wav"


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu(settings):
    clear_console()
    print("""           OPTIONS
    [1] Transcribe Audio [Recording]
    [2] Transcribe Audio [File] | Not in
    [3] Summarize Audio [Recording] | Not in
    [4] Summarize Audio [File] | Not in
    [5] Settings
    [6] Exit

    """)
    choice = input("Enter your choice: ")
    if choice == '1':
        transcribe_audio(settings)
    elif choice == '2':
        pass
    elif choice == '5':
        settings_menu(settings)


def transcribe_audio(settings):
    clear_console()
    duration = settings.get("duration", default_duration)
    filename = settings.get("filename", default_filename)

    print(f"Recording for {duration} seconds...")

    if duration == None:
        recording = sd.rec(int(default_duration * freq), 
                        samplerate=freq, channels=1)
    else:
        recording = sd.rec(int(duration * freq), 
                        samplerate=freq, channels=1)

    # Record audio for the given number of seconds
    sd.wait()
    clear_console()

    # This will convert the NumPy array to an audio
    # file with the given sampling frequency
    write(filename, freq, recording)

    # Convert the NumPy array to audio file
    audio_file = wv.write(settings["filename"], recording, freq, sampwidth=2)
    time.sleep(2) # hope this works by waiting for file to be written


    # https://www.geeksforgeeks.org/python/create-a-voice-recorder-using-python/

    # Transcribe w/ Whisper
    model = whisper.load_model("turbo")
    result = model.transcribe(filename)
    clear_console()

    print(result["text"])
    input("Press Enter to continue...")

    main_menu(settings) # END of function


def settings_menu(settings):
    clear_console()
    print(f"""         SETTINGS
    [1] Change Filename | Current: {settings['filename']}
    [2] Change Duration | Current: {settings['duration']} seconds
    [3] Back to Main Menu

    """)
    choice = input("Enter your choice: ")
    if choice == '1':
        new_filename = input("Enter new filename (with .wav extension): ").strip()
        settings['filename'] = new_filename
    elif choice == '2':
        new_duration = int(input("Enter new duration (in seconds): ")).strip()
        settings['duration'] = int(new_duration)
    elif choice == '3':
        main_menu(settings)
    else:
        settings() # restart settings if invalid input

if __name__ == "__main__":
    settings = {
        "duration": default_duration,
        "filename": default_filename
    }
    main_menu(settings)