import os
from typing import List
import ffmpeg
import shutil

from tqdm import tqdm

from utils import is_video
from utils import is_image

# Get the videos
def get_videos(video_dir: str) -> List[str]:
    videos = []
    
    for root, _, files in os.walk(video_dir):
        for file in files:
            if is_video(file):
                videos.append(os.path.join(root, file))
                
    return videos

# Process the video
def process_video(video: str, output_dir: str) -> None:
    
    os.makedirs(output_dir, exist_ok=True)
    try:
        ffmpeg.input(video, hwaccel='cuda').output(os.path.join(output_dir, 'frame_%06d.jpg'), loglevel='panic').run()
    except Exception as ex:
        print(f'Shit hit the fan right about here: {ex}')
        
def move_temp(temp_dir: str, output_dir: str) -> None:
    frames = []
    
    for root, _, files in os.walk(temp_dir):
        for file in files:
            # Check if file is an image
            if is_image(file):
                frames.append(os.path.join(root, file))
                
    image_number = 0
    
    for frame in frames:
        while os.path.exists(os.path.join(output_dir, f'{image_number:09d}{os.path.splitext(frame)[1]}')):
            image_number += 1
            
        output_image = os.path.join(output_dir, f'{image_number:09d}{os.path.splitext(frame)[1]}')
        shutil.move(frame, output_image)
        # print(f'Moving: {frame}\tTo: {output_image}')
        