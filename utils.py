import os

IMAGE_EXT = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif', '.tiff', '.webp', '.raw', '.cr2', '.nef', '.arw']
VIDEO_EXT = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm']
AUDIO_EXT = ['.mp3', '.wav', '.flav', '.aac', '.ogg', '.wma', '.aiff']

# Get the type of file
def filetype(file) -> str:
    ext = os.path.splitext(file)[1]
    ext.lower()    
    
    # Image Check
    if ext in IMAGE_EXT:
        return 'image'
        
    # Video Check
    elif ext in VIDEO_EXT:
        return 'video'
    
    else:
        return 'undefined'

# Determine if the file is an image
def is_image(file) -> bool:
    ext = os.path.splitext(file)[1]
    ext.lower()
    
    if ext in IMAGE_EXT:
        return True
    else:
        return False