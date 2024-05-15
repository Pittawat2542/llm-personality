from time import sleep

from openai import (APIConnectionError, APIError, APITimeoutError, OpenAI,
                    RateLimitError)

from src.llms.llm import LLM
from src.types.openai import ConversationHistory, GenerativeModelResponse


class OpenAILLM(LLM):
    def __init__(self, **data):
        super().__init__(**data)
        self.client = OpenAI(max_retries=3, timeout=60)

    def generate_content(self, messages: ConversationHistory, temperature=0.0, seed=42) -> GenerativeModelResponse:
        try:
            chat_completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                seed=seed,
                temperature=temperature,
            )

            response = chat_completion.choices[0].message.content

            prompt_tokens = chat_completion.usage.prompt_tokens
            completion_tokens = chat_completion.usage.completion_tokens

            return response.strip(), prompt_tokens, completion_tokens
        except (APITimeoutError, APIConnectionError, RateLimitError, APIError) as e:
            print(f"OpenAI API error: {e}")
            sleep(3)
            return self.generate_content(messages, temperature, seed)
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise e
