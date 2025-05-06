import logging
from .config import Config
from .ai_detector_yoloworld import YOLOWorldAIDetector
from .api_client import SF311APIClient
from .data_utils import load_images_from_folder

def process_images_and_report(config_path: str, image_folder: str):
    config = Config(config_path)
    detector = YOLOWorldAIDetector(
        model_variant=config.ai_params["yolo_world_model_variant"],
        detection_prompts=config.ai_params["yolo_world_detection_classes"],
        confidence_threshold=config.ai_params["confidence_threshold"]
    )
    api_client = SF311APIClient(config)
    images = load_images_from_folder(image_folder)
    for img_path in images:
        detections = detector.detect(img_path)
        for det in detections:
            # Example: dummy location; in real use, extract from drone metadata
            location = {"lat": 0.0, "long": 0.0}
            api_client.submit_report(det["prompt"], location, img_path)
