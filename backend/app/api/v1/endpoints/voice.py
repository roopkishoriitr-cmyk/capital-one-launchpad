import asyncio
import json
from typing import Dict, List, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from loguru import logger
from app.core.database import get_db
from app.core.voice_processor import voice_processor
from app.core.config import settings
from pydantic import BaseModel
import httpx

router = APIRouter()

# Pydantic models for requests and responses
class RealtimeSessionRequest(BaseModel):
    voice: str = "alloy"
    language: str = "hi"
    user_id: Optional[str] = None
    farmer_context: Optional[Dict[str, Any]] = None

class RealtimeSessionResponse(BaseModel):
    session_id: str
    model: str
    voice: str
    language: str
    status: str

class TTSRequest(BaseModel):
    text: str
    language: str = "hi"
    voice: str = "alloy"
    user_id: Optional[str] = None

class TTSResponse(BaseModel):
    audio_url: Optional[str] = None
    text: str
    language: str
    duration: float

class VoiceStatsResponse(BaseModel):
    api_provider: str
    total_queries_processed: int
    successful_conversions: int
    failed_conversions: int
    average_processing_time: float
    most_used_language: str
    language_usage: Dict[str, float]
    voice_usage: Dict[str, float]
    daily_average: int
    peak_usage_hours: List[str]
    last_updated: str

