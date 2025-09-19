from main import summarize_long_text, record_audio
import whisper



default_ai_model = "turbo"
model = whisper.load_model(default_ai_model)

default_audio_filename = "finished_recording.wav"
default_transcription_file = "transcription.txt"

freq = 44100


def save_transcription(text, transcription_filename):
    with open(transcription_filename, 'w') as f:
        f.write(f"TRANSCRIPTION:\n{text}")


# AUDIO FUNCTIONS

def transcribe_audio_file(settings):
    try:
        filename = settings.get("audio_filename", default_audio_filename)
        transcription_filename = settings.get("transcription_file", default_transcription_file)
        result = model.transcribe(filename)
        text = result["text"]
        

        save_transcription(text, transcription_filename)
    except UnicodeEncodeError as e:
        print(f"Could not transcribe your audio. Please try again.\nError Code: {e}")


def summarize_audio_file(settings):
    try:
        filename = settings.get("audio_filename", default_audio_filename)
        transcription_filename = settings.get("transcription_file", default_transcription_file)
        result = model.transcribe(filename)
        text = result["text"]
        summary = summarize_long_text(text)
        
        save_transcription(summary, transcription_filename)
    except UnicodeEncodeError as e:
        print(f"Could not transcribe your audio. Please try again.\nError Code: {e}")