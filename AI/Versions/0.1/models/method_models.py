from typing import List
from langchain_core.pydantic_v1 import BaseModel, Field

class MethodDetail(BaseModel):
    reasoning: str
    passages: List[str]
    confidence_score: float

class MethodOutput(BaseModel):
    methods: List[str]
    method_details: dict[str, MethodDetail]