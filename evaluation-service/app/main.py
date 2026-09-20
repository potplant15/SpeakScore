import os
from pathlib import Path

from fastapi import FastAPI

from app.api.evaluation import router


app = FastAPI(title="SpeakScore Evaluation Service", version="0.1.0")


def report_model_configuration():
    # Report missing local model resources before the first evaluation request.
    whisper_model = os.getenv("WHISPER_MODEL", "base.en")
    if whisper_model.startswith("/") and not Path(whisper_model).exists():
        print(f"WARNING: Whisper model path does not exist: {whisper_model}", flush=True)

    hf_home = Path(os.getenv("HF_HOME", "/root/.cache/huggingface"))
    phone_model = hf_home / "hub" / "models--facebook--wav2vec2-lv-60-espeak-cv-ft"
    if not phone_model.exists():
        print(
            "WARNING: OpenPronounce model cache is missing: "
            f"{phone_model}. Evaluation may try to download it.",
            flush=True,
        )


report_model_configuration()


@app.get("/health")
def health():
    # Report whether the evaluation service is available.
    return {"status": "ok"}


app.include_router(router, prefix="/api/v1")
