# Voice-to-Anything Toolkit

Ran off OpenAIs' Whisper library. A Python toolkit that converts voice input into useful outputs:
- Transcription
- Summarization
- Calendar & Note taking | **NOT ADDED IN DOCKER TOOL**

---
# Before we Get Started
- **Docker Tool will not be getting anymore updates.** Would rather focus on updating CLI & GUI.
- **I prioritize updating CLI more than GUI.** New features will come to CLI first, then to GUI.
- All models are ran locally. It might take time to download/load a model.
- I've made 3 versions, you can pick to your liking. Each is a little different.


# Setup
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
2. Run **main.py**
3. You will be prompted options to transcribe or summarize an audio recording or file | **TO CHANGE AUDIO FILE GO TO SETTINGS TAB**
4. After transcription or recording is done you will be asked if you want to save the transcription
5. Then you will be asked if you want to scan your transcription/summarization for Notes
6. Then you will be asked if you want to scan your transcription/summarization for Calendar information
### Settings
- If you see in the main menu there is a Settings tab.
- The settings tab is to change your directories and (or) names
- If your file directory is invalid in Settings than your whichever file directory was invalid will fallback to default. See [Here](https://github.com/carson-ops/voice-to-anything/blob/main/src/CLI_TOOL/helper.py#L16)

---
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
- **--wavfilename**: .WAV Filename Prerecorded, For File (F)
- **--transcript**: Transcript filename

### Default Settings
 - **File Name**: finished_recording.wav
 - **Audio File Name**: M_0880_14y6m_1.wav
 - **Transcription Text Name**: transcription.txt
---

## GUI Tool
1. Run **main.py**
2. Press the blue circular button in the middle of the screen to record
3. Press again to stop recording
4. You will be prompted with 1 box, asking if you would like to transcribe or summarize
5. After choosing you will wait a little bit for the AI to scan for calendar information and note taking.
Adding a settings menu in the future