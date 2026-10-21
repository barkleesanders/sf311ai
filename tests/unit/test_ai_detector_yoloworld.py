from unittest.mock import patch

import numpy as np
import pytest
import torch
from ultralytics.engine.results import Results

from sf311ai.ai_detector_yoloworld import YOLOWorldAIDetector


def test_detector_uses_official_result_tensors():
    result = Results(
        np.zeros((16, 16, 3), dtype=np.uint8),
        path="dummy.jpg",
        names={0: "trash pile", 1: "graffiti"},
        boxes=torch.tensor([[1, 2, 3, 4, 0.8, 0], [5, 6, 7, 8, 0.3, 1]]),
    )
    with patch("ultralytics.YOLOWorld") as sdk:
        sdk.return_value.predict.return_value = [result]
        detector = YOLOWorldAIDetector(
            "yolo_world/l", ["trash pile", "graffiti"], 0.4
        )
        sdk.assert_called_once_with("yolov8l-worldv2.pt")
        sdk.return_value.set_classes.assert_called_once_with(
            ["trash pile", "graffiti"]
        )
        detections = detector.detect("dummy.jpg")
    assert len(detections) == 1
    assert detections[0]["prompt"] == "trash pile"
    assert detections[0]["bbox"] == [1, 2, 3, 4]
    assert detections[0]["confidence"] == pytest.approx(0.8)


@pytest.mark.parametrize(
    "prompts,threshold", [([], 0.4), ([""], 0.4), (["bus"], -1), (["bus"], 2)]
)
def test_invalid_detection_parameters(prompts, threshold):
    with pytest.raises(ValueError):
        YOLOWorldAIDetector("yolo_world/l", prompts, threshold)
