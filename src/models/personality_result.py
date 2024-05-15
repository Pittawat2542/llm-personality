from pydantic import BaseModel


class PersonalityResult(BaseModel):
    openness: int
    conscientiousness: int
    extroversion: int
    agreeableness: int
    neuroticism: int
