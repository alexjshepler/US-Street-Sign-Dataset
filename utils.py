import os
from concurrent.futures import ThreadPoolExecutor

from tqdm import tqdm
import cv2
from skimage.metrics import structural_similarity as ssim
from PIL import Image
import imagehash

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
def is_image(file: str) -> bool:
    ext = os.path.splitext(file)[1]
    ext = ext.lower()
    
    if ext in IMAGE_EXT:
        return True
    else:
        return False
    
# Determine if the file is a video
def is_video(file: str) -> bool:
    ext = os.path.splitext(file)[1]
    ext = ext.lower()
    
    if ext in VIDEO_EXT:
        return True
    else:
        return False
    
def compare_images(image1_path: str, image2_path: str) -> int:
    # Load Images
    img1 = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE)
    
    if img1.shape != img2.shape:
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
    return ssim(img1, img2)

def get_image_hash(image_path: str):
    image = Image.open(image_path)
    return imagehash.phash(image)

def process_image(image_path: str):
    try:
        image_hash = get_image_hash(image_path)
    except:
        return None, None
        
    return image_hash, image_path

def image_hash_dict(directory):
    hash_dict = {}
    images = []
    
    for file in tqdm(os.listdir(directory), desc='Finding images', unit=' Image'):
        images.append(os.path.join(directory, file))
        
    with ThreadPoolExecutor() as executor:
        results = list(tqdm(executor.map(process_image, images), total=len(images), desc='Hashing Image'))
        
    none_type = 0
    with tqdm(total=len(images)) as pbar:
        for image_hash, image_path in results:
            if image_hash is not None:
                if image_hash in hash_dict:
                    hash_dict[image_hash].append(image_path)
                else:
                    hash_dict[image_hash] = [image_path]
            else:
                print('None type')
                none_type += 1
                
        pbar.update(1)
                
    total_images = len(images)
    total_hashes = len(hash_dict)
    total_difference = total_images - total_hashes
    print(f'Total None types: {none_type}')
    print(f'Total Images: {total_images}\nTotal Hashes: {total_hashes}\n===== Total Difference: {total_difference} =====')