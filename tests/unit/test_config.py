import os
import tempfile
import yaml
from sf311ai.config import Config

def test_config_load():
    config_yaml = {
        "paths": {"output_dir": "output/", "log_file": "sf311ai.log"},
        "ai_params": {
            "confidence_threshold": 0.4,
            "yolo_world_model_variant": "yolo_world/l",
            "yolo_world_detection_classes": ["trash pile", "graffiti"]
        },
        "api_client": {
            "base_url": "http://example.com",
            "prompt_to_service_code": {"trash pile": "S0331"}
        }
    }
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tf:
        yaml.dump(config_yaml, tf)
        tf_path = tf.name
    os.environ["SF311_API_KEY"] = "testkey"
    config = Config(tf_path)
    assert config.paths["output_dir"] == "output/"
    assert config.ai_params["confidence_threshold"] == 0.4
    assert config.api_client["base_url"] == "http://example.com"
    assert config.sf311_api_key == "testkey"
