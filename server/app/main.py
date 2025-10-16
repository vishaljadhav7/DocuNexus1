from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.redis_client import redis_client
from app.config import Settings
from app.api.v1.auth import router
from app.middleware.auth import AuthMiddleware
from app.api.v1.document import document_router
from app.services.pinecone_service import PineconeService

settings = Settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    print("Starting up...")
    
    # Startup phase - initialize services in order
    try:
        # 1. Database
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            await conn.commit()
            print("Database initialized successfully")
        
        # 2. Redis
        await redis_client.connect(settings.redis_url)
        print("Redis connected successfully")
        
        
        # 3. Pinecone - manual lifecycle management
        pinecone_service = PineconeService()
        await pinecone_service.connect()
        app.state.pinecone_service = pinecone_service
        print("Pinecone connected successfully")
        
        
        print("All services initialized successfully")
        
    except Exception as e:

        await redis_client.disconnect()
        await engine.dispose()
        raise
    
    # Application runs here
    yield
    
    # Shutdown phase - cleanup in reverse order
    print("Shutting down...")

    try:
        # 3. Pinecone (last in, first out)
        if hasattr(app.state, 'pinecone_service'):
            await app.state.pinecone_service.disconnect()
            print("Pinecone disconnected successfully")
    except Exception as e:
        print(f"Error disconnecting Pinecone: {str(e)}")
    
    try:
        # 2. Redis
        await redis_client.disconnect()
        print("Redis disconnected successfully")
    except Exception as e:
        print(f"Error disconnecting Redis: {str(e)}")
    
    try:
        # 1. Database
        await engine.dispose()
        print("Database connections closed successfully")
    except Exception as e:
        print(f"Error disposing database: {str(e)}")

app = FastAPI(
    lifespan=lifespan
)

app.add_middleware(
    AuthMiddleware,
    protected_paths=["/api/v1/me", "/api/v1/sign_out", "/api/v1/documents"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


   


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "FastAPI Authentication System",
        "docs": "/docs" if True else "Disabled in production",
        "health": "/health"
    }
    
    
routers_to_include = [router, document_router]     

for routes in routers_to_include:
    app.include_router(routes)     

if __name__ == "__main__": 
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )