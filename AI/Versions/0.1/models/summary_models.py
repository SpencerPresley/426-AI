from typing import List
from langchain_core.pydantic_v1 import BaseModel

class Feedback(BaseModel):
    assistant_name: str
    feedback: str

class AbstractSummary(BaseModel):
    summary: str
    reasoning: str
    feedback: List[Feedback]