FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml ./
COPY . .

RUN pip install --upgrade pip && \
    pip install .[dev]

CMD ["python", "scripts/run_workflow.py", "config.yaml", "images/"]
