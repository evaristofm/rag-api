from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import get_llm_service, get_vector_store_service
from app.schemas.ask import AskResponse
from app.services.llm import LLMService
from app.services.vector_store import VectorStoreService

router = APIRouter()


@router.get("/ask", response_model=AskResponse)
def ask(
    question: str,
    vector_store: Annotated[VectorStoreService, Depends(get_vector_store_service)],
    llm: Annotated[LLMService, Depends(get_llm_service)],
    user: str | None = None,
):
    context_docs = vector_store.query(question=question, user_name=user)
    context = "\n\n".join(context_docs)
    answer = llm.ask(question=question, context=context)

    return AskResponse(
        question=question,
        answer=answer,
        context_used=context_docs,
        filtered_by_user=user,
    )
