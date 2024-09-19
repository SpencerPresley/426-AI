from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY, LLM_MODEL, LLM_TEMPERATURE
from .chain_prompts import method_extraction_prompt, abstract_analysis_prompt 
from parsers import method_parser, abstract_sentence_parser

llm = ChatOpenAI(
    model=LLM_MODEL,
    openai_api_key=OPENAI_API_KEY,
    streaming=True,
    temperature=LLM_TEMPERATURE,
)

method_chain = method_extraction_prompt | llm | method_parser
abstract_chain = abstract_analysis_prompt | llm | abstract_sentence_parser