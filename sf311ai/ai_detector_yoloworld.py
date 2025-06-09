from typing import List, Dict, Any


class YOLOWorldAIDetector:
    def __init__(
        self,
        model_variant: str,
        detection_prompts: List[str],
        confidence_threshold: float = 0.4,
    ):
        from yoloworld import YOLOWorld

        self.model = YOLOWorld(model_variant)
        self.model.set_classes(detection_prompts)
        self.confidence_threshold = confidence_threshold

    def detect(self, image_path: str) -> List[Dict[str, Any]]:
        results = self.model.__call__(image_path)
        detections = []
        for r in results:
            if r["score"] >= self.confidence_threshold:
                detections.append(
                    {"prompt": r["class"], "bbox": r["bbox"], "confidence": r["score"]}
                )
        return detections
