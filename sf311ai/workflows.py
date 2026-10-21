from pathlib import Path

from .ai_detector_yoloworld import YOLOWorldAIDetector
from .api_client import SF311APIClient
from .config import Config
from .data_utils import load_images_from_folder
from .locations import validate_location


def process_images_and_report(
    config_path: str, image_folder: str, *, submit: bool = False
):
    config = Config(config_path)
    images = load_images_from_folder(image_folder)
    # Validate the entire batch before loading weights or making any request.
    locations = (
        {
            p: validate_location(config.image_locations.get(Path(p).name))
            for p in images
        }
        if submit
        else {}
    )
    if submit:
        missing = [
            p
            for p in config.ai_params["yolo_world_detection_classes"]
            if not config.api_client["prompt_to_service_code"].get(p)
        ]
        if missing:
            raise ValueError(f"Missing configured service codes: {missing}")
    api_client = SF311APIClient(config) if submit else None
    detector = YOLOWorldAIDetector(
        model_variant=config.ai_params["yolo_world_model_variant"],
        detection_prompts=config.ai_params["yolo_world_detection_classes"],
        confidence_threshold=config.ai_params["confidence_threshold"],
    )
    preview = []
    for img_path in images:
        detections = detector.detect(img_path)
        for det in detections:
            preview.append({"image": img_path, **det})
            if api_client is not None:
                api_client.submit_report(
                    det["prompt"], locations[img_path], img_path
                )
    return preview
