import sys
from sf311ai.workflows import process_images_and_report

if __name__ == "__main__":
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config.yaml"
    image_folder = sys.argv[2] if len(sys.argv) > 2 else "images/"
    process_images_and_report(config_path, image_folder)
