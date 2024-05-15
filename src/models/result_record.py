from pydantic import BaseModel

from src.types.openai import GenerativeModelResponse, ConversationHistory


class ResultRecord(BaseModel):
    id: int
    question: str
    prompt: ConversationHistory
    raw_output: GenerativeModelResponse
    parsed_output: int
