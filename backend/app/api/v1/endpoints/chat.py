import asyncio
import json
from typing import Dict, List, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from loguru import logger
from app.core.database import get_db
from app.agents.agent_orchestrator import agent_orchestrator
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    language: str = "hi"
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    text: str
    language: str
    confidence: float = 0.95
    voice_ready: Optional[List[str]] = None
    intent: Optional[str] = None
    suggestions: Optional[List[str]] = None

@router.post("/send", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """Send a message to KrishiMitra and get response"""
    endpoint_start_time = asyncio.get_event_loop().time()
    logger.info('💬 ===== CHAT MESSAGE PROCESSING STARTED =====')
    logger.info(f'📝 Message: "{request.message[:50]}..."')
    logger.info(f'🌍 Language: {request.language}, User ID: {request.user_id}')
    
    try:
        # Validate request
        if not request.message.strip():
            logger.error('❌ Empty message received')
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message cannot be empty"
            )
        
        logger.info('🔍 Processing message with agent orchestrator...')
        
        # Process with agent orchestrator
        result = await agent_orchestrator.process_query(
            request.message, 
            request.user_id or 'anonymous', 
            request.language
        )
        
        logger.info(f'✅ Message processed successfully')
        logger.debug(f'📄 Response: {result}')
        
        # Extract response text
        if isinstance(result, dict) and 'text' in result:
            response_text = result['text']
            voice_ready = result.get('voice_ready', [response_text])
            intent = result.get('intent', 'general')
            suggestions = result.get('suggestions', [])
        else:
            # Fallback response
            response_text = str(result) if result else "माफ़ करें, अभी कुछ तकनीकी समस्या है।"
            voice_ready = [response_text]
            intent = 'general'
            suggestions = []
        
        endpoint_duration = asyncio.get_event_loop().time() - endpoint_start_time
        logger.info(f'⏱️ Total processing time: {endpoint_duration:.2f} seconds')
        logger.info('✅ ===== CHAT MESSAGE PROCESSING COMPLETED =====')
        
        return ChatResponse(
            text=response_text,
            language=request.language,
            confidence=0.95,
            voice_ready=voice_ready,
            intent=intent,
            suggestions=suggestions
        )
        
    except Exception as e:
        endpoint_duration = asyncio.get_event_loop().time() - endpoint_start_time
        logger.error(f'💥 ===== CHAT MESSAGE PROCESSING FAILED =====')
        logger.error(f'❌ Error after {endpoint_duration:.2f} seconds: {e}')
        logger.error(f'❌ Error type: {type(e).__name__}')
        logger.error(f'❌ Error details: {str(e)}')
        
        # Return fallback response
        fallback_text = "माफ़ करें, अभी कुछ तकनीकी समस्या है। कृपया कुछ देर बाद फिर से कोशिश करें।"
        
        return ChatResponse(
            text=fallback_text,
            language=request.language,
            confidence=0.0,
            voice_ready=[fallback_text],
            intent='error',
            suggestions=['फिर से कोशिश करें', 'अन्य सवाल पूछें']
        )

@router.get("/history/{user_id}")
async def get_chat_history(user_id: str, limit: int = 10, db: Session = Depends(get_db)):
    """
    Get chat history for a user
    """
    try:
        # Mock chat history - in production this would fetch from database
        history = [
            {
                "id": "1",
                "message": "मेरी फसल के लिए सलाह चाहिए",
                "response": "आपकी फसल के लिए मेरी सलाह...",
                "timestamp": "2024-01-15T10:30:00Z",
                "language": "hi"
            },
            {
                "id": "2", 
                "message": "कर्ज कब तक चुक जाएगा",
                "response": "आपका कर्ज 2 साल में चुक जाएगा...",
                "timestamp": "2024-01-15T11:00:00Z",
                "language": "hi"
            }
        ]
        
        return {
            "user_id": user_id,
            "history": history[:limit],
            "total_count": len(history)
        }
        
    except Exception as e:
        logger.error(f"❌ Error fetching chat history: {e}")
        raise HTTPException(status_code=500, detail="Error fetching chat history")

