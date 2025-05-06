import cv2
import os
from typing import List

def load_images_from_folder(folder: str) -> List[str]:
    images = []
    for filename in os.listdir(folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            images.append(os.path.join(folder, filename))
    return images
