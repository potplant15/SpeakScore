from typing import Literal

from pydantic import BaseModel


class WordInfo(BaseModel):
    # Store timing and confidence data for one recognized word.
    word: str
    start: float
    end: float
    probability: float | None = None


class PronunciationError(BaseModel):
    # Describe a phoneme mismatch detected by OpenPronounce.
    word: str
    expected: str
    heard: str
    confidence: float


class PronunciationResult(BaseModel):
    # Store phoneme-level pronunciation assessment details.
    score: float
    phoneme_error_rate: float
    expected_phonemes: list[str]
    heard_phonemes: list[str]
    errors: list[PronunciationError]


class EvaluationResponse(BaseModel):
    # Define the JSON response returned by the evaluation endpoint.
    reference_text: str
    recognized_text: str
    accent: Literal["en-US", "en-GB"]
    content_accuracy: float
    completeness: float
    pronunciation: PronunciationResult
    pronunciation_errors: list[PronunciationError]
    fluency: float
    overall_score: float
    wer: float
    words_per_minute: float
    long_pause_count: int
    words: list[WordInfo]
