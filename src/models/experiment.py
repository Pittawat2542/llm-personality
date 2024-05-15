from pydantic import BaseModel

from src.llms.llm import LLM
from src.types.experiment import PersonalityType, InteractionType


class Experiment(BaseModel):
    id: str
    personality_type: PersonalityType
    interaction_type: InteractionType
    model_name: str
    llm: LLM
