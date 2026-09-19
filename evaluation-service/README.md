# SpeakScore Evaluation Service

Evaluation Service converts learner audio into a transcript and pronunciation result. It uses faster-whisper for speech recognition, OpenPronounce for phone recognition, and the scoring layer for content, completeness, pronunciation and fluency metrics.

## Requirements

- Python 3.12
- FFmpeg
- Dependencies in `requirements.txt`
- Whisper model
- OpenPronounce model `facebook/wav2vec2-lv-60-espeak-cv-ft`

The default port is `8002`.

## Run locally

```bash
cd evaluation-service
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8002
```

Health check:

```bash
curl http://127.0.0.1:8002/health
```

Direct evaluation request:

```bash
curl -X POST http://127.0.0.1:8002/api/v1/evaluate \
  -F 'reference_text=I would like some water.' \
  -F 'accent=en-US' \
  -F 'audio=@recording.mp3'
```

The service accepts audio formats supported by FFmpeg and limits uploads to 10 MB.

## Model configuration

For a server without reliable Hugging Face access, mount the Whisper model locally:

```yaml
environment:
  WHISPER_MODEL: /models/whisper
  WHISPER_DEVICE: cpu
  WHISPER_COMPUTE_TYPE: int8
  HF_HOME: /root/.cache/huggingface
  HF_HUB_OFFLINE: "1"
  TRANSFORMERS_OFFLINE: "1"
volumes:
  - /home/ubuntu/whisper-model:/models/whisper:ro
  - huggingface-cache:/root/.cache/huggingface
```

The OpenPronounce cache must be located at:

```text
/root/.cache/huggingface/hub/models--facebook--wav2vec2-lv-60-espeak-cv-ft
```

The `hub` directory is required. Copying the model directly under `/root/.cache/huggingface` will not be detected by Transformers.

When model websites cannot be reached, download models on another machine, transfer them with `scp`, copy the Hugging Face cache into the named Docker volume, and enable offline mode. Do not commit model files or tokens to Git.

## Docker

From the project root:

```bash
docker compose build evaluation-service
docker compose up -d evaluation-service
docker compose logs -f evaluation-service
```

Health checks only verify that the HTTP process is running. Perform a real `/api/v1/evaluate` request after copying models.
