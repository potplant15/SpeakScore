from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.tts import TTSRequest
from app.services.tts_service import TTSService


router = APIRouter()
tts_service = TTSService()


@router.post("/tts")
def generate_speech(request: TTSRequest):
    # Generate and stream MP3 audio for the requested text.
    audio = tts_service.synthesize(request.text)

    return StreamingResponse(audio, media_type="audio/mpeg")
