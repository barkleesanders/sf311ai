import pytest
from unittest.mock import patch, MagicMock
from sf311ai.api_client import SF311APIClient
from sf311ai.config import Config

class DummyConfig:
    def __init__(self):
        self.api_client = {
            "base_url": "http://example.com",
            "prompt_to_service_code": {"trash pile": "S0331"}
        }
        self.sf311_api_key = "testkey"

def test_submit_report_success():
    config = DummyConfig()
    client = SF311APIClient(config)
    with patch("requests.post") as mock_post, patch("builtins.open", create=True) as mock_open:
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"result": "ok"}
        mock_post.return_value = mock_response
        mock_open.return_value = MagicMock()
        result = client.submit_report("trash pile", {"lat": 1.0, "long": 2.0}, "dummy.jpg")
        assert result == {"result": "ok"}

def test_submit_report_no_service_code():
    config = DummyConfig()
    client = SF311APIClient(config)
    result = client.submit_report("unknown", {"lat": 1.0, "long": 2.0}, "dummy.jpg")
    assert result is None
