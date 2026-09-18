from fastapi import FastAPI

from app.api.evaluation import router


app = FastAPI(title="SpeakScore Evaluation Service", version="0.1.0")


@app.get("/health")
def health():
    # Report whether the evaluation service is available.
    return {"status": "ok"}


app.include_router(router, prefix="/api/v1")
