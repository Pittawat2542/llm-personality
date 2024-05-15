from pydantic import BaseModel
from typing_extensions import List

from src.models.experiment import Experiment
from src.models.personality_result import PersonalityResult
from src.models.result_record import ResultRecord


class ExperimentalResult(BaseModel):
    experiment: Experiment
    results: List[ResultRecord]
    personality_result: PersonalityResult = None
