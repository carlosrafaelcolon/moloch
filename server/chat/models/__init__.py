from pydantic import BaseModel, Extra

class QMetadata(BaseModel):
    eventid: str

class QArgs(BaseModel):
    eventid: str


class Metadata(BaseModel, extra=Extra.allow):
    conversation_id: str
    user_id: str
    eventid: str


class ChatArgs(BaseModel, extra=Extra.allow):
    conversation_id: str
    eventid: str
    metadata: Metadata
    streaming: bool