# SpeakScore Reference Service

This service provides standard English pronunciation references: Kokoro-ONNX
generates MP3 audio and eSpeak NG generates IPA text.

The default port is `8001`.

## Requirements

- Python 3.12
- FastAPI and Uvicorn
- Kokoro ONNX model and voice file
- eSpeak NG for IPA generation
- FFmpeg when audio inspection or conversion is required

## Model files

When running locally without Docker, keep the model files outside the repository:

```bash
mkdir -p ~/kokoro-models
wget -O ~/kokoro-models/kokoro-v1.0.onnx \
  https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/kokoro-v1.0.onnx
wget -O ~/kokoro-models/voices-v1.0.bin \
  https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/voices-v1.0.bin
```

The service reads these paths by default. They can be overridden with
`KOKORO_MODEL_PATH` and `KOKORO_VOICES_PATH`.

If the model download website is unavailable, download both files on another
machine and copy them to the server. Do not commit model files to Git.

## Run

```bash
cd ~/SpeakScore/reference-service
source ../.venv/bin/activate
uvicorn app.main:app --reload --port 8001
```

When running with Docker Compose, the service downloads these files automatically
on first startup and stores them in the named `kokoro-models` volume. Later
starts reuse the cached files. The download URLs can be overridden with
`KOKORO_MODEL_URL` and `KOKORO_VOICES_URL`.

To run the containerized service from the project root:

```bash
docker compose build reference-service
docker compose up -d reference-service
docker compose logs -f reference-service
```

## Generate speech

```bash
curl -X POST http://127.0.0.1:8001/api/v1/tts \
  -H 'Content-Type: application/json' \
  -d '{"text":"I would like some water.","accent":"en-US","gender":"female"}' \
  --output kokoro-test.mp3
```

## Generate IPA reference

```bash
curl -X POST http://127.0.0.1:8001/api/v1/reference \
  -H 'Content-Type: application/json' \
  -d '{"text":"I would like some water.","accent":"en-US"}'
```

Supported voice mapping:

| Accent | Female | Male |
| --- | --- | --- |
| `en-US` | `af_heart` | `am_michael` |
| `en-GB` | `bf_emma` | `bm_george` |

## Health check

```bash
curl http://127.0.0.1:8001/health
```

## API summary

Text-to-speech accepts `text`, `accent` and `gender`, and returns `audio/mpeg`.
The reference endpoint returns learner-facing IPA and metadata.

When Practice Service runs in Docker, it should call this service with
`http://reference-service:8001`, not `localhost`.
