from pydantic import BaseModel


class AttachmentForm(BaseModel):
    id: int
    name: str
    url: str
