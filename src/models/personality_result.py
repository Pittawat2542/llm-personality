from pydantic import BaseModel


class PersonalityResult(BaseModel):
    intellect: int
    conscientiousness: int
    extroversion: int
    agreeableness: int
    emotional_stability: int