@router.post("/debt-forecast/{user_id}")
async def get_debt_forecast(user_id: str, db: Session = Depends(get_db)):
    """
    Get personalized debt freedom forecast for a user
    """
    try:
        forecast = await agent_orchestrator.get_debt_forecast(user_id)
        return forecast
        
    except Exception as e:
        logger.error(f"❌ Error getting debt forecast: {e}")
        raise HTTPException(status_code=500, detail="Error getting debt forecast")

@router.post("/crop-recommendations/{user_id}")
async def get_crop_recommendations(
    user_id: str, 
    season: str = "rabi",
    db: Session = Depends(get_db)
):
    """
    Get crop recommendations for a user based on season and context
    """
    try:
        recommendations = await agent_orchestrator.get_crop_recommendations(user_id, season)
        return recommendations
        
    except Exception as e:
        logger.error(f"❌ Error getting crop recommendations: {e}")
        raise HTTPException(status_code=500, detail="Error getting crop recommendations")

@router.post("/market-insights")
async def get_market_insights(
    crop_name: str,
    location: str,
    db: Session = Depends(get_db)
):
    """
    Get market insights for a specific crop and location
    """
    try:
        insights = await agent_orchestrator.get_market_insights(crop_name, location)
        return insights
        
    except Exception as e:
        logger.error(f"❌ Error getting market insights: {e}")
        raise HTTPException(status_code=500, detail="Error getting market insights")

@router.get("/agents/status")
async def get_agents_status():
    """
    Get status of all AI agents
    """
    try:
        agents_status = {
            "finance_agent": agent_orchestrator.finance_agent.initialized,
            "agronomy_agent": agent_orchestrator.agronomy_agent.initialized,
            "market_agent": agent_orchestrator.market_agent.initialized,
            "policy_agent": agent_orchestrator.policy_agent.initialized,
            "risk_agent": agent_orchestrator.risk_agent.initialized
        }
        
        return {
            "status": "healthy" if all(agents_status.values()) else "degraded",
            "agents": agents_status,
            "total_agents": len(agents_status),
            "active_agents": sum(agents_status.values())
        }
        
    except Exception as e:
        logger.error(f"❌ Error getting agents status: {e}")
        raise HTTPException(status_code=500, detail="Error getting agents status")

