import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

LLM_MODEL = "gpt-4o"
LLM_TEMPERATURE = 0.0