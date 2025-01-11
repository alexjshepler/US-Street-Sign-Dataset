import os
import shutil

DATASET_DIR = "Datasets"
UNPROCESSED_DIR = "static/images/unprocessed/"
SAVED_DIR = "static/images/saved"
DISCARDED_DIR = "static/images/discarded"

class Image:
    def __init__(self, path, name):
        self.path = path
        self.name = name

    def save(self):
        print(f'Saving: {self.name}')
        new_path = os.path.join(SAVED_DIR, self.name)
        shutil.move(self.path, new_path)
        self.path = new_path

    def discard(self):
        print(f'Discarding: {self.name}')
        new_path = os.path.join(DISCARDED_DIR, self.name)
        shutil.move(self.path, new_path)
        self.path = new_path

    def unprocessed(self):
        print(f'Unprocessing: {self.name}')
        new_path = os.path.join(UNPROCESSED_DIR, self.name)
        shutil.move(self.path, new_path)
        self.path = new_path
