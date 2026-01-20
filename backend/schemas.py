from pydantic import BaseModel
from typing import List

class MatchAnalysis(BaseModel):
    strengths: List[str]
    mistakes: List[str]
    training_focus: List[str]
    confidence: float