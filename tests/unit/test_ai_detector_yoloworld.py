import pytest
from unittest.mock import patch, MagicMock
from sf311ai.ai_detector_yoloworld import YOLOWorldAIDetector

def test_yoloworld_detector_detect():
    prompts = ["trash pile", "graffiti"]
    with patch("sf311ai.ai_detector_yoloworld.YOLOWorldAIDetector.__init__", return_value=None):
        detector = YOLOWorldAIDetector("yolo_world/l", prompts, 0.4)
        detector.model = MagicMock()
        fake_result = [{"class": "trash pile", "score": 0.8, "bbox": [1,2,3,4]}, {"class": "graffiti", "score": 0.3, "bbox": [5,6,7,8]}]
        detector.model.__call__ = MagicMock(return_value=fake_result)
        detector.confidence_threshold = 0.4
        detections = detector.detect("dummy.jpg")
        assert len(detections) == 1
        assert detections[0]["prompt"] == "trash pile"
        assert detections[0]["confidence"] == 0.8
