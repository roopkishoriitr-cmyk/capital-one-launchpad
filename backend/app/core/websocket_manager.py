from fastapi import WebSocket
from typing import Dict, List
import json
import asyncio
from loguru import logger

class WebSocketManager:
    """
    Manages WebSocket connections for real-time communication
    between the frontend and AI agents.
    """
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_sessions: Dict[str, Dict] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        """Accept a new WebSocket connection"""
        await websocket.accept()
        self.active_connections[client_id] = websocket
        
        # Initialize user session
        self.user_sessions[client_id] = {
            "language": "hi",
            "context": {},
            "conversation_history": []
        }
        
        logger.info(f"🔗 WebSocket connected: {client_id}")
        
        # Send welcome message
        welcome_message = {
            "type": "welcome",
            "message": "नमस्कार! मैं KrishiSampann हूँ, आपका कृषि और वित्तीय सलाहकार।",
            "language": "hi"
        }
        await self.send_message(client_id, welcome_message)
    
    def disconnect(self, client_id: str):
        """Remove a WebSocket connection"""
        if client_id in self.active_connections:
            del self.active_connections[client_id]
        
        if client_id in self.user_sessions:
            del self.user_sessions[client_id]
        
        logger.info(f"🔌 WebSocket disconnected: {client_id}")
    
    async def send_message(self, client_id: str, message: Dict):
        """Send a message to a specific client"""
        if client_id in self.active_connections:
            try:
                await self.active_connections[client_id].send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"❌ Error sending message to {client_id}: {e}")
                self.disconnect(client_id)
    
    async def broadcast_message(self, message: Dict):
        """Send a message to all connected clients"""
        disconnected_clients = []
        
        for client_id, websocket in self.active_connections.items():
            try:
                await websocket.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"❌ Error broadcasting to {client_id}: {e}")
                disconnected_clients.append(client_id)
        
        # Clean up disconnected clients
        for client_id in disconnected_clients:
            self.disconnect(client_id)
    
    def get_user_session(self, client_id: str) -> Dict:
        """Get user session data"""
        return self.user_sessions.get(client_id, {})
    
    def update_user_session(self, client_id: str, updates: Dict):
        """Update user session data"""
        if client_id in self.user_sessions:
            self.user_sessions[client_id].update(updates)
    
    def add_conversation_history(self, client_id: str, query: str, response: str):
        """Add conversation to user's history"""
        if client_id in self.user_sessions:
            self.user_sessions[client_id]["conversation_history"].append({
                "query": query,
                "response": response,
                "timestamp": asyncio.get_event_loop().time()
            })
            
            # Keep only last 10 conversations
            if len(self.user_sessions[client_id]["conversation_history"]) > 10:
                self.user_sessions[client_id]["conversation_history"] = \
                    self.user_sessions[client_id]["conversation_history"][-10:]
    
    def get_active_connections_count(self) -> int:
        """Get number of active connections"""
        return len(self.active_connections)
    
    def get_connected_clients(self) -> List[str]:
        """Get list of connected client IDs"""
        return list(self.active_connections.keys())
