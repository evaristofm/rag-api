from pydantic import BaseModel


class AskResponse(BaseModel):
    question: str
    answer: str
    context_used: list[str]
    filtered_by_user: str | None
