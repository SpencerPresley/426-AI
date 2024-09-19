from typing import List
from langchain_core.pydantic_v1 import BaseModel

class SentenceDetails(BaseModel):
    sentence: str
    meaning: str
    reasoning: str
    confidence_score: float

class AbstractThemes(BaseModel):
    sentence_details: List[SentenceDetails]
    overall_theme: str
    summary: str