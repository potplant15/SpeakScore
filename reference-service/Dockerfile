FROM python:3.12-slim

WORKDIR /app

ENV PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple

RUN sed -i 's@deb.debian.org@mirrors.aliyun.com@g' /etc/apt/sources.list.d/debian.sources 2>/dev/null || true \
    && apt-get -o Acquire::Retries=3 update \
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
