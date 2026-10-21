"""Opt-in real inference check without invoking submission."""

import argparse
import hashlib
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory

import cv2
import numpy as np
import ultralytics
from ultralytics import settings

from sf311ai.ai_detector_yoloworld import YOLOWorldAIDetector


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--weights", default="yolov8l-worldv2.pt")
    args = parser.parse_args()
    weights = Path(args.weights)
    if weights.is_file():
        weights = weights.resolve()
    image = Path(ultralytics.__file__).parent / "assets" / "bus.jpg"
    settings.update({"sync": False})
    previous = Path.cwd()
    with TemporaryDirectory(prefix="sf311ai-model-smoke-") as folder:
        try:
            os.chdir(folder)
            blank = Path(folder) / "blank.png"
            if not cv2.imwrite(str(blank), np.zeros((640, 640, 3), np.uint8)):
                raise RuntimeError("Cannot create blank control")
            detector = YOLOWorldAIDetector(
                str(weights), ["bus", "person"], 0.4
            )
            positive = detector.detect(str(image))
            negative = detector.detect(str(blank))
            if (
                not {"bus", "person"}.issubset({d["prompt"] for d in positive})
                or negative
            ):
                raise AssertionError({"positive": positive, "blank": negative})
            print(
                json.dumps(
                    {
                        "sdk": ultralytics.__version__,
                        "weights_sha256": hashlib.sha256(
                            weights.read_bytes()
                        ).hexdigest(),
                        "positive": positive,
                        "blank": negative,
                    }
                )
            )
        finally:
            os.chdir(previous)


if __name__ == "__main__":
    main()
