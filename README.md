# sf311ai

Open-vocabulary 311 issue detection from drone video using YOLO-World and automated reporting to SF311.

## Features
- **YOLO-World**: Uses open-vocabulary object detection (text prompts) for 311 issues (e.g., "trash pile", "graffiti")
- **No Training Required**: Just specify detection prompts in `config.yaml`—no custom weights or data labeling needed
- **SF311 Integration**: Maps detections to official SF311 service codes and submits reports
- **Modular Python Package**: Easy to extend, test, and deploy
- **CI/CD Ready**: Linting, tests, packaging, and release automation

## Quickstart
1. **Clone and Install**
   ```sh
   git clone https://github.com/barkleesanders/sf311ai.git
   cd sf311ai
   python3 -m venv venv && source venv/bin/activate
   pip install -r requirements.txt  # or use pyproject.toml if available
   ```
2. **Configure**
   - Copy `.env.example` to `.env` and add your SF311 API key
   - Edit `config.yaml` to set detection prompts and API details
3. **Run Workflow**
   ```sh
   python scripts/run_workflow.py config.yaml images/
   ```

## Configuration
- `config.yaml`:
  - `yolo_world_detection_classes`: List of detection prompts (text, e.g. "trash pile")
  - `prompt_to_service_code`: Maps prompts to SF311 service codes
- `.env`: Set `SF311_API_KEY`

## Development
- Format: `black .`
- Lint: `flake8 .`
- Type check: `mypy .`
- Test: `pytest --cov=sf311ai`

## License
MIT © 2025 Barklee Sanders
