from langchain_core.output_parsers import JsonOutputParser
from models.abstract_sentence_models import AbstractThemes

abstract_sentence_parser = JsonOutputParser(pydantic_object=AbstractThemes)