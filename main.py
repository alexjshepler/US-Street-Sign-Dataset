import os
import shutil

from Image import Image

from tqdm import tqdm
from flask import Flask, request, jsonify

app = Flask(__name__)

# Define directories
DATASET_DIR = 'Datasets'
UNPROCESSED_DIR = "static/images/unprocessed"
SAVED_DIR = "static/images/saved"
DISCARDED_DIR = "static/images/discarded"

# Global variable to store image paths
images = []
curr_index = 0
# ========== Flask Functions ==========


@app.route("/")
def index():
    # Serve the main HTML file
    return app.send_static_file("index.html")


@app.route("/image/<int:index>", methods=["GET"])
def get_image(index):
    global images, curr_index

    # Validate the index
    if index < 0 or index >= len(images):
        return jsonify({"message": "No more images", "image_url": None})

    # Get the image file path
    image_file = images[index].path
    curr_index = index
    image_url = f"/{image_file}"  # Path relative to `static`

    return jsonify(
        {
            "message": f"Showing image {index + 1} of {len(images)}",
            "image_url": image_url,
        }
    )


@app.route("/keypress", methods=["POST"])
def keypress():
    data = request.json
    key = data.get("key")

    # Log the key press for debugging
    print(f"{key} | Current Index: {curr_index:09d} | Image Path: {images[curr_index].path}")

    if key.lower() == 'j':
        images[curr_index].save()
        
    if key.lower() == 'f':
        images[curr_index].discard()
        
    if key.lower() == 'u':
        images[curr_index].unprocess()
        
    # Add your custom processing logic here
    result = "Key processed successfully"

    return jsonify({"message": "Key processed", "result": result})


# ========== Main Functions ==========


def check_dirs():
    """Ensure the required directories exist."""
    if not os.path.exists(SAVED_DIR):
        os.makedirs(SAVED_DIR)

    if not os.path.exists(DISCARDED_DIR):
        os.makedirs(DISCARDED_DIR)

def move_dataset_images():
    index = 0
    total_images = 0
    
    for root, _, files in os.walk(DATASET_DIR):
        for file in files:
            if os.path.splitext(file)[1] == '.jpg':
                total_images += 1
    
    with tqdm(desc='Moving Images', total=total_images, unit='Image') as pbar:
    
        for root, _, files in os.walk(DATASET_DIR):
            for file in files:
                if os.path.splitext(file)[1] == '.jpg':
                    while os.path.exists(os.path.join(UNPROCESSED_DIR, f'{index:09d}.jpg')):
                        index += 1
                    shutil.move(os.path.join(root, file), os.path.join(UNPROCESSED_DIR, f'{index:09d}.jpg'))
                    index += 1
                    pbar.update(1)

def get_images():
    """Retrieve all .jpg image paths from the dataset directory."""
    image_paths = []

    for root, _, files in os.walk(UNPROCESSED_DIR):
        for file in files:
            if os.path.splitext(file)[1].lower() == ".jpg":
                # Store paths relative to `static/`
                image_paths.append(Image(os.path.join(root, file), file))

    return image_paths


def main():
    """Main setup function."""
    global images

    check_dirs()  # Ensure directories exist
    move_dataset_images()
    images = get_images()  # Load images into the global list

if __name__ == "__main__":
    main()
    app.run(debug=True)
