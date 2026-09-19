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

        # Aggregate individual edits by word so a replacement cannot cross a
        # word boundary and produce misleading strings such as "aɪwʊ".
        grouped: dict[str, dict] = {}
        for tag, expected_index, heard_index in Levenshtein.editops(expected, heard):
            # Insertions have no expected phone; attach them to the nearest
            # preceding phone, or to the first word for an insertion at zero.
            word_index = expected_index
            if tag == "insert" and expected_index > 0:
                word_index = expected_index - 1
            word = word_for(word_index)
            entry = grouped.setdefault(
                word,
                {"word": word, "expected": [], "heard": [], "confidences": []},
            )

            if tag in ("replace", "delete"):
                entry["expected"].append(expected[expected_index])
            if tag in ("replace", "insert") and heard_index < len(heard):
                entry["heard"].append(heard[heard_index])
                if heard_index < len(confidences):
                    entry["confidences"].append(confidences[heard_index])

        errors = []
        for entry in grouped.values():
            confidence_values = entry["confidences"]
            confidence = (
                sum(confidence_values) / len(confidence_values)
                if confidence_values
                else 1.0
            )
            errors.append(
                {
                    "word": entry["word"],
                    "expected": "".join(entry["expected"]),
                    "heard": "".join(entry["heard"]),
                    "confidence": round(float(confidence), 3),
                }
            )
        return errors


pronunciation_service = PronunciationService()
