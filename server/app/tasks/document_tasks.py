from app.celery_app import celery_app
from app.models.document import Document, DocumentChunk, ProcessingStatus
from app.models.user import User
from app.services.unstructured_service import UnstructuredService
from app.services.gemini_service import GeminiService
from app.services.pinecone_service import PineconeService
from sqlalchemy.exc import SQLAlchemyError
from app.core.exceptions import DocumentProcessingError, VectorStoreError
import logging
import asyncio
from app.config import Settings

settings = Settings()
logger = logging.getLogger(__name__)

# In your database.py or config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Sync engine for Celery
sync_engine = create_engine(
    settings.database_url.replace('postgresql+asyncpg://', 'postgresql+psycopg2://'),
    pool_pre_ping=True
)

SyncSessionLocal = sessionmaker(bind=sync_engine, expire_on_commit=False)

@celery_app.task(bind=True, name='process_document')
def process_document_task(self, document_id: str):
    
    with SyncSessionLocal() as db:
        document = None
        try:
            document = db.get(Document, document_id)
            
            if not document:
                raise DocumentProcessingError(f"Document {document_id} not found")
            
            document.processing_status = ProcessingStatus.PROCESSING.value
            db.commit()
            db.refresh(document)
            
            # Step 1: Parse PDF (separate event loop)
            unstructured_service = UnstructuredService()
            chunks_data = asyncio.run(unstructured_service.parse_pdf(document.cloudinary_url))
            
            # Step 2: Summarize chunks (separate event loop)
            gemini_service = GeminiService()
            summarised_chunks = asyncio.run(gemini_service.summarize_chunks(chunks=chunks_data))
            
            # Step 3: Prepare embeddings (sync)
            embedding_vectors = [
                {
                    "embedding_id": chunk['embed_data']['embedding_id'],
                    "embedding": chunk['embed_data']['embedding']
                }
                for chunk in summarised_chunks
            ]
            
            # Step 4: ALL Pinecone operations in ONE event loop
            async def handle_pinecone():
                """Execute all Pinecone operations in single async context"""
                pinecone_service = PineconeService()
                try:
                    await pinecone_service.connect()
                    result = await pinecone_service.upsert_embeddings(embedding_vectors)
                    return result
                finally:
                    await pinecone_service.disconnect()
            
            # Run all Pinecone operations together
            pinecone_result = asyncio.run(handle_pinecone())
            logger.info(f"Upserted {pinecone_result['upserted_count']} embeddings to Pinecone")
            
            # Step 5: Save chunks to DB (sync)
            chunks = []
            for data in summarised_chunks:
                chunk = DocumentChunk(
                    document_id=document_id,
                    embedding_id=data['embed_data']['embedding_id'],
                    content=data['metadata'],
                    summary=data['summary']
                )
                chunks.append(chunk)
            
            db.add_all(chunks)
            db.commit()
            
            logger.info(f"Successfully saved {len(chunks)} chunks")
            
            # Step 6: Update document status
            document.processing_status = ProcessingStatus.COMPLETED.value
            db.commit()
            
        except (SQLAlchemyError, VectorStoreError, DocumentProcessingError) as exc:
            if document:
                db.rollback()
                document.processing_status = ProcessingStatus.FAILED.value
                document.error_message = str(exc)
                db.commit()
            logger.error(f"Processing failed for document {document_id}: {str(exc)}")
            raise self.retry(exc=exc)
        
        except Exception as exc:
            if document:
                db.rollback()
                document.processing_status = ProcessingStatus.FAILED.value
                document.error_message = str(exc)
                db.commit()
            logger.error(f"Unexpected failure for document {document_id}: {str(exc)}")
            raise