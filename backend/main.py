from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
import os
import json
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1.api import api_router
from app.core.websocket_manager import WebSocketManager
from app.agents.agent_orchestrator import AgentOrchestrator

# Create database tables
Base.metadata.create_all(bind=engine)

# WebSocket manager
websocket_manager = WebSocketManager()

# Agent orchestrator
agent_orchestrator = AgentOrchestrator()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting KrishiSampann - Where Crops Meet Capital")
    await agent_orchestrator.initialize()
    yield
    # Shutdown
    print("🛑 Shutting down KrishiSampann")

app = FastAPI(
    title="KrishiSampann API",
    description="AI-powered agronomy and financial advisory platform for Indian farmers",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

# WebSocket endpoint for real-time communication
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket_manager.connect(websocket, client_id)
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            
            # Parse the incoming data
            try:
                message_data = json.loads(data)
                query = message_data.get("message", data)
                language = message_data.get("language", "hi")
            except json.JSONDecodeError:
                query = data
                language = "hi"
            
            # Process with KrishiMitra (OpenAI)
            response = await agent_orchestrator.process_query(query, client_id, language)
            
            # Send response back to client
            await websocket.send_text(json.dumps(response))
            
    except WebSocketDisconnect:
        websocket_manager.disconnect(client_id)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "KrishiSampann",
        "version": "1.0.0",
        "message": "Kisan ka digital saathi chal raha hai"
    }

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "KrishiSampann - Where Crops Meet Capital",
        "tagline": "Be it the seed in your hand or the loan on your head — both must be nurtured wisely to bear fruit.",
        "status": "running",
        "docs": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
