from helper import * 
import json
from transformers import pipeline


os.system("title VOICE-TO-ANYTHING")

summarization = pipeline("summarization", model="facebook/bart-large-cnn")

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu(settings):
    clear_console()
    print("""           OPTIONS
    [1] Transcribe Audio [Recording]  
    [2] Transcribe Audio [File] 
    [3] Summarize Audio [Recording] 
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


def chunk_text(text, max_length=3000): # chunk it
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

def summarize_long_text(text): # put it in chunk -> summarize each chunk -> stich chunk together -> summarize again after stiched
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

# CONFIGURATION / SETTINGS

def settings_menu(settings): # could optimize to use less code down the line
    clear_console()
    print(f"""         SETTINGS
    [1] Change Filename | Current: {settings['filename']}
    [2] Change Transcription File | Current: {settings['transcription_file']}
    [3] Change Audio File | Current: {settings['audio_filename']}
    [4] Reset to Default
    [5] Back to Main Menu

    """)
    choice = input("Enter your choice: ")
    if choice == '1':
        new_filename = input("Enter new filename (with .wav extension): ").strip()
        settings['filename'] = new_filename
        with open("settings.json", "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)
        settings_menu(settings)
    elif choice == '2':
        new_transcription_file = input("Enter new transcription filename (with .txt extension): ").strip()
        settings['transcription_file'] = new_transcription_file
        with open("settings.json", "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)
        settings_menu(settings)
    elif choice == '3':
        new_audio_file = input("Enter new audio filename (with .wav extension): ").strip()
        settings['audio_filename'] = new_audio_file
        with open("settings.json", "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)
        settings_menu(settings)
    elif choice == '4':
        confirm_action = input("ARE YOU SURE YOU WANT TO RESET SETTINGS TO DEFAULT? (y/n): ")
        if confirm_action == 'y' or confirm_action == 'Y':
            settings = {
                "filename": default_filename,
                "audio_filename": default_audio_filename,
                "transcription_file": default_transcription_file
            }
            with open("settings.json", "w", encoding="utf-8") as f:
                json.dump(settings, f, indent=4)
            main_menu(settings)
    elif choice == '5':
        main_menu(settings)
    else:
        settings_menu(settings) # restart settings if invalid input

if __name__ == "__main__":
    if os.path.exists("settings.json"):
        with open("settings.json", "r", encoding="utf-8") as f:
            settings = json.load(f)
    else:
        settings = {
            "filename": default_filename,
            "audio_filename": default_audio_filename,
            "transcription_file": default_transcription_file
        }
        with open("settings.json", "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)
    main_menu(settings)