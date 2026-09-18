import os
import tempfile
from pathlib import Path
from typing import Annotated, Literal

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from starlette.concurrency import run_in_threadpool

from app.schemas.evaluation import EvaluationResponse
from app.services.asr_service import asr_service
from app.services.pronunciation_service import pronunciation_service
from app.services.scoring_service import scoring_service


router = APIRouter()
MAX_AUDIO_SIZE = 10 * 1024 * 1024


@router.post("/evaluate", response_model=EvaluationResponse)
async def evaluate(
    reference_text: Annotated[str, Form(min_length=1, max_length=1000)],
    audio: Annotated[UploadFile, File()],
    accent: Annotated[Literal["en-US", "en-GB"], Form()] = "en-US",
):
    # Transcribe and pronunciation-score the uploaded audio.
    suffix = Path(audio.filename or "audio.webm").suffix or ".webm"
    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_path = temp_file.name
            total_size = 0

            while chunk := await audio.read(1024 * 1024):
                total_size += len(chunk)
                if total_size > MAX_AUDIO_SIZE:
                    raise HTTPException(
                        status_code=413,
                        detail="Audio file is too large",
                    )
                temp_file.write(chunk)

        transcription = await run_in_threadpool(asr_service.transcribe, temp_path)

        if not transcription["words"]:
            raise HTTPException(status_code=422, detail="No speech detected")

        try:
            pronunciation = await run_in_threadpool(
                pronunciation_service.evaluate,
                temp_path,
                reference_text,
                accent,
            )
        except (RuntimeError, OSError, ValueError) as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

        scores = scoring_service.evaluate(
            reference_text,
            transcription["text"],
            transcription["words"],
            pronunciation_score=pronunciation["score"],
        )

        return {
            "reference_text": reference_text,
            "recognized_text": transcription["text"],
            "accent": accent,
            "pronunciation": pronunciation,
            "pronunciation_errors": pronunciation["errors"],
            **scores,
            "words": transcription["words"],
        }
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        await audio.close()
