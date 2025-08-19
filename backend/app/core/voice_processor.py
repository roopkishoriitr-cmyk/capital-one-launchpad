import asyncio
import json
import tempfile
import os
from typing import Dict, List, Any, Optional
from openai import AsyncOpenAI
from loguru import logger
from app.core.config import settings

class VoiceProcessor:
    """
    OpenAI Realtime API processor for voice-to-voice interactions
    with Indian farmers using KrishiMitra.
    """
    
    def __init__(self):
        logger.info("🎤 Initializing OpenAI Realtime API Voice Processor...")
        
        # Check API key availability
        if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "your-actual-openai-api-key-here":
            logger.warning("⚠️ OPENAI_API_KEY not set or using placeholder - Voice features will be disabled")
            self.client = None
            self.api_key_available = False
        else:
            self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            self.api_key_available = True
            logger.info(f"✅ OpenAI client initialized with API key: {settings.OPENAI_API_KEY[:10]}...")
        
        self.supported_languages = settings.SUPPORTED_LANGUAGES
        logger.info(f"🌍 Supported languages: {self.supported_languages}")
        
        self.language_names = {
            "hi": "Hindi",
            "bn": "Bengali", 
            "ta": "Tamil",
            "te": "Telugu",
            "mr": "Marathi",
            "gu": "Gujarati",
            "pa": "Punjabi",
            "or": "Odia",
            "ml": "Malayalam",
            "kn": "Kannada"
        }
        
        # OpenAI Realtime API configuration
        self.voice_model = "tts-1"
        self.voice_name = "alloy"  # Can be: alloy, echo, fable, onyx, nova, shimmer
        logger.info(f"🎵 Voice configuration - Model: {self.voice_model}, Default Voice: {self.voice_name}")
        
        logger.info("🎤 OpenAI Realtime API processor initialized successfully")
    
    async def create_realtime_session(self, voice: str = "alloy", language: str = "hi", instructions: str = "") -> Dict[str, Any]:
        """
        Create a real-time voice session using OpenAI Realtime API
        """
        # Check if API key is available
        if not self.api_key_available:
            logger.error("❌ Cannot create realtime session - OpenAI API key not configured")
            raise ValueError("OpenAI API key is required for voice features. Please set OPENAI_API_KEY environment variable.")
        
        session_start_time = asyncio.get_event_loop().time()
        logger.info(f"🔄 Starting realtime session creation...")
        logger.info(f"📝 Session params - Voice: {voice}, Language: {language}, Instructions length: {len(instructions)} chars")
        
        try:
            # Validate inputs
            if not voice:
                logger.warning("⚠️ No voice specified, using default: alloy")
                voice = "alloy"
            
            if not language:
                logger.warning("⚠️ No language specified, using default: hi")
                language = "hi"
            
            if not instructions:
                logger.warning("⚠️ No instructions provided, using default KrishiMitra instructions")
                instructions = "You are KrishiMitra, an AI farming assistant for Indian farmers."
            
            # Prepare request body for OpenAI Realtime API
            body = {
                "model": "gpt-4o-realtime",
                "voice": voice,
                "instructions": instructions
            }
            
            logger.info(f"📦 Request body prepared - Model: {body['model']}, Voice: {body['voice']}")
            logger.debug(f"📋 Instructions preview: {instructions[:100]}...")
            
            # Make request to OpenAI Realtime API using httpx
            import httpx
            logger.info("🌐 Making HTTP request to OpenAI Realtime API...")
            
            async with httpx.AsyncClient() as client:
                logger.info(f"🔗 Connecting to: https://api.openai.com/v1/realtime/sessions")
                logger.info(f"🔑 Using API key: {settings.OPENAI_API_KEY[:10]}...")
                
                response = await client.post(
                    'https://api.openai.com/v1/realtime/sessions',
                    headers={
                        'Authorization': f'Bearer {settings.OPENAI_API_KEY}',
                        'Content-Type': 'application/json'
                    },
                    json=body,
                    timeout=30.0
                )
            
            logger.info(f"📡 OpenAI API response received - Status: {response.status_code}")
            logger.debug(f"📡 Response headers: {dict(response.headers)}")
            
            if response.status_code != 200:
                error_text = response.text
                logger.error(f"❌ OpenAI API error - Status: {response.status_code}")
                logger.error(f"❌ Error response: {error_text}")
                raise Exception(f"OpenAI API error: {error_text}")
            
            session_data = response.json()
            logger.info(f"✅ Session data received - ID: {session_data.get('id', 'unknown')}")
            logger.debug(f"📄 Full session response: {json.dumps(session_data, indent=2)}")
            
            session_duration = asyncio.get_event_loop().time() - session_start_time
            logger.info(f"⏱️ Session creation completed in {session_duration:.2f} seconds")
            
            result = {
                "success": True,
                "session_id": session_data.get('id'),
                "model": session_data.get('model', 'gpt-4o-realtime'),
                "voice": voice,
                "language": language,
                "status": 'active',
                "creation_time": session_duration
            }
            
            logger.info(f"🎉 Realtime session created successfully - ID: {result['session_id']}")
            return result
            
        except Exception as e:
            session_duration = asyncio.get_event_loop().time() - session_start_time
            logger.error(f"❌ Error creating realtime session after {session_duration:.2f} seconds: {e}")
            logger.error(f"❌ Error type: {type(e).__name__}")
            logger.error(f"❌ Error details: {str(e)}")
            
            return {
                "success": False,
                "error": f"Session creation error: {e}",
                "error_type": type(e).__name__,
                "duration": session_duration
            }
    
    async def text_to_speech(self, text: str, language: str = "hi") -> Dict[str, Any]:
        """
        Convert text to speech using OpenAI TTS API (for non-realtime responses)
        """
        tts_start_time = asyncio.get_event_loop().time()
        logger.info(f"🔊 Starting TTS conversion...")
        logger.info(f"📝 TTS params - Text length: {len(text)}, Language: {language}")
        logger.debug(f"📄 Text preview: {text[:100]}...")
        
        try:
            if language not in self.supported_languages:
                logger.warning(f"⚠️ Unsupported language '{language}', defaulting to 'hi'")
                language = "hi"  # Default to Hindi
            
            logger.info(f"🎵 Using TTS model: {self.voice_model}, Voice: {self.voice_name}")
            
            # Use OpenAI TTS for text-to-speech
            logger.info("🌐 Making TTS request to OpenAI...")
            response = await self.client.audio.speech.create(
                model=self.voice_model,
                voice=self.voice_name,
                input=text,
                response_format="mp3"
            )
            
            # Get audio data
            audio_data = response.content
            audio_size = len(audio_data)
            logger.info(f"✅ TTS response received - Audio size: {audio_size} bytes")
            
            # Calculate approximate duration (rough estimate)
            duration = audio_size / 16000  # Approximate duration
            logger.info(f"⏱️ Estimated audio duration: {duration:.2f} seconds")
            
            tts_duration = asyncio.get_event_loop().time() - tts_start_time
            logger.info(f"🎉 TTS conversion completed in {tts_duration:.2f} seconds")
            
            return {
                "success": True,
                "audio_data": audio_data,
                "language": language,
                "text": text,
                "duration": duration,
                "audio_size": audio_size,
                "processing_time": tts_duration
            }
            
        except Exception as e:
            tts_duration = asyncio.get_event_loop().time() - tts_start_time
            logger.error(f"❌ Error in TTS conversion after {tts_duration:.2f} seconds: {e}")
            logger.error(f"❌ Error type: {type(e).__name__}")
            logger.error(f"❌ Error details: {str(e)}")
            
            return {
                "success": False,
                "error": f"TTS error: {e}",
                "language": language,
                "error_type": type(e).__name__,
                "processing_time": tts_duration
            }
    
    def get_supported_languages(self) -> List[Dict[str, str]]:
        """Get list of supported languages"""
        logger.info(f"🌍 Returning {len(self.language_names)} supported languages")
        return [
            {"code": code, "name": name} 
            for code, name in self.language_names.items()
        ]
    
    def get_available_voices(self) -> List[Dict[str, str]]:
        """Get list of available voices"""
        logger.info("🎵 Returning available OpenAI TTS voices")
        return [
            {"id": "alloy", "name": "Alloy", "description": "Neutral, balanced voice"},
            {"id": "echo", "name": "Echo", "description": "Warm, friendly voice"},
            {"id": "fable", "name": "Fable", "description": "Narrative, storytelling voice"},
            {"id": "onyx", "name": "Onyx", "description": "Deep, authoritative voice"},
            {"id": "nova", "name": "Nova", "description": "Bright, energetic voice"},
            {"id": "shimmer", "name": "Shimmer", "description": "Soft, gentle voice"}
        ]
    
    def is_language_supported(self, language: str) -> bool:
        """Check if language is supported"""
        is_supported = language in self.supported_languages
        logger.info(f"🌍 Language '{language}' supported: {is_supported}")
        return is_supported
    
    async def get_voice_preview(self, text: str, language: str = "hi", voice: str = "alloy") -> Dict[str, Any]:
        """Get voice preview for testing"""
        logger.info(f"🎵 Generating voice preview...")
        logger.info(f"📝 Preview params - Text length: {len(text)}, Language: {language}, Voice: {voice}")
        
        try:
            # Use a simple test text if none provided
            test_text = text or "नमस्कार! मैं KrishiMitra हूं। आपकी कैसे मदद कर सकता हूं?"
            logger.info(f"📄 Using test text: {test_text}")
            
            result = await self.text_to_speech(test_text, language)
            
            if result["success"]:
                logger.info(f"✅ Voice preview generated successfully")
                return {
                    "success": True,
                    "preview_text": test_text,
                    "language": language,
                    "voice": voice,
                    "duration": result.get("duration", 0),
                    "audio_size": result.get("audio_size", 0)
                }
            else:
                logger.error(f"❌ Voice preview generation failed: {result.get('error')}")
                return result
                
        except Exception as e:
            logger.error(f"❌ Error in voice preview: {e}")
            return {
                "success": False,
                "error": f"Preview error: {e}",
                "error_type": type(e).__name__
            }
    
    def _get_error_response(self, language: str = "hi") -> str:
        """Get error response in appropriate language"""
        logger.info(f"🚨 Generating error response in language: {language}")
        if language == "hi":
            return "माफ़ करें, अभी कुछ तकनीकी समस्या है। कृपया कुछ देर बाद फिर से कोशिश करें।"
        else:
            return "Sorry, there's a technical issue. Please try again later."

# Create a global instance
logger.info("🎤 Creating global VoiceProcessor instance...")
voice_processor = VoiceProcessor()
logger.info("✅ Global VoiceProcessor instance created successfully")
