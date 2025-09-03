 ## Audio Extraction – GPT-4 Model – DaVinci Resolve

An end-to-end AI-powered Tamil-to-Tanglish subtitle automation project that combines Python, POML workflow automation, GPT-4 transcription/translation, and DaVinci Resolve editing.

 Features

✅ POML Workflow Parsing – Automates structured process definition.

✅ DaVinci Resolve Integration – Setup connections for media pool and timeline handling.

✅ Audio Extraction – Extracts audio tracks directly from video.

✅ GPT-4 AI Transcription – Converts Tamil audio to text.

✅ Tanglish Conversion – GPT-4 model transforms Tamil text into Tanglish.

✅ SRT Subtitle Generation – Automated subtitle file creation.

✅ Subtitles Import – Directly imports generated SRT into DaVinci Resolve.

✅ Final Output Rendering – Produces video with embedded Tanglish subtitles.

 ## 🛠️Tech Stack

Programming Language: Python

AI Models: GPT-4

Workflow Definition: POML

Video Editor: DaVinci Resolve

Subtitle Handling: SRT files

## 📂Workflow Steps

Parse POML Workflow – Define and load structured process.

Setup DaVinci Connection – Connect Python automation to DaVinci Resolve.

Download Video – Fetch media input.

Import to Media Pool – Add video clips into DaVinci environment.

Add to Timeline – Place media on editing timeline.

Extract Audio – Isolate audio track for transcription.

Transcribe Tamil (GPT-4) – Convert Tamil speech to text.

Convert to Tanglish (GPT-4) – Transform Tamil script into Tanglish format.

Generate SRT – Create subtitle file.

Import Subtitles – Add subtitles into DaVinci Resolve project.

Add Subtitle Track – Sync subtitles with video.

Final Output – Render edited video with Tanglish subtitles.

## 📊Model Workflow

AI Model: GPT-4

Task Type: Speech-to-text + Translation

Integration Tool: Python scripting with DaVinci Resolve API

Automation Language: POML
![WhatsApp Image 2025-08-27 at 22 17 47_dab0f74e](https://github.com/user-attachments/assets/e7851bc5-c3fe-4268-be40-8619826c7faf)

📦 Installation
# Clone repo
git clone https://github.com/yourusername/audio-extraction-gpt4-davinci.git
cd audio-extraction-gpt4-davinci

# Install dependencies
pip install -r requirements.txt

▶️ Usage
python main.py --workflow poml_file.yaml --video input.mp4


This will:

Parse workflow

Extract audio

Transcribe Tamil → Tanglish

Generate & import SRT subtitles

Render final DaVinci Resolve project
