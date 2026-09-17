from pydantic import BaseModel, Field


class TTSRequest(BaseModel):
    # Validate the text submitted for speech synthesis.
    text: str = Field(min_length=1, max_length=1000)
