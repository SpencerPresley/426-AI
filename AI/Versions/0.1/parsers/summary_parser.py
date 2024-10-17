from langchain_core.output_parsers import JsonOutputParser
from models.summary_models import AbstractSummary

summary_parser = JsonOutputParser(pydantic_object=AbstractSummary)
