# SpeakScore Kokoro Service

This service generates English MP3 audio with Kokoro-ONNX.

## Model files

Keep the model files outside the repository:

```bash
mkdir -p ~/kokoro-models
wget -O ~/kokoro-models/kokoro-v1.0.onnx \
  https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/kokoro-v1.0.onnx
wget -O ~/kokoro-models/voices-v1.0.bin \
  https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/voices-v1.0.bin
```

The service reads these paths by default. They can be overridden with
`KOKORO_MODEL_PATH` and `KOKORO_VOICES_PATH`.

## Run

```bash
cd ~/SpeakScore/kokoro-service
source ../.venv/bin/activate
uvicorn app.main:app --reload --port 8001
```

For a container run, mount the external model directory at
`/root/kokoro-models` and publish port `8001`.

## Generate speech

```bash
curl -X POST http://127.0.0.1:8001/api/v1/tts \
  -H 'Content-Type: application/json' \
  -d '{"text":"I would like some water.","accent":"en-US","gender":"female"}' \
  --output kokoro-test.mp3
```

Supported voice mapping:

| Accent | Female | Male |
| --- | --- | --- |
| `en-US` | `af_heart` | `am_michael` |
| `en-GB` | `bf_emma` | `bm_george` |
