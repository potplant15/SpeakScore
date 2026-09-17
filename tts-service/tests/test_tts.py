from io import BytesIO

from app.main import app, health
from app.api import tts as tts_api
from app.api.tts import generate_speech
from app.schemas.tts import TTSRequest


def test_health():
    # Verify the health response and application metadata.
    assert health() == {"status": "ok"}
    assert app.title == "SpeakScore TTS Service"
    assert app.version == "0.1.0"


def test_tts_returns_mp3(monkeypatch):
    class FakeTTSService:
        # Return deterministic fake audio for the API test.
        def synthesize(self, text: str) -> BytesIO:
            assert text == "How are you today?"
            return BytesIO(b"fake-mp3-data")

    monkeypatch.setattr(tts_api, "tts_service", FakeTTSService())

    response = generate_speech(TTSRequest(text="How are you today?"))

    assert response.media_type == "audio/mpeg"
    assert response.body_iterator is not None


def test_tts_rejects_empty_text():
    # Ensure empty input fails schema validation.
    try:
        TTSRequest(text="")
    except ValueError:
        pass
    else:
        raise AssertionError("empty text should be rejected")
