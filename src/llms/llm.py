from abc import ABC, abstractmethod

from pydantic import BaseModel
from typing_extensions import Any

from src.types.openai import ConversationHistory, GenerativeModelResponse


class LLM(ABC, BaseModel):
    model_name: str
    client: Any

    @abstractmethod
    def generate_content(self, messages: ConversationHistory, temperature=0.0, seed=2024) -> GenerativeModelResponse:
        pass
