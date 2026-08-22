from pydantic import BaseModel


class DocumentSubmission(BaseModel):
    user_name: str
    content: str


class DocumentResponse(BaseModel):
    message: str
    user_name: str
    chunks_added: int