@router.post("/realtime/session", response_model=RealtimeSessionResponse)
async def create_realtime_session(
    request: RealtimeSessionRequest,
    db: Session = Depends(get_db)
):
    """Create a real-time session using OpenAI Realtime API for KrishiMitra"""
    endpoint_start_time = asyncio.get_event_loop().time()
    logger.info('🔄 ===== REALTIME SESSION CREATION STARTED =====')
    logger.info(f'📝 Request received - Voice: {request.voice}, Language: {request.language}, User ID: {request.user_id}')
    logger.info(f'📝 Request timestamp: {asyncio.get_event_loop().time()}')
    
    try:
        # Validate request parameters
        logger.info('🔍 Validating request parameters...')
        if not request.voice:
            logger.warning('⚠️ No voice specified in request, using default: alloy')
            request.voice = 'alloy'
        
        if not request.language:
            logger.warning('⚠️ No language specified in request, using default: hi')
            request.language = 'hi'
        
        logger.info(f'✅ Request validation passed - Voice: {request.voice}, Language: {request.language}')

        # Get farmer context (mock data for now)
        farmer_context = request.farmer_context or {
            "location": "Punjab, India",
            "crops": ["wheat", "rice", "cotton"],
            "experience": "15 years",
            "land_size": "10 acres",
            "current_concerns": ["loan repayment", "crop selection", "market prices"]
        }
        logger.info(f'👨‍🌾 Farmer context: {farmer_context}')

        # Language mapping for instructions
        language_names = {
            "hi": "Hindi", "bn": "Bengali", "ta": "Tamil", "te": "Telugu", "mr": "Marathi",
            "gu": "Gujarati", "pa": "Punjabi", "or": "Odia", "ml": "Malayalam", "kn": "Kannada", "en": "English"
        }
        
        language = language_names.get(request.language, "Hindi")
        voice = request.voice.lower()
        logger.info(f'🌍 Language mapping - Code: {request.language} -> Name: {language}')
        logger.info(f'🎵 Voice setting: {voice}')

        # Create KrishiMitra instructions (detailed prompt)
        logger.info('📝 Generating KrishiMitra instructions...')
        instructions = f"""You are KrishiMitra, an AI farming assistant for Indian farmers. You have comprehensive knowledge about farming in Punjab, India. 

**IMPORTANT: Always ask basic questions first to understand the farmer's situation before giving recommendations.**

**BASIC QUESTIONS TO ASK FIRST:**
1. **Land Information**: "आपके पास कितनी जमीन है?" (How much land do you have?)
2. **Current Crops**: "आप वर्तमान में कौन सी फसलें उगा रहे हैं?" (What crops are you currently growing?)
3. **Experience**: "आपको कितने साल का खेती का अनुभव है?" (How many years of farming experience do you have?)
4. **Financial Situation**: "क्या आपके पास कोई कर्ज है?" (Do you have any existing loans?)
5. **Water Availability**: "आपके पास किस तरह की सिंचाई सुविधा है?" (What type of irrigation do you have?)
6. **Location**: "आप पंजाब के किस जिले में हैं?" (Which district of Punjab are you in?)

**CONVERSATION FLOW:**
1. **Start with a warm greeting** in {language}
2. **Ask 2-3 basic questions** to understand their situation
3. **Listen to their responses** and ask follow-up questions if needed
4. **Then provide personalized recommendations** based on their specific situation
5. **Always be encouraging and supportive**

**KNOWLEDGE BASE FOR RECOMMENDATIONS:**

**LOAN INFORMATION FOR PUNJAB FARMERS:**
- Crop Loan: Up to ₹3,00,000, 7% interest rate, 12 months tenure
- Equipment Loan: Up to ₹5,00,000, 8.5% interest rate, 36 months tenure  
- Irrigation Loan: Up to ₹2,00,000, 7.5% interest rate, 24 months tenure
- Dairy Loan: Up to ₹10,00,000, 6.5% interest rate, 60 months tenure
- Horticulture Loan: Up to ₹4,00,000, 6.8% interest rate, 48 months tenure
- Best Bank: Punjab National Bank (6.8% crop loan rate)

**RECOMMENDED CROPS FOR PUNJAB (Current Season - {language}):**
1. Wheat: ₹42,000/acre profit, 120 days, ₹2,180/quintal market price
2. Potato: ₹66,000/acre profit, 90 days, ₹880/quintal market price  
3. Rice: ₹31,500/acre profit, 150 days, ₹1,880/quintal market price
4. Maize: ₹36,000/acre profit, 100 days, ₹1,680/quintal market price
5. Cotton: ₹29,250/acre profit, 180 days, ₹6,750/quintal market price
6. Sugarcane: ₹65,625/acre profit, 365 days, ₹325/quintal market price

**CURRENT MARKET PRICES (Punjab Mandis):**
- Wheat: ₹2,180 (Ludhiana), stable trend
- Rice: ₹1,880 (Ludhiana), increasing trend
- Maize: ₹1,680 (Ludhiana), stable trend
- Cotton: ₹6,750 (Ludhiana), decreasing trend
- Sugarcane: ₹325 (Ludhiana), stable trend
- Potato: ₹880 (Ludhiana), increasing trend

**GOVERNMENT SCHEMES FOR PUNJAB FARMERS:**
- PM-KISAN: ₹6,000/year (small and marginal farmers)
- Seed Subsidy: ₹500/quintal (small farmers)
- Fertilizer Subsidy: ₹1,400/bag (all farmers)
- Pesticide Subsidy: ₹300/liter (all farmers)
- Drip Irrigation Subsidy: ₹50,000 (farmers with 2+ acres)
- Farm Machinery Subsidy: Up to 40% of cost (farmers with 5+ acres)

**AGRONOMY TECHNIQUES FOR BETTER YIELD:**
- Drip Irrigation: 40-60% water saving
- Laser Land Leveling: 25% water use efficiency improvement
- Integrated Nutrient Management: Combine organic and inorganic fertilizers
- Integrated Pest Management: Cultural, biological, and chemical control
- Precision Agriculture: GPS guidance, variable rate technology
- Crop Rotation: Wheat-Rice-Maize rotation recommended

**RISK ASSESSMENT FOR PUNJAB:**
- Weather Risks: 15% drought probability, 10% flood probability, 25% heat wave probability
- Pest Risks: Fall armyworm (maize), Pink bollworm (cotton), Brown planthopper (rice)
- Market Risks: Wheat (medium volatility), Rice (high volatility), Cotton (very high volatility)
- Credit Risks: 8% loan default probability

**CONTACT INFORMATION:**
- Agriculture Department: 0172-2700711
- PM-KISAN Helpline: 1800-180-1551
- Common Service Center: 1800-3000-3468
- Punjab Cooperative Banks: Multiple branches

**PERSONALIZATION GUIDELINES:**
- **Small Farmers (1-2 acres)**: Focus on high-value crops, subsidies, and government schemes
- **Medium Farmers (2-10 acres)**: Balance between traditional and modern farming techniques
- **Large Farmers (10+ acres)**: Emphasize mechanization, contract farming, and export opportunities
- **New Farmers**: Provide basic guidance, recommend training programs
- **Experienced Farmers**: Focus on advanced techniques and market opportunities

**RESPONSE GUIDELINES:**
1. **Always ask questions first** to understand their situation
2. **Provide specific, actionable advice** based on their responses
3. **Include current market prices and trends**
4. **Mention relevant government schemes and subsidies**
5. **Suggest appropriate agronomy techniques**
6. **Assess risks and provide mitigation strategies**
7. **Give contact information for further assistance**
8. **Use {language} language primarily, but you can mix with English terms when needed**
9. **Be encouraging and supportive to farmers**
10. **Provide step-by-step guidance when possible**
11. **Always mention the financial benefits and ROI of recommendations**

**EXAMPLE CONVERSATION FLOW:**
Farmer: "मुझे कर्ज चाहिए और फसल की सलाह भी"
KrishiMitra: "नमस्कार! मैं आपकी मदद करूंगा। पहले कुछ बातें जाननी हैं:
1. आपके पास कितनी जमीन है?
2. आप वर्तमान में क्या उगा रहे हैं?
3. आपको कितने साल का अनुभव है?"

**IMPORTANT:**
- All data is current and specific to Punjab, India
- Focus on practical, implementable solutions
- Consider the farmer's financial situation and land size
- Emphasize government support and subsidies available
- Provide both short-term and long-term recommendations
- **Never give generic advice without understanding their situation first**

Remember: You are a trusted advisor to Indian farmers. Your goal is to help them maximize their profits while managing risks effectively. Always start by understanding their specific situation through questions."""

        logger.info(f'📋 Instructions prepared - Length: {len(instructions)} characters')
        logger.debug(f'📋 Instructions preview: {instructions[:200]}...')

        # Create realtime session using voice processor
        logger.info('🎤 Calling voice processor to create realtime session...')
        result = await voice_processor.create_realtime_session(voice, request.language, instructions)
        
        if not result["success"]:
            logger.error(f'❌ Voice processor failed to create session: {result["error"]}')
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating realtime session: {result['error']}"
            )

        logger.info('✅ Voice processor session creation successful')
        logger.info(f'🎉 Session created - ID: {result["session_id"]}, Model: {result["model"]}')

        endpoint_duration = asyncio.get_event_loop().time() - endpoint_start_time
        logger.info(f'⏱️ Total endpoint processing time: {endpoint_duration:.2f} seconds')
        logger.info('✅ ===== REALTIME SESSION CREATION COMPLETED =====')

        return RealtimeSessionResponse(
            session_id=result["session_id"],
            model=result["model"],
            voice=voice,
            language=language,
            status=result["status"]
        )

    except Exception as e:
        endpoint_duration = asyncio.get_event_loop().time() - endpoint_start_time
        logger.error(f'💥 ===== REALTIME SESSION CREATION FAILED =====')
        logger.error(f'❌ Error after {endpoint_duration:.2f} seconds: {e}')
        logger.error(f'❌ Error type: {type(e).__name__}')
        logger.error(f'❌ Error details: {str(e)}')
        logger.error(f'❌ Request params - Voice: {request.voice}, Language: {request.language}, User ID: {request.user_id}')
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating realtime session: {str(e)}"
        )

