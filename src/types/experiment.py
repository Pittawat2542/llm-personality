from enum import Enum


class PersonalityType(Enum):
    NO_PERSONALITY = "no_personality"
    AGREEABLENESS = "agreeableness"
    CONSCIENTIOUSNESS = "conscientiousness"
    EXTROVERSION = "extroversion"
    NEUROTICISM = "neuroticism"
    OPENNESS_TO_EXPERIENCE = "openness_to_experience"


class InteractionType(Enum):
    ALL_AT_ONCE = "all_at_once"
    ONE_AT_A_TIME_SAME_CONTEXT = "one_at_a_time_same_context"
    ONE_AT_A_TIME_NEW_CONTEXT = "one_at_a_time_new_context"
