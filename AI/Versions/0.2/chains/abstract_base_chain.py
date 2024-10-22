from abc import ABC, abstractmethod
from langchain.schema.runnable import RunnablePassthrough, RunnableParallel
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
from typing import List, Dict, Any
import json
import os
import logging
from pydantic import BaseModel


class AbstractBaseChain(ABC):
    def __init__(self, llm_model: str, llm_temperature: float, **llm_kwargs):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(logging.StreamHandler())
        self.model_type = self.get_model_type(llm_model)
        self.llm = self._initialize_llm(
            llm_model, llm_temperature, self.model_type, **llm_kwargs
        )

    @staticmethod
    def get_model_type(llm_model: str):
        if llm_model.lower().startswith("gpt"):
            return "openai"
        elif llm_model.lower().startswith("gemini"):
            return "gemini"
        elif llm_model.lower().startswith("claude"):
            return "anthropic"
        else:
            raise ValueError(f"Unsupported model: {llm_model}")

    @staticmethod
    def _initialize_llm(
        llm_model: str, llm_temperature: float, model_type: str, **llm_kwargs
    ):
        if model_type == "openai":
            return ChatOpenAI(
                model=llm_model, temperature=llm_temperature, **llm_kwargs
            )
        elif model_type == "gemini":
            return ChatGoogleGenerativeAI(
                model=llm_model, temperature=llm_temperature, **llm_kwargs
            )
        elif model_type == "anthropic":
            return ChatAnthropic(
                model=llm_model, temperature=llm_temperature, **llm_kwargs
            )
        else:
            raise ValueError(f"Unsupported model: {llm_model}")

    @abstractmethod
    def create_chain(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement the create_chain method")

    @abstractmethod
    def run_chain(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement the run_chain method")

    def save_output(self, output: Any, file_name: str):
        output_type = None
        if isinstance(output, list):
            output_type = type(output[0])
        else:
            output_type = type(output)

        if type(output) == dict:
            with open(file_name, "w") as f:
                json.dump(output, f, indent=4)
        elif type(output) == BaseModel:
            with open(file_name, "w") as f:
                json.dump(output.model_dump(), f, indent=4)
        else:
            raise ValueError(f"Unsupported output type: {output_type}")
