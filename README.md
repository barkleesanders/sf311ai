# sf311ai

Open-vocabulary issue detection from images using YOLO-World. Preview detections before configuring any city submission.

## Features
- **YOLO-World**: Uses open-vocabulary object detection (text prompts) for 311 issues (e.g., "trash pile", "graffiti")
- **No Training Required**: Just specify detection prompts in `config.yaml`—no custom weights or data labeling needed
- **Submission adapter**: Maps prompts to configured service codes. The supplied API URL and codes are placeholders; city acceptance is not verified.
- **Modular Python Package**: Easy to extend, test, and deploy
- **CI/CD Ready**: Linting, tests, packaging, and release automation

## Quickstart
1. **Clone and Install**
   ```sh
   git clone https://github.com/barkleesanders/sf311ai.git
   cd sf311ai
   # Python 3.11 or newer (required by patched Pillow)
   python3 -m venv venv && source venv/bin/activate
   pip install .
   ```
2. **Configure**
   - Copy `.env.example` to `.env` and add your SF311 API key
   - Edit `config.yaml` to set detection prompts and API details
3. **Run Workflow**
   ```sh
   sf311ai config.yaml images/
   ```

## Configuration
- `config.yaml`:
  - `yolo_world_detection_classes`: List of detection prompts (text, e.g. "trash pile")
  - `prompt_to_service_code`: Maps prompts to SF311 service codes
- `.env`: Set `SF311_API_KEY` for submission only.
- `image_locations`: Map each image filename to its verified `lat` and `long`.
  Submission rejects missing, nonfinite, out-of-range, and `0,0` coordinates
  before processing any image in the batch. No GPS extraction is implemented.

The CLI emits a JSON preview by default. Once the actual API URL, service codes,
credentials, and image locations have been verified, `--submit` explicitly enables
submission. It must be used only for reports you intend to file. Failed HTTP
responses and timeouts stop the batch; unknown outcomes are never retried.
The adapter's multipart transport is tested against a local HTTP server;
this does not establish the city's API contract or successful case creation.

The original `yolo_world/l` configuration resolves to `yolov8l-worldv2.pt`.
Official weight filenames and local weight paths are also accepted. Initial model
use downloads YOLO-World and CLIP weights. The CLIP source dependency is pinned
by commit and archive hash, rather than installed from a floating Git branch at
runtime. Real local inference has been checked with bus/person prompts on the
SDK sample and a blank-image negative control; this is not validation of the
accuracy of the supplied civic-issue prompts.

Install development tools with `pip install '.[dev,browser]'`. The optional
browser extra installs Playwright's Python package; it does not install or launch
browsers.

## Development
- Format: `black .`
- Lint: `flake8 .`
- Type check: `mypy`
- Test: `pytest --cov=sf311ai`

## SF311 Form Automation
The repository also includes `submit_sf311.py` which automates submitting online
forms on the official SF311 website using Playwright. Create a `config.json`
mapping each form slug to its required field values and run:

```sh
python submit_sf311.py --config config.json
```

Use the `--show` flag to launch the browser in headed mode for debugging. Each
submission confirmation is appended to `submissions.csv` and any errors are
logged to `errors.log`.

## License
Project source: MIT © 2025 Barklee Sanders.

Ultralytics and its CLIP fork are separate AGPL-3.0 dependencies; see
[Ultralytics licensing](https://www.ultralytics.com/license) and the
[pinned CLIP license](https://github.com/ultralytics/CLIP/blob/7ffa84b3bfa40c42ecc1c77147a855e69cb2dd40/LICENSE).
The registry vulnerability audit does not cover the direct CLIP GitHub dependency;
its pinned source and integrity require separate review.
