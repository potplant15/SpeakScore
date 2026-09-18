import re

import jiwer


class ScoringService:
    # Calculate text accuracy, completeness, and basic fluency scores.
    def normalize(self, text: str) -> str:
        # Normalize text to lowercase alphabetic words for comparison.
        words = re.findall(r"[a-z]+(?:'[a-z]+)?", text.lower())
        return " ".join(words)

    def text_scores(self, reference: str, recognized: str) -> dict:
        # Calculate WER-based accuracy and completeness scores.
        reference = self.normalize(reference)
        recognized = self.normalize(recognized)
        result = jiwer.process_words(reference, recognized)
        reference_words = reference.split()
        word_count = len(reference_words)

        if word_count == 0:
            return {"accuracy": 0, "completeness": 0, "wer": 1}

        accuracy = max(0, 100 * (1 - result.wer))
        completeness = max(
            0,
            100 * (1 - result.deletions / word_count),
        )

        return {
            "content_accuracy": round(accuracy, 2),
            "completeness": round(completeness, 2),
            "wer": round(result.wer, 4),
        }

    def fluency_score(self, words: list[dict]) -> dict:
        # Estimate fluency from speaking speed and long pauses.
        if not words:
            return {
                "fluency": 0,
                "words_per_minute": 0,
                "long_pause_count": 0,
            }

        start = words[0]["start"]
        end = words[-1]["end"]
        duration = max(end - start, 0.1)
        words_per_minute = len(words) / duration * 60

        long_pauses = []
        for previous, current in zip(words, words[1:]):
            pause = current["start"] - previous["end"]
            if pause >= 0.8:
                long_pauses.append(pause)

        pause_ratio = min(sum(long_pauses) / duration, 1)
        pause_score = max(0, 100 - pause_ratio * 100)

        if 90 <= words_per_minute <= 180:
            speed_score = 100
        elif words_per_minute < 90:
            speed_score = max(0, 100 - (90 - words_per_minute))
        else:
            speed_score = max(0, 100 - (words_per_minute - 180) * 0.5)

        fluency = pause_score * 0.6 + speed_score * 0.4
        return {
            "fluency": round(fluency, 2),
            "words_per_minute": round(words_per_minute, 2),
            "long_pause_count": len(long_pauses),
        }

    def evaluate(
        self,
        reference: str,
        recognized: str,
        words: list[dict],
        pronunciation_score: float | None = None,
    ) -> dict:
        # Combine content, pronunciation, and fluency metrics into the total score.
        text_result = self.text_scores(reference, recognized)
        fluency_result = self.fluency_score(words)
        if pronunciation_score is None:
            overall = (
                text_result["content_accuracy"] * 0.75
                + fluency_result["fluency"] * 0.25
            )
        else:
            overall = (
                pronunciation_score * 0.50
                + text_result["content_accuracy"] * 0.30
                + fluency_result["fluency"] * 0.20
            )

        return {
            **text_result,
            **fluency_result,
            "overall_score": round(overall, 2),
        }


scoring_service = ScoringService()
