import os
from typing import List
import ffmpeg
import sys

from tqdm import tqdm

from utils import is_video

# Get the videos
def get_videos(video_dir: str) -> List[str]:
    videos = []
    
    for root, _, files in os.walk(video_dir):
        for file in files:
            if is_video(file):
                videos.append(os.path.join(root, file))
                
    return videos

# Function to process the progress output
def process_progress(progress_output):
    for line in progress_output.splitlines():
        # Check if the line contains any progress information, e.g., frame and time
        if line.startswith('frame='):
            # Overwrite the previous line by printing a carriage return
            sys.stdout.write('\r' + line)
            sys.stdout.flush()
            
# Process the video
def process_video(video: str, output_dir: str) -> None:
    
    os.makedirs(output_dir, exist_ok=True)
    try:
        ffmpeg.input(video, hwaccel='cuda').output(os.path.join(output_dir, 'frame_%06d.jpg'), loglevel='panic').run()
    except Exception as ex:
        print(f'Shit hit the fan right about here: {ex}')