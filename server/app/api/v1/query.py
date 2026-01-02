from fastapi import APIRouter, Depends, Request, Query
from app.database import AsyncSessionDep
from app.api.dependencies import CurrentUserDep
from app.services.query_service import QueryService
from app.schemas.query import QueryResponseDTO, QueryRequest
from typing import List
from app.services.pinecone_service import PineconeService

query_router = APIRouter(prefix="/api/v1/contracts", tags=["contract-queries"])

query_service = QueryService()

@query_router.post(
    "/queries",
    response_model=QueryResponseDTO,
    status_code=201,
    summary="Query contract document with RAG",
    description="Submit a question about a contract document and receive AI-powered analysis"
)
async def query_document(
    request: Request,
    payload: QueryRequest,
    db: AsyncSessionDep,
    user: CurrentUserDep
) -> QueryResponseDTO:
    # Get Pinecone from app state
    pinecone_service : PineconeService = request.app.state.pinecone_service
    

    query_response = await query_service.process_contract_query(
        query_text=payload.query_text,
        document_id=payload.document_id,
        user_id=user.id,
        pinecone_service=pinecone_service,
        db=db
    )
    

    return QueryResponseDTO(
        id=query_response.id,
        response_text=query_response.response_text,
        created_at=query_response.created_at,
        query_text=query_response.query_text
    )


@query_router.get(
    "/queries",
    response_model=List[QueryResponseDTO],
    status_code=200,
    summary="Fetch all queries for a document"
)
async def fetch_queries(
    user: CurrentUserDep,
    db: AsyncSessionDep,
    document_id: str = Query(..., description="Document ID"),
) -> List[QueryResponseDTO]:

    return await query_service.get_document_queries(
        user_id=user.id,
        document_id=document_id,
        db=db
    )