from fastapi import APIRouter
from app.api.v1.endpoints import chat, users, crops, loans, market, weather, subsidies, voice

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(crops.router, prefix="/crops", tags=["crops"])
api_router.include_router(loans.router, prefix="/loans", tags=["loans"])
api_router.include_router(market.router, prefix="/market", tags=["market"])
api_router.include_router(weather.router, prefix="/weather", tags=["weather"])
api_router.include_router(subsidies.router, prefix="/subsidies", tags=["subsidies"])
api_router.include_router(voice.router, prefix="/voice", tags=["voice"])
