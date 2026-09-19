FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl ffmpeg libgomp1 espeak-ng \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

ENV KOKORO_MODEL_PATH=/root/kokoro-models/kokoro-v1.0.onnx \
    KOKORO_VOICES_PATH=/root/kokoro-models/voices-v1.0.bin \
    KOKORO_MODEL_URL=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/kokoro-v1.0.onnx \
    KOKORO_VOICES_URL=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/voices-v1.0.bin

VOLUME ["/root/kokoro-models"]

COPY docker-entrypoint.sh ./docker-entrypoint.sh

EXPOSE 8001

CMD ["sh", "./docker-entrypoint.sh"]
