from typing import List
from pydantic import BaseModel


class Feedback(BaseModel):
    assistant_name: str
    feedback: str


class AbstractSummary(BaseModel):
    summary: str
    reasoning: str
    feedback: List[Feedback]
