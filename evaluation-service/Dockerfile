FROM python:3.12-slim

WORKDIR /app

ENV PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple

RUN sed -i 's@deb.debian.org@mirrors.aliyun.com@g' /etc/apt/sources.list.d/debian.sources 2>/dev/null || true \
    && apt-get -o Acquire::Retries=3 update \
    && apt-get install -y --no-install-recommends ffmpeg espeak-ng libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir -r requirements.txt

COPY app ./app

ENV OPENPRONOUNCE_DEVICE=cpu \
    HF_HOME=/root/.cache/huggingface

VOLUME ["/root/.cache/huggingface"]

EXPOSE 8002

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]
