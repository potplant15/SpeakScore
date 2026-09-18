import os
import subprocess
from io import BytesIO
from pathlib import Path

import soundfile as sf
from kokoro_onnx import Kokoro


class KokoroService:
    # Convert English text into an MP3 stream with a selected Kokoro voice.
    VOICE_MAP = {
        ("en-US", "female"): "af_heart",
        ("en-US", "male"): "am_michael",
        ("en-GB", "female"): "bf_emma",
        ("en-GB", "male"): "bm_george",
    }

    def __init__(self):
        # Keep large model files outside the repository by default.
        model_path = os.getenv(
            "KOKORO_MODEL_PATH", str(Path.home() / "kokoro-models/kokoro-v1.0.onnx")
        )
        voices_path = os.getenv(
            "KOKORO_VOICES_PATH", str(Path.home() / "kokoro-models/voices-v1.0.bin")
        )
        self.model_path = model_path
        self.voices_path = voices_path
        self.kokoro = None

    def _get_kokoro(self) -> Kokoro:
        # Load the model only when synthesis is requested.
        if self.kokoro is None:
            self.kokoro = Kokoro(self.model_path, self.voices_path)
        return self.kokoro

    def synthesize(self, text: str, accent: str, gender: str) -> BytesIO:
        # Generate WAV samples and encode them as MP3 for the API response.
        voice = self.VOICE_MAP[(accent, gender)]
        samples, sample_rate = self._get_kokoro().create(
            text,
            voice=voice,
            speed=1.0,
            lang=accent.lower(),
        )

        wav_audio = BytesIO()
        sf.write(wav_audio, samples, sample_rate, format="WAV", subtype="PCM_16")
        wav_audio.seek(0)

        result = subprocess.run(
            ["ffmpeg", "-nostdin", "-loglevel", "error", "-i", "pipe:0", "-f", "mp3", "pipe:1"],
            input=wav_audio.read(),
            stdout=subprocess.PIPE,
            check=True,
        )
        return BytesIO(result.stdout)
