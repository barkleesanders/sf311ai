import os
import yaml
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self, config_path="config.yaml"):
        with open(config_path, "r") as f:
            data = yaml.safe_load(f)
        self.paths = data["paths"]
        self.ai_params = data["ai_params"]
        self.api_client = data["api_client"]
        self.sf311_api_key = os.getenv("SF311_API_KEY")
