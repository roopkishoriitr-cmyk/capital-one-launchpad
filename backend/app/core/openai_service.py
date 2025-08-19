import asyncio
import json
from typing import Dict, List, Any, Optional
from openai import AsyncOpenAI
from loguru import logger
from app.core.config import settings

class OpenAIService:
    """
    Real-time OpenAI service for KrishiSampann with voice-first responses
    """
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.conversation_history: Dict[str, List[Dict]] = {}
        
    async def get_krishi_mitra_response(self, query: str, user_id: str, language: str = "hi") -> Dict[str, Any]:
        """
        Get a comprehensive response from KrishiMitra (AI assistant)
        with voice-first approach and contextual understanding
        """
        try:
            # Build conversation context
            context = await self._build_context(query, user_id, language)
            
            # Create system prompt for KrishiMitra
            system_prompt = self._create_krishi_mitra_prompt(language)
            
            # Get conversation history
            history = self.conversation_history.get(user_id, [])
            
            # Prepare messages
            messages = [
                {"role": "system", "content": system_prompt},
                *history[-10:],  # Last 10 messages for context
                {"role": "user", "content": query}
            ]
            
            # Get response from OpenAI
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=500,
                temperature=0.7,
                presence_penalty=0.1,
                frequency_penalty=0.1
            )
            
            ai_response = response.choices[0].message.content
            
            # Update conversation history
            self._update_conversation_history(user_id, query, ai_response)
            
            # Process response for voice-first delivery
            processed_response = await self._process_for_voice(ai_response, language)
            
            return {
                "text": ai_response,
                "voice_ready": processed_response["voice_ready"],
                "language": language,
                "intent": await self._detect_intent(query, language),
                "confidence": 0.95,
                "suggestions": await self._generate_suggestions(query, language)
            }
            
        except Exception as e:
            logger.error(f"❌ Error in OpenAI service: {e}")
            return self._get_fallback_response(language)
    
    def _create_krishi_mitra_prompt(self, language: str) -> str:
        """Create a comprehensive system prompt for KrishiMitra"""
        
        if language == "hi":
            return """आप KrishiMitra हैं - भारतीय किसानों के लिए एक AI सहायक। आपकी विशेषताएं:

1. **वॉइस-फर्स्ट**: आपका प्राथमिक लक्ष्य बोलकर जवाब देना है
2. **किसान-केंद्रित**: सरल, व्यावहारिक सलाह दें
3. **बहुभाषी**: हिंदी में प्राथमिक रूप से बात करें
4. **विशेषज्ञता**: फसल, ऋण, मंडी, मौसम, सरकारी योजनाएं

आपका स्वभाव:
- दोस्ताना और सहायक
- सरल भाषा में जटिल जानकारी
- व्यावहारिक समाधान
- स्थानीय संदर्भ के साथ

हमेशा वॉइस के लिए अनुकूलित जवाब दें - छोटे वाक्य, स्पष्ट उच्चारण, और बोलने में आसान।"""
        
        else:
            return """You are KrishiMitra - an AI assistant for Indian farmers. Your characteristics:

1. **Voice-First**: Your primary goal is to respond by speaking
2. **Farmer-Centric**: Give simple, practical advice
3. **Multilingual**: Primarily speak in Hindi, but can use English when needed
4. **Expertise**: Crops, loans, markets, weather, government schemes

Your personality:
- Friendly and helpful
- Complex information in simple language
- Practical solutions
- With local context

Always give voice-optimized responses - short sentences, clear pronunciation, and easy to speak."""
    
    async def _build_context(self, query: str, user_id: str, language: str) -> Dict[str, Any]:
        """Build context for the AI response"""
        # This would typically fetch user data, location, crops, etc.
        return {
            "user_id": user_id,
            "language": language,
            "location": "India",  # Would be fetched from user profile
            "current_season": "Kharif",  # Would be calculated
            "user_crops": ["wheat", "rice"],  # Would be fetched
            "user_loans": [],  # Would be fetched
            "timestamp": asyncio.get_event_loop().time()
        }
    
    async def _process_for_voice(self, text: str, language: str) -> Dict[str, Any]:
        """Process text response for optimal voice delivery"""
        # Break into shorter sentences for better speech
        sentences = text.split('. ')
        voice_ready_sentences = []
        
        for sentence in sentences:
            if len(sentence) > 100:
                # Break long sentences
                parts = sentence.split(', ')
                voice_ready_sentences.extend(parts)
            else:
                voice_ready_sentences.append(sentence)
        
        return {
            "voice_ready": voice_ready_sentences,
            "total_duration": len(voice_ready_sentences) * 3,  # ~3 seconds per sentence
            "pause_points": [i for i, s in enumerate(voice_ready_sentences) if len(s) > 50]
        }
    
    async def _detect_intent(self, query: str, language: str) -> str:
        """Detect the intent of the user query"""
        intent_keywords = {
            "crop_advice": ["फसल", "बीज", "खाद", "कीट", "crop", "seed", "fertilizer"],
            "loan_help": ["ऋण", "कर्ज", "पैसा", "loan", "money", "credit"],
            "market_info": ["मंडी", "भाव", "बिक्री", "market", "price", "sell"],
            "weather": ["मौसम", "बारिश", "weather", "rain"],
            "government": ["सरकार", "योजना", "सब्सिडी", "government", "scheme"]
        }
        
        query_lower = query.lower()
        for intent, keywords in intent_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                return intent
        
        return "general_inquiry"
    
    async def _generate_suggestions(self, query: str, language: str) -> List[str]:
        """Generate follow-up suggestions based on the query"""
        if language == "hi":
            return [
                "अपनी फसल के बारे में और जानें",
                "मंडी भाव की जानकारी लें",
                "सरकारी योजनाओं के बारे में पूछें",
                "मौसम की जानकारी लें"
            ]
        else:
            return [
                "Learn more about your crops",
                "Get market price information",
                "Ask about government schemes",
                "Get weather information"
            ]
    
    def _update_conversation_history(self, user_id: str, user_query: str, ai_response: str):
        """Update conversation history for context"""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        self.conversation_history[user_id].extend([
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": ai_response}
        ])
        
        # Keep only last 20 messages to prevent context overflow
        if len(self.conversation_history[user_id]) > 20:
            self.conversation_history[user_id] = self.conversation_history[user_id][-20:]
    
    def _get_fallback_response(self, language: str) -> Dict[str, Any]:
        """Get a fallback response when OpenAI is unavailable"""
        if language == "hi":
            return {
                "text": "माफ़ करें, अभी मैं आपकी मदद नहीं कर पा रहा हूं। कृपया कुछ देर बाद फिर से कोशिश करें।",
                "voice_ready": ["माफ़ करें, अभी मैं आपकी मदद नहीं कर पा रहा हूं।", "कृपया कुछ देर बाद फिर से कोशिश करें।"],
                "language": language,
                "intent": "error",
                "confidence": 0.0,
                "suggestions": []
            }
        else:
            return {
                "text": "Sorry, I'm unable to help you right now. Please try again later.",
                "voice_ready": ["Sorry, I'm unable to help you right now.", "Please try again later."],
                "language": language,
                "intent": "error",
                "confidence": 0.0,
                "suggestions": []
            }

# Global instance
openai_service = OpenAIService()
