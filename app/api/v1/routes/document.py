import logging
from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import get_vector_store_service
from app.schemas.document import DocumentResponse, DocumentSubmission
from app.services.vector_store import VectorStoreService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/documents", response_model=DocumentResponse)
def add_document(
    submission: DocumentSubmission,
    vector_store: Annotated[VectorStoreService, Depends(get_vector_store_service)],
):
    chunks = [chunk.strip() for chunk in submission.content.split("\n\n") if chunk.strip()]

    vector_store.add_documents(
        ids=[f"{submission.user_name}-chunk{i}" for i in range(len(chunks))],
        documents=chunks,
        metadatas=[
            {"source": "profile", "user_name": submission.user_name, "chunk_index": i}
            for i in range(len(chunks))
        ],
    )

    return DocumentResponse(
        message=f"Added {len(chunks)} chunks for user '{submission.user_name}'.",
        user_name=submission.user_name,
        chunks_added=len(chunks),
    )
