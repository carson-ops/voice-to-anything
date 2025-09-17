# 1. Start with an official lightweight Python image
FROM python:3.12.5-slim

# 2. Set a working directory inside the container
WORKDIR /app

# 3. Install system-level dependencies (ffmpeg is common for audio projects)
#    - apt-get update: fetches latest package lists
#    - install ffmpeg: so your code can handle audio files if needed
#    - clean up package lists to keep image size small
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libportaudio2 \
    libsndfile1 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy only requirements first (better for build caching)
COPY requirements.txt .

# 5. Install Python dependencies
#    --no-cache-dir avoids caching wheels (reduces image size)
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of the source code into the container
COPY . .

# 7. Specify default command to run when the container starts
#    - Uses "exec form" (list syntax) so it handles signals properly
CMD ["python", "src/DOCKER TOOL/main.py"]
