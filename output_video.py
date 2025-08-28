import DaVinciResolveScript as dvr # type: ignore
import xml.etree.ElementTree as ET
import openai
import os
import subprocess
from pathlib import Path
import requests
import time

# Assume OpenAI API key is set in environment variable OPENAI_API_KEY
client = openai.OpenAI()

# Function to format time for SR
def format_time(seconds):
    hour = int(seconds // 3600)
    minute = int((seconds // 60) % 60)
    second = int(seconds % 60)
    millisecond = int((seconds - int(seconds)) * 1000)
    return f"{hour:02}:{minute:02}:{second:02},{millisecond:03d}"

# Get Resolve objects
resolve = dvr.scriptapp("Resolve")
project_manager = resolve.GetProjectManager()
project = project_manager.GetCurrentProject()
media_pool = project.GetMediaPool()
timeline = project.GetCurrentTimeline()
media_storage = resolve.GetMediaStorage()

# Download video from Google Drive URL if not already in project
drive_file_id = "1e-E0kCB9kBcCpwUbXVv2_4y1BYZpmdiW"
download_url = f"https://drive.google.com/uc?export=download&id={drive_file_id}"
local_video_path = os.path.join(os.getcwd(), "input_video.mp4")

if not os.path.exists(local_video_path):
    print("Downloading video from Drive...")
    response = requests.get(download_url)
    with open(local_video_path, "wb") as f:
        f.write(response.content)

# Import video to Media Pool and add to timeline if not present
imported_clips = media_storage.AddItemListToMediaPool(local_video_path)
if not imported_clips:
    print("Failed to import video.")
    exit()
video_item = imported_clips[0]
media_pool.AppendToTimeline([video_item])

# Refresh timeline
timeline = project.GetCurrentTimeline()

# Get the file path of the first video clip in the timeline
video_items = timeline.GetItemListInTrack("video", 1)
if not video_items:
    print("No video clips found in track 1.")
    exit()

clip = video_items[0]  # Assuming the first clip is the main video
media_item = clip.GetMediaPoolItem()
if not media_item:
    print("No media item found for the clip.")
    exit()

video_path = media_item.GetClipProperty("File Path")
if not video_path:
    print("Unable to get video file path.")
    exit()

# Extract audio from video using ffmpeg (assume ffmpeg is installed)
audio_path = os.path.join(os.getcwd(), "extracted_audio.wav")
subprocess.run(["ffmpeg", "-i", video_path, "-vn", "-acodec", "pcm_s16le", "-ar", "16000", audio_path], check=True)

if not os.path.exists(audio_path):
    print("Audio extraction failed.")
    exit()

# Transcribe audio using OpenAI Whisper with timestamps (Tamil language)
with open(audio_path, "rb") as audio_file:
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="verbose_json",
        language="ta",  # Tamil
        timestamp_granularities=["segment"]
    )

# Process transcription to get segments
segments = transcription.segments

# For each segment, convert Tamil text to Tanglish with emojis using GPT
srt_content = ""
index = 1
for segment in segments:
    start = segment['start']
    end = segment['end']
    tamil_text = segment['text'].strip()

    # Use GPT to convert to Tanglish and add emojis
    prompt = f"""
    Convert the following Tamil text to Tanglish (Tamil words in English script).
    Add contextual emojis that reflect the emotions conveyed by tone and content, like 😊 for happy, 😠 for angry, ❤ for love, 😕 for confused.
    Make it a subtitle line. Keep it concise.

    Tamil text: "{tamil_text}"
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    tanglish_subtitle = response.choices[0].message.content.strip()

    # Format SRT entry
    srt_content += f"{index}\n"
    srt_content += f"{format_time(start)} --> {format_time(end)}\n"
    srt_content += f"{tanglish_subtitle}\n\n"
    index += 1

# Save to SRT file
srt_path = os.path.join(os.getcwd(), "subtitles.srt")
with open(srt_path, "w", encoding="utf-8") as f:
    f.write(srt_content)

# Clean up audio file
os.remove(audio_path)

# Import the SRT file into the Media Pool
imported_items = media_storage.AddItemListToMediaPool(srt_path)
if not imported_items:
    print("Failed to import subtitles.srt")
    exit()

subtitle_item = imported_items[0]

# Add a subtitle track if none exists
if timeline.GetTrackCount("subtitle") == 0:
    if not timeline.AddTrack("subtitle"):
        print("Failed to add subtitle track")
        exit()

# Append the subtitle item to the subtitle track
appended_items = media_pool.AppendToTimeline([subtitle_item])
if not appended_items:
    print("Failed to append subtitles to timeline")
    exit()

# IMPORTANT: After script runs, manually style subtitles in Resolve (Edit > Inspector > Subtitle):
# - Color: Yellow (#FFFF00) with black outline for visibility (adjust based on video background).
# - Size: 48-72 pt, bold font.
# - Position: Centered bottom.
# Then re-render if needed.

# Set render settings
render_settings = {
    "TargetDir": "D:\\youtubevlogs\\poml\\output",  # Replace with your output path
    "CustomName": "rendered_video",
    "ExportVideo": True,
    "ExportAudio": True,
    "SelectAllFrames": True
}
if not project.SetRenderSettings(render_settings):
    print("Failed to set render settings")
    exit()

# Set render format and codec (MP4 H.264)
render_formats = project.GetRenderFormats()
if "mp4" in render_formats:
    codecs = project.GetRenderCodecs("mp4")
    if codecs:  # Pick first available codec
        project.SetCurrentRenderFormatAndCodec("mp4", list(codecs.keys())[0])
    else:
        print("No codecs available for MP4")
        exit()
else:
    print("MP4 format not available")
    exit()

# Add and start render job
job_id = project.AddRenderJob()
if not job_id:
    print("Failed to add render job")
    exit()

if not project.StartRendering(job_id):
    print("Failed to start rendering")
    exit()

# Monitor rendering
while project.IsRenderingInProgress():
    print("Rendering in progress...")
    time.sleep(1)

print("Rendering completed. Output: /path/to/output/rendered_video.mp4")