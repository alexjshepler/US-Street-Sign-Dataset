import os

from tqdm import tqdm

import from_dataset
import from_videos

# Input Directories
DATASET_DIR = 'Datasets'
VIDEO_DIR = 'Videos'

# Output Directories
IMAGE_DIR = 'Images'
UNPROCESSED_DIR = 'Images/Unprocessed'
TEMP_DIR = 'Images/temp'

# Move files from dataset to unprocessed
def dataset_images():
    images = from_dataset.get_images(DATASET_DIR)
    from_dataset.move_images(images, UNPROCESSED_DIR)
        
# Convert videos to frames and save in temp files
def video_frames():
    videos = from_videos.get_videos(VIDEO_DIR)
    
    with tqdm(desc='Processing Videos', total=len(videos), unit='Videos') as pbar:
        for i, video in enumerate(videos):
            from_videos.process_video(video, os.path.join(TEMP_DIR, f'{i:04}'))
            pbar.update(1)  
    
# Move temp files to unprocessed

# Remove similar images

# Rename images

def main():
    print('\n==========================\nMoving images from dataset\n==========================\n')
    dataset_images()
    
    print('\n=================\nProcessing Videos\n=================\n')
    video_frames()
    
if __name__ == '__main__':
    main()