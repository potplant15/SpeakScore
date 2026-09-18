import Levenshtein
from openpronounce import load_audio, transcribe_phones

from app.services.phoneme_service import phoneme_service


class PronunciationService:
    # Assess the learner's phonemes against an accent-specific eSpeak reference.
    def evaluate(self, audio_path: str, reference_text: str, accent: str) -> dict:
        # Decode audio and recognize the phones actually spoken by the learner.
        expected, words, groups = phoneme_service.get_expected_phonemes(
            reference_text, accent
        )
        waveform = load_audio(audio_path)
        heard, confidences = transcribe_phones(
            waveform,
            sampling_rate=16000,
            lang="en",
            return_confidence=True,
        )

        distance = Levenshtein.distance(expected, heard)
        error_rate = distance / len(expected) if expected else 1.0
        errors = self._errors(expected, heard, confidences, words, groups)

        return {
            "score": round(max(0.0, 100.0 * (1.0 - error_rate)), 2),
            "phoneme_error_rate": round(error_rate, 4),
            "expected_phonemes": expected,
            "heard_phonemes": heard,
            "errors": errors,
        }

    def _errors(
        self,
        expected: list[str],
        heard: list[str],
        confidences: list[float],
        words: list[str],
        groups: list[list[str]],
    ) -> list[dict]:
        # Convert sequence edit operations into compact word-level feedback.
        boundaries = []
        offset = 0
        for word, group in zip(words, groups):
            boundaries.append((offset, offset + len(group), word))
            offset += len(group)

        def word_for(index: int) -> str:
            for start, end, word in boundaries:
                if start <= index < end:
                    return word
            return words[-1] if words else ""

        errors = []
        for tag, start, end, heard_start, heard_end in Levenshtein.opcodes(
            expected, heard
        ):
            if tag == "equal":
                continue
            word = word_for(start)
            actual_confidences = confidences[heard_start:heard_end]
            confidence = sum(actual_confidences) / len(actual_confidences) if actual_confidences else 1.0
            errors.append(
                {
                    "word": word,
                    "expected": "".join(expected[start:end]),
                    "heard": "".join(heard[heard_start:heard_end]),
                    "confidence": round(float(confidence), 3),
                }
            )
        return errors


pronunciation_service = PronunciationService()
