from app.services import pronunciation_service as pronunciation_module
from app.services.pronunciation_service import PronunciationService


def test_pronunciation_alignment(monkeypatch, tmp_path):
    # Verify OpenPronounce phones are aligned and converted into a score.
    monkeypatch.setattr(
        pronunciation_module.phoneme_service,
        "get_expected_phonemes",
        lambda text, accent: (
            ["h", "ɛ", "l", "oʊ"],
            ["hello"],
            [["h", "ɛ", "l", "oʊ"]],
        ),
    )
    monkeypatch.setattr(pronunciation_module, "load_audio", lambda path: [0.0])
    monkeypatch.setattr(
        pronunciation_module,
        "transcribe_phones",
        lambda waveform, sampling_rate, lang, return_confidence: (
            ["h", "ɛ", "l", "əʊ"],
            [0.9, 0.9, 0.9, 0.8],
        ),
    )

    result = PronunciationService().evaluate(
        str(tmp_path / "sample.wav"), "Hello", "en-GB"
    )

    assert result["score"] == 75.0
    assert result["phoneme_error_rate"] == 0.25
    assert result["errors"][0]["word"] == "hello"
