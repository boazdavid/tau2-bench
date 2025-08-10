import uuid
from pydantic import BaseModel
import requests
from typing import List
from tau2.agent.base import BaseAgent, ValidAgentInputMessage
from tau2.data_model.message import APICompatibleMessage, AssistantMessage, Message, ParticipantMessageBase



class CollieConvState(BaseModel):
    messages: list[APICompatibleMessage]
    threadId: str | None

class CollieMessageResponse(BaseModel):
    message: str
    thread_id: str | None

class RemoteCollieAgent(BaseAgent[CollieConvState]):
    server_url: str

    def __init__(self, server_url: str) -> None:
        super().__init__()
        self.server_url = server_url

    def get_init_state(self, message_history: list[Message]|None = None) -> CollieConvState:
        return CollieConvState(
            messages=message_history or [], # type: ignore
            threadId=None #str(uuid.uuid4())
        )

    def generate_next_message(
        self, message: ValidAgentInputMessage, state: CollieConvState
    ) -> tuple[AssistantMessage, CollieConvState]:
        state.messages.append(message)
        
        resp_message = self.call_remote(state)
        assistant_message = AssistantMessage(
            role="assistant",
            content=resp_message.message
        )
        state.messages.append(assistant_message)
        state.threadId = resp_message.thread_id
        return assistant_message, state

    def call_remote(self, state: CollieConvState)->CollieMessageResponse:
        url = f"{self.server_url}/api/message"
        last_message = state.messages[-1]
        payload = {
            "messages": [last_message.model_dump()],
            "thread_id": state.threadId
        }
        response = requests.post(url, json=payload)

        if response.ok:
            return CollieMessageResponse.model_construct(**response.json())
        else:
            raise Exception(f"Request failed with status {response.status_code}: {response.text}")