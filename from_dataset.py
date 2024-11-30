import os
from typing import List
import shutil

from tqdm import tqdm

from utils import is_image

# Find all images
def get_images(dataset_dir: str) -> list:
    images = []
    
    for root, _, files in os.walk(dataset_dir):
        for file in files:
            if is_image(file):
                images.append(os.path.join(root, file))
            
    return images

# Move images
def move_images(images: List[str], output_dir: str) -> None:
    file_counter = 0
    
    for image in tqdm(images, desc='Moving Images', unit='Image'):
        try:
            while os.path.exists(os.path.join(output_dir, f'{file_counter:09}{os.path.splitext(image)[1]}')):
                file_counter += 1
                
            output_file = os.path.join(output_dir, f'{file_counter:09}{os.path.splitext(image)[1]}')
            file_counter += 1
            
            # print(f'Moving: {image} \t To: {output_file}')
            shutil.move(image, output_file)
        except Exception as e:
            print(f'An error occurred with the file: {image} | It produced the error:\n\t{e}')