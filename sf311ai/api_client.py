import requests
import logging
from typing import Dict, Any
from .config import Config

class SF311APIClient:
    def __init__(self, config: Config):
        self.base_url = config.api_client["base_url"]
        self.prompt_to_service_code = config.api_client["prompt_to_service_code"]
        self.api_key = config.sf311_api_key
        self.logger = logging.getLogger("sf311ai.api_client")

    def submit_report(self, prompt: str, location: Dict[str, float], image_path: str) -> Any:
        service_code = self.prompt_to_service_code.get(prompt)
        if not service_code:
            self.logger.error(f"No service code for prompt: {prompt}")
            return None
        files = {"media": open(image_path, "rb")}
        data = {
            "service_code": service_code,
            "lat": location["lat"],
            "long": location["long"],
            "api_key": self.api_key
        }
        response = requests.post(f"{self.base_url}/requests.json", data=data, files=files)
        if response.status_code == 201:
            self.logger.info(f"Report submitted for {prompt}")
            return response.json()
        else:
            self.logger.error(f"Failed to submit report: {response.text}")
            return None
