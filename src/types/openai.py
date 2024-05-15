from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam, \
    ChatCompletionAssistantMessageParam
from typing_extensions import Literal, Tuple

type Response = str
type TokenCount = int

OpenAIRole = Literal["system", "assistant", "user"]
ConversationHistory = list[ChatCompletionSystemMessageParam | ChatCompletionUserMessageParam |
                           ChatCompletionAssistantMessageParam]
GenerativeModelResponse = Tuple[Response, TokenCount, TokenCount]