@router.post("/text-to-speech", response_model=TTSResponse)
async def text_to_speech(
    request: TTSRequest,
    db: Session = Depends(get_db)
):
    """Convert text to speech using OpenAI TTS (for non-realtime responses)"""
    endpoint_start_time = asyncio.get_event_loop().time()
    logger.info('🔊 ===== TEXT-TO-SPEECH CONVERSION STARTED =====')
    logger.info(f'📝 TTS Request - Text length: {len(request.text)}, Language: {request.language}, Voice: {request.voice}')
    logger.info(f'📝 User ID: {request.user_id}')
    logger.debug(f'📄 Text preview: {request.text[:100]}...')
    
    try:
        # Validate request parameters
        logger.info('🔍 Validating TTS request parameters...')
        if not request.text:
            logger.error('❌ No text provided in TTS request')
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text is required for TTS conversion"
            )
        
        if not request.language:
            logger.warning('⚠️ No language specified, using default: hi')
            request.language = 'hi'
        
        if not request.voice:
            logger.warning('⚠️ No voice specified, using default: alloy')
            request.voice = 'alloy'
        
        logger.info(f'✅ TTS request validation passed')
        
        # Process text to speech using OpenAI TTS
        logger.info('🎤 Calling voice processor for TTS conversion...')
        result = await voice_processor.text_to_speech(request.text, request.language)
        
        if not result["success"]:
            logger.error(f'❌ Voice processor TTS conversion failed: {result["error"]}')
            logger.error(f'❌ Error type: {result.get("error_type", "unknown")}')
            logger.error(f'❌ Processing time: {result.get("processing_time", 0):.2f} seconds')
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"]
            )
        
        logger.info(f'✅ TTS conversion successful')
        logger.info(f'🎵 Audio generated - Size: {result.get("audio_size", 0)} bytes, Duration: {result.get("duration", 0):.2f}s')
        logger.info(f'⏱️ TTS processing time: {result.get("processing_time", 0):.2f} seconds')
        
        endpoint_duration = asyncio.get_event_loop().time() - endpoint_start_time
        logger.info(f'⏱️ Total TTS endpoint processing time: {endpoint_duration:.2f} seconds')
        logger.info('✅ ===== TEXT-TO-SPEECH CONVERSION COMPLETED =====')
        
        return TTSResponse(
            audio_url=None,  # Audio data is returned directly
            text=request.text,
            language=request.language,
            duration=result["duration"]
        )
        
    except Exception as e:
        endpoint_duration = asyncio.get_event_loop().time() - endpoint_start_time
        logger.error(f'💥 ===== TEXT-TO-SPEECH CONVERSION FAILED =====')
        logger.error(f'❌ Error after {endpoint_duration:.2f} seconds: {e}')
        logger.error(f'❌ Error type: {type(e).__name__}')
        logger.error(f'❌ Error details: {str(e)}')
        logger.error(f'❌ Request params - Text length: {len(request.text)}, Language: {request.language}, Voice: {request.voice}')
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing text to speech"
        )

@router.get("/available-voices")
async def get_available_voices():
    """Get list of available voices"""
    try:
        voices = voice_processor.get_available_voices()
        return {
            "voices": voices,
            "default_voice": "alloy",
            "api_provider": "OpenAI"
        }
    except Exception as e:
        logger.error(f"❌ Error getting available voices: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting available voices"
        )

@router.get("/voice-stats", response_model=VoiceStatsResponse)
async def get_voice_stats():
    """Get voice processing statistics"""
    try:
        # Mock statistics for now
        stats = {
            "api_provider": "OpenAI Realtime API",
            "total_queries_processed": 1250,
            "successful_conversions": 1180,
            "failed_conversions": 70,
            "average_processing_time": 1.8,
            "most_used_language": "hi",
            "language_usage": {
                "hi": 45, "bn": 15, "ta": 12, "te": 10, "mr": 8,
                "gu": 5, "pa": 3, "or": 1, "ml": 0.5, "kn": 0.5
            },
            "voice_usage": {
                "alloy": 60, "echo": 20, "nova": 10, "onyx": 5, "fable": 3, "shimmer": 2
            },
            "daily_average": 42,
            "peak_usage_hours": ["09:00", "12:00", "18:00"],
            "last_updated": "2024-01-15T10:30:00Z"
        }
        
        return VoiceStatsResponse(**stats)
        
    except Exception as e:
        logger.error(f"❌ Error getting voice stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting voice statistics"
        )

@router.get("/voice-preview")
async def get_voice_preview(
    text: str = "नमस्कार! मैं KrishiMitra हूं।",
    language: str = "hi",
    voice: str = "alloy"
):
    """Get voice preview for testing"""
    try:
        result = await voice_processor.get_voice_preview(text, language, voice)
        
        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"]
            )
        
        return {
            "success": True,
            "preview_text": result["preview_text"],
            "language": result["language"],
            "voice": result["voice"],
            "duration": result["duration"]
        }
        
    except Exception as e:
        logger.error(f"❌ Error in voice preview: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error generating voice preview"
        )
