import re

from phonemizer import phonemize
from phonemizer.separator import Separator

from openpronounce.phones import normalize_phones


class PhonemeService:
    # Map the requested accent to an eSpeak pronunciation standard.
    ACCENTS = {
        "en-US": "en-us",
        "en-GB": "en-gb-x-rp",
    }

    def get_expected_phonemes(self, text: str, accent: str) -> tuple[list[str], list[str], list[list[str]]]:
        # Generate accent-specific expected phonemes and preserve word boundaries.
        language = self.ACCENTS[accent]
        words = re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", text.lower())
        if not words:
            return [], [], []

        output = phonemize(
            " ".join(words),
            language=language,
            backend="espeak",
            strip=True,
            preserve_punctuation=False,
            separator=Separator(phone=" ", word=" | ", syllable=""),
        )
        groups = [normalize_phones(group.split(), lang="en") for group in output.split("|")]
        if len(groups) != len(words):
            raise RuntimeError("eSpeak returned an unexpected number of word groups")
        return [phone for group in groups for phone in group], words, groups


phoneme_service = PhonemeService()
