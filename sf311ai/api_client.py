import logging
from typing import Any
from urllib.parse import urlparse

import requests

from .config import Config
from .locations import Location, validate_location


class SF311APIClient:
    def __init__(self, config: Config):
        self.base_url = config.api_client["base_url"]
        self.prompt_to_service_code = config.api_client[
            "prompt_to_service_code"
        ]
        self.api_key = config.sf311_api_key
        self.logger = logging.getLogger("sf311ai.api_client")
        parsed = urlparse(self.base_url)
        if parsed.scheme != "https" and not (
            parsed.scheme == "http"
            and parsed.hostname in {"127.0.0.1", "localhost"}
        ):
            raise ValueError(
                "Configure an HTTPS API base_url before submitting"
            )
        if not self.api_key:
            raise ValueError("SF311_API_KEY is required for submission")

    def submit_report(
        self, prompt: str, location: Location, image_path: str
    ) -> Any:
        location = validate_location(location)
        service_code = self.prompt_to_service_code.get(prompt)
        if not service_code:
            self.logger.error(f"No service code for prompt: {prompt}")
            return None
        data = {
            "service_code": service_code,
            "lat": location["lat"],
            "long": location["long"],
            "api_key": self.api_key,
        }
        with open(image_path, "rb") as image:
            response = requests.post(
                f"{self.base_url.rstrip('/')}/requests.json",
                data=data,
                files={"media": image},
                timeout=(10, 60),
                allow_redirects=False,
            )
        if response.status_code == 201:
            self.logger.info(f"Report submitted for {prompt}")
            return response.json()
        else:
            raise RuntimeError(f"Report rejected: HTTP {response.status_code}")
