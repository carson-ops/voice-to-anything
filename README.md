# Voice-to-Anything Toolkit

Ran off OpenAIs' Whisper library. A Python toolkit that converts voice input into useful outputs:
- Transcription
- Summarization
- Integrations (calendar, notes, etc.) | **NOT ADDED**

## Setup
To get started follow along.

1. ```bash
   git clone https://github.com/carson-ops/voice-to-anything
   ```
2. ```bash
   pip install -r requirements.txt
   ```
**You have setup the environment**

---
# How to Run
## CLI Tool
1. Go into src/CLI_TOOL
2. Run main.py
3. **Will add more details later**

## Docker Tool
1. Go into src/DOCKER_TOOL
2. ```bash
   docker build -t voice-to-anything .
   ```
3. All this is, is building a Docker image file to run our app on.
4. Now to actually run the program is easy.
5. ```bash
   docker run --rm voice-to-anything --args
   ```
6. --rm removes the running container after it is no longer running. Optional.
7. Replace --args with the arguments of your choice. **Required**
## ARGS
### Functional Args
- **--TAudioR**: Text Audio Recording | Requires a filename
- **--TAudioF**: Text Audio File | Requires a WAV file
- **--SAudioR**: Summarize Audio Recording | Requires a filename
- **--SAudioF**: Summarize Audio File | Requires a WAV file

### Customizable Args
- **--filename**: Recording Filename, for Recordings (R)
- - **--wavfilename**: .WAV Filename Prerecorded, For File (F)
- **--transcript**: Transcript filename

### Default Settings
 - **File Name**: finished_recording.wav
 - **Audio File Name**: M_0880_14y6m_1.wav
 - **Transcription Text Name**: transcription.txt

## GUI Tool
- **Coming Soon**
---
