from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, conlist

from .model import ModelService

app = FastAPI(title="Iris Classifier API")
model_service = ModelService()


class PredictRequest(BaseModel):
    features: conlist(float, min_items=4, max_items=4) = Field(
        ..., description="sepal_length, sepal_width, petal_length, petal_width"
    )


class PredictResponse(BaseModel):
    class_index: int
    class_label: str


@app.get("/health")
def health():
    return {"status": "ok", "model_accuracy": round(model_service.accuracy, 4)}


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    try:
        result = model_service.predict(req.features)
        return PredictResponse(**result)
    except Exception as e:  # pragma: no cover - defensive
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":  # pragma: no cover - manual run
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
