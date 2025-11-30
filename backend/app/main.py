"""
FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print(f"🚀 Starting {settings.app_name} v{settings.app_version}")
    print(f"📊 Database: {settings.database_url}")
    print(f"📁 Log directory: {settings.log_dir}")
    print(f"🔐 Encryption: {'Enabled' if settings.encryption_key else 'Disabled'}")

    yield

    # Shutdown
    print("👋 Shutting down application...")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="A web-based SSH client similar to MobaXterm/Xshell/PuTTY",
    lifespan=lifespan,
)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return JSONResponse(
        content={
            "status": "healthy",
            "app": settings.app_name,
            "version": settings.app_version,
        }
    )


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/health",
    }


# API routes will be added here
# from app.api import sessions, servers, credentials, logs, websocket
# app.include_router(sessions.router, prefix="/api/sessions", tags=["Sessions"])
# app.include_router(servers.router, prefix="/api/servers", tags=["Servers"])
# app.include_router(credentials.router, prefix="/api/credentials", tags=["Credentials"])
# app.include_router(logs.router, prefix="/api/logs", tags=["Logs"])
# app.include_router(websocket.router, prefix="/ws", tags=["WebSocket"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.backend_host,
        port=settings.backend_port,
        reload=settings.debug,
    )
