import subprocess
import re


class IPAService:
    # Map API accents to eSpeak NG pronunciation voices.
    ACCENT_MAP = {
        "en-US": "en-us",
        "en-GB": "en-GB-x-rp",
    }

    # Use common connected-speech forms for frequent English function words.
    WEAK_FORMS = {
        "a": {"en-US": "ə", "en-GB": "ə"},
        "an": {"en-US": "ən", "en-GB": "ən"},
        "and": {"en-US": "ən", "en-GB": "ən"},
        "of": {"en-US": "əv", "en-GB": "əv"},
        "some": {"en-US": "səm", "en-GB": "səm"},
        "would": {"en-US": "wəd", "en-GB": "wəd"},
        "could": {"en-US": "kəd", "en-GB": "kəd"},
        "should": {"en-US": "ʃəd", "en-GB": "ʃəd"},
        "to": {"en-US": "tə", "en-GB": "tə"},
        "for": {"en-US": "fɚ", "en-GB": "fə"},
    }

    # Group adjacent IPA vowel symbols into syllable nuclei.
    VOWEL_GROUP = re.compile(r"[iɪeɛæɑɒɔoʊuəɚɝʌː]+")

    def _format_token(self, token: str) -> str:
        # Remove eSpeak stress marks from monosyllables and normalize polysyllables.
        primary = "ˈ" in token
        secondary = "ˌ" in token and not primary
        clean = token.replace("ˈ", "").replace("ˌ", "")
        syllables = len(self.VOWEL_GROUP.findall(clean))
        if syllables <= 1:
            return clean
        if primary:
            return "ˈ" + clean
        if secondary:
            return "ˌ" + clean
        return clean

    def normalize(self, raw_ipa: str, text: str, accent: str) -> str:
        # Convert machine-oriented eSpeak IPA into learner-oriented IPA.
        ipa_tokens = raw_ipa.split()
        words = re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", text.lower())
        normalized = []
        for index, token in enumerate(ipa_tokens):
            word = words[index] if index < len(words) else ""
            weak = self.WEAK_FORMS.get(word, {}).get(accent)
            normalized.append(weak if weak else self._format_token(token))
        return " ".join(normalized)

    def generate(self, text: str, accent: str) -> str:
        # Generate IPA text using the requested English accent.
        result = subprocess.run(
            ["espeak-ng", "-q", "--ipa", "-v", self.ACCENT_MAP[accent], text],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        return self.normalize(result.stdout.strip(), text, accent)
