from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.redis_client import redis_client
from app.config import Settings
from app.api.v1.auth import router
from app.middleware.auth import AuthMiddleware

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
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    AuthMiddleware,
    protected_paths=["/api/v1/me", "/api/v1/sign_out"]
)



@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "FastAPI Authentication System",
        "docs": "/docs" if True else "Disabled in production",
        "health": "/health"
    }
    
    
app.include_router(router)    

if __name__ == "__main__": 
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )