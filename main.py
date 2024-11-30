import os
import concurrent.futures

from tqdm import tqdm

import from_dataset
import from_videos

import utils

# Input Directories
DATASET_DIR = 'Datasets'
VIDEO_DIR = 'Videos'

# Output Directories
IMAGE_DIR = 'Images'
TEMP_DIR = 'Images/temp'
UNPROCESSED_DIR = 'Images/Unprocessed'
PROCESSED_DIR = 'Images/Processed'

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
def move_temp():
    from_videos.move_temp(TEMP_DIR, UNPROCESSED_DIR)

# Remove similar images
def remove_similar():
    utils.image_hash_dict(UNPROCESSED_DIR)
    
# Rename images

def main():
    print('\n==========================\nMoving images from dataset\n==========================\n')
    dataset_images()
    
    print('\n=================\nProcessing Videos\n=================\n')
    # video_frames()
    
    print('\n=============\nMoving Frames\n=============\n')
    move_temp()
    
    print('\n=======================\nRemoving Similar Images\n=======================\n')
    remove_similar()
    
        
if __name__ == '__main__':
    main()