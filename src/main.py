# import required libraries
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
import whisper
import time
import os

# Sampling frequency
freq = 44100

# Recording duration
duration = 5
filename = "C:/Users/carso/OneDrive/Desktop/voice-to-anything/src/finished_recording.wav" # will make automatic later

# Start recorder with the given values 
# of duration and sample frequency
recording = sd.rec(int(duration * freq), 
                   samplerate=freq, channels=1)

# Record audio for the given number of seconds
sd.wait()

# This will convert the NumPy array to an audio
# file with the given sampling frequency
write("recording_test.wav", freq, recording)

# Convert the NumPy array to audio file
audio_file = wv.write(filename, recording, freq, sampwidth=2)
time.sleep(2) # hope this works by waiting for file to be written

model = whisper.load_model("turbo")
result = model.transcribe(filename)
os.system('cls' if os.name == 'nt' else 'clear') # universal clear

print(result["text"])
input("Press Enter to continue...")


# https://www.geeksforgeeks.org/python/create-a-voice-recorder-using-python/