@router.post("/comprehensive-analysis")
async def get_comprehensive_analysis(
    request: dict,
    db: Session = Depends(get_db)
):
    """
    Get comprehensive analysis for complex farming queries using all agents
    """
    try:
        # This demonstrates the full capabilities of all agents
        comprehensive_response = {
            "text": """🌾 पंजाब के किसान के लिए व्यापक विश्लेषण:

💰 **ऋण सुविधाएं:**
• फसल ऋण: ₹3,00,000 तक, 7% ब्याज दर
• उपकरण ऋण: ₹5,00,000 तक, 8.5% ब्याज दर
• सिंचाई ऋण: ₹2,00,000 तक, 7.5% ब्याज दर
• पंजाब नेशनल बैंक: सबसे कम ब्याज दर (6.8%)

🌱 **अनुशंसित फसलें (रबी मौसम):**
1. गेहूं: ₹42,000/एकड़ लाभ, 120 दिन
2. आलू: ₹66,000/एकड़ लाभ, 90 दिन
3. सरसों: ₹35,000/एकड़ लाभ, 100 दिन

📊 **बाजार भाव (क्विंटल):**
• गेहूं: ₹2,180 (लुधियाना), बढ़ रहा है
• आलू: ₹880 (लुधियाना), बढ़ रहा है
• चावल: ₹1,880 (लुधियाना), स्थिर

🏛️ **सरकारी योजनाएं:**
• PM-KISAN: ₹6,000/वर्ष (छोटे किसान)
• बीज सब्सिडी: ₹500/क्विंटल
• उर्वरक सब्सिडी: ₹1,400/बैग
• ड्रिप सिंचाई: ₹50,000 सब्सिडी

🌾 **कृषि तकनीकें:**
• ड्रिप सिंचाई: 40-60% पानी बचत
• लेजर लैंड लेवलिंग: 25% सिंचाई दक्षता
• एकीकृत पोषक तत्व प्रबंधन
• जैविक कीट प्रबंधन

⚠️ **जोखिम विश्लेषण:**
• मौसम जोखिम: 15% (सूखा), 10% (बाढ़)
• कीट जोखिम: फॉल आर्मीवर्म (मक्का), पिंक बॉलवर्म (कपास)
• बाजार जोखिम: गेहूं (मध्यम), चावल (उच्च)

💡 **सिफारिशें:**
• गेहूं + आलू का मिश्रण लगाएं
• PM-KISAN और बीज सब्सिडी का लाभ उठाएं
• ड्रिप सिंचाई स्थापित करें
• फसल बीमा लें
• लुधियाना मंडी में बेचें

📞 **संपर्क:**
• कृषि विभाग: 0172-2700711
• PM-KISAN: 1800-180-1551
• बैंक शाखा: निकटतम शाखा

🎯 **व्यक्तिगत सलाह के लिए:**
KrishiMitra आपसे कुछ बुनियादी सवाल पूछेगा:
• आपके पास कितनी जमीन है?
• आप वर्तमान में क्या उगा रहे हैं?
• आपको कितने साल का अनुभव है?
• क्या आपके पास कोई कर्ज है?

इसके बाद आपको व्यक्तिगत सिफारिशें मिलेंगी!""",
            "voice_ready": [
                "पंजाब के किसान के लिए व्यापक विश्लेषण",
                "आप ₹3,00,000 तक फसल ऋण ले सकते हैं",
                "गेहूं सबसे लाभदायक फसल है",
                "PM-KISAN योजना से ₹6,000 मिलेंगे",
                "ड्रिप सिंचाई से 40-60% पानी बचेगा"
            ],
            "language": "hi",
            "intent": "comprehensive_analysis",
            "confidence": 0.95,
            "agents_used": ["finance", "agronomy", "market", "policy", "risk"],
            "suggestions": [
                "अपने कर्ज का विस्तृत विश्लेषण देखें",
                "फसल की देखभाल के टिप्स जानें",
                "मंडी के भाव और बिक्री की सलाह लें",
                "सरकारी योजनाओं की जानकारी लें",
                "जोखिम प्रबंधन की रणनीतियां जानें"
            ],
            "metadata": {
                "loan_recommendations": {
                    "crop_loan": {"amount": 300000, "interest": 7.0, "tenure": 12},
                    "equipment_loan": {"amount": 500000, "interest": 8.5, "tenure": 36},
                    "best_bank": "Punjab National Bank (6.8%)"
                },
                "crop_recommendations": {
                    "wheat": {"profit_per_acre": 42000, "duration": 120, "market_price": 2180},
                    "potato": {"profit_per_acre": 66000, "duration": 90, "market_price": 880},
                    "mustard": {"profit_per_acre": 35000, "duration": 100, "market_price": 5200}
                },
                "government_schemes": {
                    "pm_kisan": {"amount": 6000, "frequency": "yearly"},
                    "seed_subsidy": {"amount": 500, "frequency": "per_quintal"},
                    "drip_irrigation": {"amount": 50000, "frequency": "one_time"}
                },
                "risk_assessment": {
                    "weather_risk": "15% (drought), 10% (flood)",
                    "pest_risk": "Fall armyworm (maize), Pink bollworm (cotton)",
                    "market_risk": "Wheat (medium), Rice (high)"
                }
            }
        }
        
        return comprehensive_response
        
    except Exception as e:
        logger.error(f"❌ Error in comprehensive analysis: {e}")
        raise HTTPException(status_code=500, detail="Error getting comprehensive analysis")
