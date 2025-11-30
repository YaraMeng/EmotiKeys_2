# EmotiKeys — Emotion Music Canvas

EmotiKeys is an experimental web application that transforms a user's mouse movement across a canvas into real-time musical output. By exploring different emotional zones on the canvas (Happy, Calm, Tense, Sad), users can create, preview and record short emotional music pieces.

## Table of Contents

- Demo
- Music Interaction Flow
- Project Overview
- Tech Stack
- File Structure
- Setup & Launch Guide

## Demo

Add a short demo GIF or an embedded video link here.

## Music Interaction Flow

1.  Open the webpage: the browser loads the application interface.
2.  Free exploration (preview mode):
    - Move the mouse across the canvas. When the cursor enters different emotional zones (Happy, Calm, Tense, Sad), the app will synthesize and play music according to the preset scale/parameters for that zone.
    - During preview mode the audio is not recorded — you can freely explore sounds.
3.  Start composing (recording mode):
    - Click the "Start" button to begin recording the generated audio.
    - Continue exploring the canvas to create melodies and textures.
4.  Stop composing: click the "Pause" (or Stop) button to end the recording.
5.  Save: after recording, click the "Save" button to download your composition as a `.wav` file.

## Project Overview

The goal of EmotiKeys is to provide an intuitive music creation tool that requires no formal music-theory knowledge. The canvas is divided into four diagonal emotional regions. Mouse movement within each region triggers notes, chords and harmonic textures that match the region's mood. Users can preview these sounds in real time and optionally record and download their creations.

## Tech Stack

- Backend: Python, FastAPI, Uvicorn
- Frontend: HTML5, CSS3, Vanilla JavaScript
- Audio synthesis: Tone.js
- Animation: GSAP (GreenSock)

## File Structure

```
.
├── backend/                # FastAPI backend code
│   └── app/
│       ├── routes/         # API routes
│       └── main.py         # FastAPI application entry point
├── head09_test/            # Frontend files (served by backend)
│   ├── assets/             # images, icons and other static assets
│   ├── app.js              # main JavaScript logic
│   ├── index.html          # frontend entry page
│   └── styles.css          # stylesheet
├── .gitignore
├── README.md
└── requirements.txt        # Python dependencies
```

## Setup & Launch Guide

Follow these steps to run the project locally.

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd EmotiKeys_2
```

### 2. Create and activate a Python virtual environment

Windows:

```powershell
python -m venv .venv
.venv\\Scripts\\Activate.ps1
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the backend (serves APIs and frontend static files)

```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

The `--host 0.0.0.0` option allows other devices on the same LAN to access the service.

### 5. Open the application

Open one of the following in your browser:

- Local: `http://localhost:8000`
- LAN device: `http://<server-ip>:8000`

Note: Sensitive features such as microphone and screen-audio capture require a secure context (HTTPS) or `localhost` in most browsers. Accessing the app via an IP address over the LAN may restrict those features.

## Troubleshooting & Notes

- If you cannot record audio from a remote device, try opening the app on the server machine using `http://localhost:8000` to confirm the feature works locally.
- If you want LAN devices to use microphone/screen recording, consider setting up HTTPS (self-signed cert for dev) and configuring `uvicorn` to use TLS, or host the app behind a reverse proxy that provides HTTPS.

