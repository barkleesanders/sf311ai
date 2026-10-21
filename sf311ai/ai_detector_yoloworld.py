from typing import TypedDict


class Detection(TypedDict):
    prompt: str
    bbox: list[float]
    confidence: float


class YOLOWorldAIDetector:
    def __init__(
        self,
        model_variant: str,
        detection_prompts: list[str],
        confidence_threshold: float = 0.4,
    ):
        if not detection_prompts or any(
            not p.strip() for p in detection_prompts
        ):
            raise ValueError(
                "At least one nonempty detection prompt is required"
            )
        if not 0 <= confidence_threshold <= 1:
            raise ValueError("confidence_threshold must be between 0 and 1")

        from ultralytics import YOLOWorld

        # Preserve the original model size using official weights.
        aliases = {
            "yolo_world/s": "yolov8s-worldv2.pt",
            "yolo_world/m": "yolov8m-worldv2.pt",
            "yolo_world/l": "yolov8l-worldv2.pt",
            "yolo_world/x": "yolov8x-worldv2.pt",
        }
        self.model = YOLOWorld(aliases.get(model_variant, model_variant))
        self.model.set_classes(detection_prompts)
        self.confidence_threshold = confidence_threshold

    def detect(self, image_path: str) -> list[Detection]:
        from ultralytics.engine.results import Results

        results = self.model.predict(
            source=image_path, conf=self.confidence_threshold, verbose=False
        )
        detections: list[Detection] = []
        for result in results:
            if not isinstance(result, Results):
                raise TypeError("YOLO-World returned a non-detection result")
            if result.boxes is None:
                continue
            boxes = result.boxes.cpu()
            for bbox, score, class_id in zip(
                boxes.xyxy.tolist(), boxes.conf.tolist(), boxes.cls.tolist()
            ):
                if score < self.confidence_threshold:
                    continue
                detections.append(
                    {
                        "prompt": result.names[int(class_id)],
                        "bbox": bbox,
                        "confidence": score,
                    }
                )
        return detections
