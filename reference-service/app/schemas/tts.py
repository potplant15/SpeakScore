from typing import Literal

from pydantic import BaseModel, Field


class TTSRequest(BaseModel):
    # Validate text and voice selection submitted for speech synthesis.
    text: str = Field(min_length=1, max_length=1000)
    accent: Literal["en-US", "en-GB"] = "en-US"
    gender: Literal["female", "male"] = "female"


class PronunciationReferenceResponse(BaseModel):
    # Return the submitted text, accent, and generated IPA reference.
    text: str
    accent: Literal["en-US", "en-GB"]
    ipa: str
