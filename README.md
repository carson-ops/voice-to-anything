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
2. Go into the src/ directory
3. ```bash
   pip install -r requirements.txt
   ```
**You have setup the environment**

---
# How to Run
## CLI Tool
1. Go into src/CLI_TOOL
2. Run main.py

## Docker Tool
1. Go into src/DOCKER_TOOL
2. ```bash
   docker build -t voice-to-anything .
   ```
3. All this is, is building a Docker image file to run our app on that container.
4. Now to actually run the program is easy.
5. ```bash
   docker run --rm voice-to-anything --args
   ```
6. --rm remvoes the running container after it is no longer running. Optional.
7. Replace --args with the arguments of your choice.
ARGS
- **TAudioR**: Text Audio Recording
- **TAudioF**: Text Audio File
- **SAudioR**: Summarize Audio Recording
- **SAudioF**: Summarize Audio File
