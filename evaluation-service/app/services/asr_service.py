import os

from faster_whisper import WhisperModel


class ASRService:
    # Provide English speech recognition with word-level timestamps.
    def __init__(self):
        self.model_name = os.getenv("WHISPER_MODEL", "base.en")
        self.device = os.getenv("WHISPER_DEVICE", "cpu")
        self.compute_type = os.getenv("WHISPER_COMPUTE_TYPE", "int8")
        self.model = None

    def _get_model(self) -> WhisperModel:
        # Load the Whisper model only when the first evaluation is requested.
        if self.model is None:
            print(
                f"Loading Whisper model: {self.model_name} "
                f"(device={self.device}, compute_type={self.compute_type})",
                flush=True,
            )
            self.model = WhisperModel(
                self.model_name,
                device=self.device,
                compute_type=self.compute_type,
            )
        return self.model

    def transcribe(self, audio_path: str) -> dict:
        # Transcribe an audio file and collect recognized word timestamps.
        segments, info = self._get_model().transcribe(
            audio_path,
            language="en",
            beam_size=5,
            word_timestamps=True,
            vad_filter=True,
        )

        texts = []
        words = []

        for segment in segments:
            if segment.text:
                texts.append(segment.text.strip())

            if segment.words:
                for word in segment.words:
                    words.append(
                        {
                            "word": word.word.strip(),
                            "start": round(word.start, 3),
                            "end": round(word.end, 3),
                            "probability": (
                                round(word.probability, 4)
                                if word.probability is not None
                                else None
                            ),
                        }
                    )

        return {
            "text": " ".join(texts).strip(),
            "words": words,
            "language": info.language,
        }


asr_service = ASRService()
