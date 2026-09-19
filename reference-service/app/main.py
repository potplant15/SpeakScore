from fastapi import FastAPI

from app.api.tts import router as tts_router


app = FastAPI(title="SpeakScore Reference Service", version="0.1.0")


@app.get("/health")
def health():
    # Report whether the TTS service is available.
    return {"status": "ok"}


app.include_router(tts_router, prefix="/api/v1")
