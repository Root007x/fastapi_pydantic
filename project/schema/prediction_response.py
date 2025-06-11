from pydantic import BaseModel, Field
from typing import Dict


class PredictionResponse(BaseModel):
    predicted_category: str = Field(
        ..., 
        description="The predicted insurance premium category", examples=["high"]
    )
    confidence: float = Field(
        ...,
        description="Model Confidence Score (range : 0 to 1)",
        examples=[0.85]
    )
    class_probabilities: Dict[str, float] = Field(
        ...,
        description="Probability distribution across all possiable classes",
        examples=[{
            "Low": 0.01,
            "Medium": 0.15,
            "High": 0.56
        }]
    )