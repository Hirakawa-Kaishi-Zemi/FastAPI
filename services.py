from dataclasses import dataclass
from enum import StrEnum

import openai

from settings import OPEN_AI_API_KEY

openai.api_key = OPEN_AI_API_KEY


class ChatGptException(Exception):
    pass


class PromptRole(StrEnum):
    User = 'user'
    Assistant = 'assistant'
    System = 'system'


class PromptModel(StrEnum):
    gpt_35_turbo = 'gpt-3.5-turbo'
    gpt_35_turbo_16k = 'gpt-3.5-turbo-16k'

    # Add other models ...


@dataclass
class Message(object):
    role: PromptRole
    content: str

    def to_dict(self):
        return {
            'role': self.role,
            'content': self.content
        }


@dataclass
class Choice(object):
    index: int
    finish_reason: str
    message: Message


@dataclass
class Response(object):
    id: str
    model: str
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int
    created: int
    choices: list[Choice]


class ChatGPT(object):
    def __init__(self):
        self._messages: list[Message] = []
        self._old_messages: list[Message] = []
        self._model: PromptModel = PromptModel.gpt_35_turbo

    @staticmethod
    def models():
        return openai.Model.list()

    def set_model(self, model: PromptModel):
        self._model = model

    def system_prompt(self, content: str):
        self._messages.append(
            Message(
                role=PromptRole.System,
                content=content,
            )
        )
        return self

    def assistant_prompt(self, content: str):
        self._messages.append(
            Message(
                role=PromptRole.Assistant,
                content=content,
            )
        )
        return self

    def prompt(self, content: str):
        self._messages.append(
            Message(
                role=PromptRole.User,
                content=content,
            )
        )
        return self

    def submit(self) -> Response:
        response = openai.ChatCompletion.create(
            model=self._model,
            messages=[m.to_dict() for m in self._messages],
        )

        choices: list[Choice] = []
        for c in response['choices']:
            choices.append(
                Choice(
                    index=c['index'],
                    finish_reason=c['finish_reason'],
                    message=Message(
                        role=PromptRole(c['message']['role']),
                        content=c['message']['content'],
                    )
                )
            )

        self._old_messages = self._messages[:]
        self._messages.clear()

        return Response(
            id=response['id'],
            model=response['model'],
            completion_tokens=response['usage']['completion_tokens'],
            prompt_tokens=response['usage']['prompt_tokens'],
            total_tokens=response['usage']['total_tokens'],
            created=response['created'],
            choices=choices,
        )
