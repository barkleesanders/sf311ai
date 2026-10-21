from unittest.mock import patch

import pytest

from sf311ai.workflows import process_images_and_report


def test_process_images_and_report(tmp_path):
    # Setup dummy config file and image
    config_yaml = tmp_path / "config.yaml"
    config_yaml.write_text("""
paths:
  output_dir: output/
  log_file: sf311ai.log
ai_params:
  confidence_threshold: 0.4
  yolo_world_model_variant: "yolo_world/l"
  yolo_world_detection_classes:
    - "trash pile"
    - "graffiti"
api_client:
  base_url: http://example.com
  prompt_to_service_code:
    "trash pile": "S0331"
    "graffiti": "S0191"
""")
    image_dir = tmp_path / "images"
    image_dir.mkdir()
    img_path = image_dir / "img.jpg"
    img_path.write_bytes(b"fakeimg")
    # Patch detector and API client
    with (
        patch("sf311ai.workflows.YOLOWorldAIDetector") as mock_detector,
        patch("sf311ai.workflows.SF311APIClient") as mock_api_client,
        patch(
            "sf311ai.workflows.load_images_from_folder",
            return_value=[str(img_path)],
        ),
    ):
        instance = mock_detector.return_value
        instance.detect.return_value = [
            {"prompt": "trash pile", "bbox": [1, 2, 3, 4], "confidence": 0.9}
        ]
        api_instance = mock_api_client.return_value
        api_instance.submit_report.return_value = {"result": "ok"}
        process_images_and_report(str(config_yaml), str(image_dir))
        instance.detect.assert_called_once_with(str(img_path))
        mock_api_client.assert_not_called()
        api_instance.submit_report.assert_not_called()

    with (
        patch("sf311ai.workflows.YOLOWorldAIDetector") as detector,
        patch("sf311ai.workflows.SF311APIClient") as client,
    ):
        with pytest.raises(ValueError, match="explicit"):
            process_images_and_report(
                str(config_yaml), str(image_dir), submit=True
            )
        detector.assert_not_called()
        client.assert_not_called()

    with config_yaml.open("a") as stream:
        stream.write(
            "\nimage_locations:\n  img.jpg: {lat: 37.77, long: -122.4}\n"
        )
    with (
        patch("sf311ai.workflows.YOLOWorldAIDetector") as detector,
        patch("sf311ai.workflows.SF311APIClient") as client,
    ):
        detector.return_value.detect.return_value = [
            {"prompt": "trash pile", "bbox": [1, 2, 3, 4], "confidence": 0.9}
        ]
        process_images_and_report(
            str(config_yaml), str(image_dir), submit=True
        )
        client.return_value.submit_report.assert_called_once_with(
            "trash pile", {"lat": 37.77, "long": -122.4}, str(img_path)
        )
