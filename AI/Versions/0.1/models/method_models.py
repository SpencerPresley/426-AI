from typing import List
from pydantic import BaseModel


class MethodDetail(BaseModel):
    reasoning: str
    passages: List[str]
    confidence_score: float


class MethodOutput(BaseModel):
    methods: List[str]
    method_details: dict[str, MethodDetail]
