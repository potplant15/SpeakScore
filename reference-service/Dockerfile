FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg libgomp1 espeak-ng \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

ENV KOKORO_MODEL_PATH=/root/kokoro-models/kokoro-v1.0.onnx \
    KOKORO_VOICES_PATH=/root/kokoro-models/voices-v1.0.bin

VOLUME ["/root/kokoro-models"]

EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
