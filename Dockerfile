FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install --no-install-recommends -y libgl1 libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*
COPY . .
RUN python -m pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu && \
    python -m pip install --no-cache-dir . && python -m pip check
CMD ["sf311ai", "--help"]
