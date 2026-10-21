import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from types import SimpleNamespace

import pytest

from sf311ai.api_client import SF311APIClient
from sf311ai.locations import validate_location


@pytest.mark.parametrize(
    "location",
    [
        None,
        {},
        {"lat": 0, "long": 0},
        {"lat": 91, "long": 1},
        {"lat": 1, "long": float("nan")},
        {"lat": True, "long": 1},
    ],
)
def test_invalid_location_rejected(location):
    with pytest.raises(ValueError):
        validate_location(location)


def test_multipart_upload_and_rejection(tmp_path):
    requests = []

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            requests.append(
                (
                    self.path,
                    self.rfile.read(int(self.headers["Content-Length"])),
                )
            )
            self.send_response(201 if len(requests) == 1 else 503)
            self.end_headers()
            self.wfile.write(
                json.dumps({"service_request_id": "local-fixture"}).encode()
            )

        def log_message(self, *args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = Thread(target=server.serve_forever)
    thread.start()
    image = tmp_path / "image.jpg"
    image.write_bytes(b"local-fixture-bytes")
    client = SF311APIClient(
        SimpleNamespace(
            api_client={
                "base_url": f"http://127.0.0.1:{server.server_port}",
                "prompt_to_service_code": {"trash pile": "fixture-code"},
            },
            sf311_api_key="fixture-key",
        )
    )
    try:
        assert client.submit_report(
            "trash pile", {"lat": 37.77, "long": -122.4}, str(image)
        ) == {"service_request_id": "local-fixture"}
        assert requests[0][0] == "/requests.json"
        assert b"local-fixture-bytes" in requests[0][1]
        assert b"fixture-code" in requests[0][1]
        assert b"37.77" in requests[0][1]
        with pytest.raises(RuntimeError, match="503"):
            client.submit_report(
                "trash pile", {"lat": 37.77, "long": -122.4}, str(image)
            )
        with pytest.raises(ValueError, match="service code"):
            client.submit_report(
                "unknown", {"lat": 37.77, "long": -122.4}, str(image)
            )
        assert len(requests) == 2
    finally:
        server.shutdown()
        thread.join()
        server.server_close()
