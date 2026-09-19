from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.tts import PronunciationReferenceResponse, TTSRequest
from app.services.audio_service import AudioService
from app.services.ipa_service import IPAService


router = APIRouter()
audio_service = AudioService()
ipa_service = IPAService()


@router.post("/tts")
def generate_speech(request: TTSRequest):
    # Generate and stream MP3 audio for the requested text and voice.
    audio = audio_service.synthesize(request.text, request.accent, request.gender)

    return StreamingResponse(audio, media_type="audio/mpeg")


@router.post("/reference", response_model=PronunciationReferenceResponse)
def get_pronunciation_reference(request: TTSRequest):
    # Generate an IPA pronunciation reference for the requested accent.
    return PronunciationReferenceResponse(
        text=request.text,
        accent=request.accent,
        ipa=ipa_service.generate(request.text, request.accent),
    )
