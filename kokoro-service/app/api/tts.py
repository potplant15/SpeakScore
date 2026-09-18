from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.tts import TTSRequest
from app.services.kokoro_service import KokoroService


router = APIRouter()
kokoro_service = KokoroService()


@router.post("/tts")
def generate_speech(request: TTSRequest):
    # Generate and stream MP3 audio for the requested text and voice.
    audio = kokoro_service.synthesize(request.text, request.accent, request.gender)

    return StreamingResponse(audio, media_type="audio/mpeg")
