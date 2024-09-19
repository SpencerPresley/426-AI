from langchain_core.output_parsers import JsonOutputParser
from models.method_models import MethodOutput

method_parser = JsonOutputParser(pydantic_object=MethodOutput)