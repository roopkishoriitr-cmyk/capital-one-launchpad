import asyncio
import json
from typing import Dict, List, Any, Optional
from loguru import logger
from app.core.config import settings
from app.agents.finance_agent import FinanceAgent
from app.agents.agronomy_agent import AgronomyAgent
from app.agents.market_agent import MarketAgent
from app.agents.policy_agent import PolicyAgent
from app.agents.risk_agent import RiskAgent
from app.core.voice_processor import VoiceProcessor
from app.core.openai_service import openai_service
# from app.core.language_detector import LanguageDetector

class AgentOrchestrator:
    """
    Main orchestrator that coordinates all specialized AI agents
    for comprehensive farmer advisory services.
    """
    
    def __init__(self):
        self.finance_agent = FinanceAgent()
        self.agronomy_agent = AgronomyAgent()
        self.market_agent = MarketAgent()
        self.policy_agent = PolicyAgent()
        self.risk_agent = RiskAgent()
        self.voice_processor = VoiceProcessor()
        # self.language_detector = LanguageDetector()
        
        # Agent registry for easy access
        self.agents = {
            "finance": self.finance_agent,
            "agronomy": self.agronomy_agent,
            "market": self.market_agent,
            "policy": self.policy_agent,
            "risk": self.risk_agent
        }
        
        logger.info("🤖 Agent Orchestrator initialized")
    
    async def initialize(self):
        """Initialize all agents and load necessary data"""
        try:
            await asyncio.gather(
                self.finance_agent.initialize(),
                self.agronomy_agent.initialize(),
                self.market_agent.initialize(),
                self.policy_agent.initialize(),
                self.risk_agent.initialize()
            )
            logger.info("✅ All agents initialized successfully")
        except Exception as e:
            logger.error(f"❌ Error initializing agents: {e}")
            raise
    
    async def process_query(self, query: str, user_id: str, language: str = "hi") -> Dict[str, Any]:
        """
        Process a farmer's query through specialized agents for comprehensive advice
        with voice-first approach and return a structured response.
        """
        try:
            # Get user context
            user_context = await self._get_user_context(user_id)
            
            # Analyze intent to determine which agents to involve
            intent_analysis = await self._analyze_intent(query, language)
            
            # Check if this is a comprehensive query that needs multiple agents
            if self._is_comprehensive_query(query):
                # Use specialized agents for detailed analysis
                agent_responses = await self._process_with_agents(query, intent_analysis, user_context, language)
                synthesized_response = await self._synthesize_response(agent_responses, language)
                
                # Create structured response
                response = {
                    "text": synthesized_response,
                    "intent": intent_analysis["primary_intent"],
                    "confidence": intent_analysis["confidence"],
                    "agents_used": intent_analysis["involved_agents"],
                    "voice_ready": [synthesized_response],
                    "suggestions": self._generate_suggestions(intent_analysis["involved_agents"], language),
                    "metadata": {
                        "user_context": user_context,
                        "agent_responses": agent_responses
                    }
                }
            else:
                # Use OpenAI for simple queries
                response = await openai_service.get_krishi_mitra_response(query, user_id, language)
            
            # Log conversation
            await self._log_conversation(user_id, query, response["text"], language, response["intent"])
            
            return response
            
        except Exception as e:
            logger.error(f"❌ Error processing query: {e}")
            return self._get_error_response(language)
    
    async def _analyze_intent(self, query: str, language: str) -> Dict[str, Any]:
        """Analyze the intent of the query to determine which agents to involve"""
        intent_keywords = {
            "finance": ["loan", "debt", "payment", "money", "credit", "karz", "udhar", "qarz"],
            "agronomy": ["crop", "seed", "fertilizer", "pest", "soil", "fasal", "beej", "khad"],
            "market": ["price", "mandi", "sell", "buy", "rate", "bhav", "bikri"],
            "policy": ["subsidy", "scheme", "government", "yojana", "sarkar"],
            "risk": ["weather", "rain", "drought", "flood", "mausam", "baarish"]
        }
        
        query_lower = query.lower()
        involved_agents = []
        
        for agent, keywords in intent_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                involved_agents.append(agent)
        
        # If no specific intent detected, involve all agents for comprehensive advice
        if not involved_agents:
            involved_agents = ["finance", "agronomy", "market"]
        
        return {
            "involved_agents": involved_agents,
            "confidence": 0.8,
            "primary_intent": involved_agents[0] if involved_agents else "general"
        }
    
    async def _get_user_context(self, user_id: str) -> Dict[str, Any]:
        """Get user's current context including loans, crops, location, etc."""
        # This would typically fetch from database
        # For now, return mock data
        return {
            "user_id": user_id,
            "location": "Punjab",
            "current_loans": [
                {"amount": 50000, "interest_rate": 7.5, "remaining": 35000}
            ],
            "current_crops": [
                {"name": "wheat", "area": 5.0, "stage": "growing"}
            ],
            "soil_health": {"ph": 7.2, "nitrogen": "medium"},
            "language": "hi"
        }
    
    async def _process_with_agents(self, query: str, intent_analysis: Dict, 
                                 user_context: Dict, language: str) -> Dict[str, str]:
        """Process query with relevant agents"""
        responses = {}
        
        for agent_name in intent_analysis["involved_agents"]:
            if agent_name in self.agents:
                try:
                    agent_response = await self.agents[agent_name].process(
                        query, user_context, language
                    )
                    responses[agent_name] = agent_response
                except Exception as e:
                    logger.error(f"❌ Error with {agent_name} agent: {e}")
                    responses[agent_name] = f"Sorry, {agent_name} agent is temporarily unavailable."
        
        return responses
    
    async def _synthesize_response(self, responses: Dict[str, str], language: str) -> str:
        """Synthesize responses from multiple agents into a coherent response"""
        if not responses:
            return self._get_default_response(language)
        
        if len(responses) == 1:
            return list(responses.values())[0]
        
        # For multiple agents, create a comprehensive response
        synthesis_prompt = f"""
        Combine the following agent responses into a coherent, helpful response in {language}:
        
        {json.dumps(responses, indent=2)}
        
        Make sure the response is:
        1. Culturally appropriate for Indian farmers
        2. Clear and actionable
        3. Prioritizes the most important information first
        4. Uses simple, understandable language
        """
        
        # For now, return a simple combination
        # In production, this would use an LLM to synthesize
        combined_response = "🌾 आपके सवाल के लिए मेरी सलाह:\n\n"
        
        for agent, response in responses.items():
            agent_names = {
                "finance": "💰 वित्तीय सलाह",
                "agronomy": "🌱 कृषि सलाह", 
                "market": "📊 बाजार की जानकारी",
                "policy": "🏛️ सरकारी योजनाएं",
                "risk": "⚠️ जोखिम चेतावनी"
            }
            combined_response += f"{agent_names.get(agent, agent)}:\n{response}\n\n"
        
        return combined_response
    
    async def _log_conversation(self, user_id: str, query: str, response: str, 
                              language: str, intent: str):
        """Log the conversation for analytics and improvement"""
        # This would typically save to database
        logger.info(f"💬 Conversation logged - User: {user_id}, Language: {language}, Intent: {intent}")
    
    def _get_error_response(self, language: str) -> Dict[str, Any]:
        """Get error response in appropriate language"""
        error_responses = {
            "hi": {
                "text": "माफ़ करें, अभी कुछ तकनीकी समस्या है। कृपया कुछ देर बाद फिर से कोशिश करें।",
                "voice_ready": ["माफ़ करें, अभी कुछ तकनीकी समस्या है।", "कृपया कुछ देर बाद फिर से कोशिश करें।"],
                "language": language,
                "intent": "error",
                "confidence": 0.0,
                "suggestions": []
            },
            "en": {
                "text": "Sorry, there's a technical issue right now. Please try again later.",
                "voice_ready": ["Sorry, there's a technical issue right now.", "Please try again later."],
                "language": language,
                "intent": "error",
                "confidence": 0.0,
                "suggestions": []
            }
        }
        return error_responses.get(language, error_responses["en"])
    
    def _get_default_response(self, language: str) -> str:
        """Get default response when no specific advice is available"""
        default_responses = {
            "hi": "नमस्कार! मैं आपकी कृषि और वित्तीय सलाह के लिए यहाँ हूँ। कृपया अपना सवाल पूछें।",
            "en": "Hello! I'm here to help with your agriculture and financial advice. Please ask your question.",
            "bn": "নমস্কার! আমি আপনার কৃষি এবং আর্থিক পরামর্শের জন্য এখানে আছি। অনুগ্রহ করে আপনার প্রশ্ন জিজ্ঞাসা করুন।",
            "ta": "வணக்கம்! நான் உங்கள் விவசாயம் மற்றும் நிதி ஆலோசனைக்காக இங்கே இருக்கிறேன். தயவுசெய்து உங்கள் கேள்வியைக் கேள்வி."
        }
        return default_responses.get(language, default_responses["en"])
    
    async def get_debt_forecast(self, user_id: str) -> Dict[str, Any]:
        """Get personalized debt freedom forecast for a user"""
        return await self.finance_agent.get_debt_forecast(user_id)
    
    async def get_crop_recommendations(self, user_id: str, season: str) -> Dict[str, Any]:
        """Get crop recommendations based on user's context and season"""
        return await self.agronomy_agent.get_crop_recommendations(user_id, season)
    
    async def get_market_insights(self, crop_name: str, location: str) -> Dict[str, Any]:
        """Get market insights for a specific crop and location"""
        return await self.market_agent.get_market_insights(crop_name, location)

    def _is_comprehensive_query(self, query: str) -> bool:
        """Check if query requires multiple agent analysis"""
        comprehensive_keywords = [
            "loan", "crop", "revenue", "repay", "agronomy", "market", "policy", "risk",
            "karz", "fasal", "kamai", "kisht", "kheti", "mandi", "yojana", "khatra"
        ]
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in comprehensive_keywords)
    
    def _generate_suggestions(self, agents_used: List[str], language: str) -> List[str]:
        """Generate follow-up suggestions based on agents used"""
        suggestions = []
        
        if "finance" in agents_used:
            suggestions.append("अपने कर्ज का विस्तृत विश्लेषण देखें" if language == "hi" else "View detailed loan analysis")
        if "agronomy" in agents_used:
            suggestions.append("फसल की देखभाल के टिप्स जानें" if language == "hi" else "Get crop care tips")
        if "market" in agents_used:
            suggestions.append("मंडी के भाव और बिक्री की सलाह लें" if language == "hi" else "Get market prices and selling advice")
        if "policy" in agents_used:
            suggestions.append("सरकारी योजनाओं की जानकारी लें" if language == "hi" else "Get government scheme information")
        if "risk" in agents_used:
            suggestions.append("जोखिम प्रबंधन की रणनीतियां जानें" if language == "hi" else "Learn risk management strategies")
        
        return suggestions

# Create a global instance
logger.info("🤖 Creating global AgentOrchestrator instance...")
agent_orchestrator = AgentOrchestrator()
logger.info("✅ Global AgentOrchestrator instance created successfully")
