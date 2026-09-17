from io import BytesIO

from gtts import gTTS


class TTSService:
    # Convert English text into an MP3 audio stream.
    def synthesize(self, text: str) -> BytesIO:
        audio = BytesIO()

        tts = gTTS(text=text, lang="en")
        tts.write_to_fp(audio)

        audio.seek(0)
        return audio
