import from_dataset

# Input Directories
DATASET_DIR = 'Datasets'
VIDEO_DIR = 'Videos'

# Output Directories
IMAGE_DIR = 'Images'
UNPROCESSED_DIR = 'Images/Unprocessed'
TEMP_DIR = 'Images/temp'

# Move files from dataset to unprocessed

# Convert videos to frames and save in temp files

# Move temp files to unprocessed

# Remove similar images

# Rename images

def main():
    images = from_dataset.get_images(DATASET_DIR)
    from_dataset.move_images(images, UNPROCESSED_DIR)

if __name__ == '__main__':
    main()