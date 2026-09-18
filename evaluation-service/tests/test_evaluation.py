import asyncio
from io import BytesIO

from app.api.evaluation import evaluate
from app.main import app, health
from app.schemas.evaluation import EvaluationResponse
from app.services.scoring_service import ScoringService


def test_health():
    # Verify the health response and application metadata.
    assert health() == {"status": "ok"}
    assert app.title == "SpeakScore Evaluation Service"
    assert app.version == "0.1.0"


def test_scoring_service():
    # Verify exact text receives full accuracy and completeness scores.
    service = ScoringService()
    result = service.evaluate(
        "How are you today?",
        "How are you today",
        [
            {"word": "How", "start": 0.0, "end": 0.3},
            {"word": "are", "start": 0.35, "end": 0.55},
            {"word": "you", "start": 0.6, "end": 0.85},
            {"word": "today", "start": 0.9, "end": 1.4},
        ],
    )

    assert result["content_accuracy"] == 100.0
    assert result["completeness"] == 100.0
    assert result["wer"] == 0.0
    assert result["long_pause_count"] == 0


def test_evaluate_endpoint_with_mocked_asr(monkeypatch):
    # Verify multipart evaluation without downloading a Whisper model.
    def fake_transcribe(audio_path: str):
        return {
            "text": "How are you today",
            "words": [
                {"word": "How", "start": 0.0, "end": 0.3, "probability": 0.99},
                {"word": "are", "start": 0.35, "end": 0.55, "probability": 0.99},
                {"word": "you", "start": 0.6, "end": 0.85, "probability": 0.99},
                {"word": "today", "start": 0.9, "end": 1.4, "probability": 0.99},
            ],
            "language": "en",
        }

    monkeypatch.setattr(
        "app.api.evaluation.asr_service.transcribe",
        fake_transcribe,
    )
    monkeypatch.setattr(
        "app.api.evaluation.pronunciation_service.evaluate",
        lambda audio_path, reference_text, accent: {
            "score": 90.0,
            "phoneme_error_rate": 0.1,
            "expected_phonemes": ["h", "aʊ"],
            "heard_phonemes": ["h", "aʊ"],
            "errors": [],
        },
    )

    async def fake_run_in_threadpool(func, *args):
        return func(*args)

    monkeypatch.setattr(
        "app.api.evaluation.run_in_threadpool",
        fake_run_in_threadpool,
    )

    class FakeUpload:
        # Provide an in-memory upload without a threadpool dependency.
        filename = "sample.mp3"

        def __init__(self):
            self.stream = BytesIO(b"fake-mp3-data")

        async def read(self, size: int):
            return self.stream.read(size)

    async def fake_close():
        return None

    upload = FakeUpload()
    upload.close = fake_close

    response = asyncio.run(evaluate("How are you today?", upload, "en-US"))

    result = EvaluationResponse.model_validate(response)
    assert result.recognized_text == "How are you today"
    assert result.accent == "en-US"
    assert result.content_accuracy == 100.0
    assert result.pronunciation.score == 90.0
    assert len(result.words) == 4
