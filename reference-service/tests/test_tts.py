from io import BytesIO

from app.main import app, health
from app.api import tts as tts_api
from app.api.tts import generate_speech
from app.schemas.tts import TTSRequest
from app.services.ipa_service import IPAService


def test_health():
    # Verify the health response and application metadata.
    assert health() == {"status": "ok"}
    assert app.title == "SpeakScore Reference Service"
    assert app.version == "0.1.0"


def test_tts_returns_mp3(monkeypatch):
    class FakeTTSService:
        # Return deterministic fake audio for the API test.
        def synthesize(self, text: str, accent: str, gender: str) -> BytesIO:
            assert text == "How are you today?"
            assert accent == "en-US"
            assert gender == "female"
            return BytesIO(b"fake-mp3-data")

    monkeypatch.setattr(tts_api, "audio_service", FakeTTSService())

    response = generate_speech(
        TTSRequest(text="How are you today?", accent="en-US", gender="female")
    )

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


def test_reference_returns_ipa(monkeypatch):
    class FakeIPAService:
        # Return deterministic IPA for the API test.
        def generate(self, text: str, accent: str) -> str:
            assert text == "How are you today?"
            assert accent == "en-US"
            return "haʊ ɑɹ ju təˈdeɪ"

    monkeypatch.setattr(tts_api, "ipa_service", FakeIPAService())
    response = tts_api.get_pronunciation_reference(
        TTSRequest(text="How are you today?", accent="en-US")
    )
    assert response.ipa == "haʊ ɑɹ ju təˈdeɪ"


def test_ipa_is_formatted_for_learners():
    service = IPAService()
    raw = "aɪ wʊd lˈaɪk sˌʌm wˈɔːɾɚ"

    assert service.normalize(raw, "I would like some water.", "en-US") == (
        "aɪ wəd laɪk səm ˈwɔːɾɚ"
    )
