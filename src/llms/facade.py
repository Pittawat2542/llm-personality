from src.llms.openai_llm import OpenAILLM

supported_models = ["gpt-4o-2024-05-13", "gpt-4-turbo-2024-04-09", "gpt-4-0613", "gpt-3.5-turbo-0125"]


def get_llm(model: str):
    if model in supported_models:
        return OpenAILLM(model_name=model, client=None)
    else:
        raise ValueError(f"Model {model} not supported")
