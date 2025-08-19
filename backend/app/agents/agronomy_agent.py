import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from loguru import logger
from app.core.config import settings

class AgronomyAgent:
    """
    Agronomy Agent - Handles crop recommendations, soil health analysis,
    and farming best practices for Indian farmers.
    """
    
    def __init__(self):
        self.name = "Agronomy Agent"
        self.description = "Specialized in crop science, soil health, and farming techniques"
        self.initialized = False
        
    async def initialize(self):
        """Initialize the agronomy agent with crop and soil data"""
        try:
            await self._load_agronomy_data()
            self.initialized = True
            logger.info("🌱 Agronomy Agent initialized successfully")
        except Exception as e:
            logger.error(f"❌ Error initializing Agronomy Agent: {e}")
            raise
    
    async def _load_agronomy_data(self):
        """Load crop, soil, and farming data"""
        # Comprehensive crop data for Punjab
        self.crops = {
            "wheat": {
                "season": "rabi",
                "duration": 120,
                "water_requirement": "medium",
                "soil_type": "loamy",
                "ph_range": (6.0, 7.5),
                "yield_per_acre": 20,  # quintals
                "market_price": 2100,  # per quintal
                "input_cost": 15000,  # per acre
                "profit_margin": 0.4,
                "sowing_time": "November-December",
                "harvest_time": "March-April",
                "best_varieties": ["PBW-343", "HD-2967", "WH-1105"],
                "fertilizer_requirement": {"N": 120, "P": 60, "K": 40},  # kg/acre
                "pest_management": ["Aphids", "Termites", "Rust"],
                "disease_resistance": "Moderate",
                "climate_suitability": "Cool and dry"
            },
            "rice": {
                "season": "kharif",
                "duration": 150,
                "water_requirement": "high",
                "soil_type": "clay",
                "ph_range": (5.5, 6.5),
                "yield_per_acre": 25,
                "market_price": 1800,
                "input_cost": 18000,
                "profit_margin": 0.35,
                "sowing_time": "June-July",
                "harvest_time": "October-November",
                "best_varieties": ["PR-114", "PR-116", "PR-118"],
                "fertilizer_requirement": {"N": 150, "P": 75, "K": 50},
                "pest_management": ["Stem borer", "Leaf folder", "Bacterial blight"],
                "disease_resistance": "High",
                "climate_suitability": "Warm and humid"
            },
            "maize": {
                "season": "kharif",
                "duration": 100,
                "water_requirement": "medium",
                "soil_type": "loamy",
                "ph_range": (6.0, 7.0),
                "yield_per_acre": 30,
                "market_price": 1600,
                "input_cost": 12000,
                "profit_margin": 0.5,
                "sowing_time": "June-July",
                "harvest_time": "September-October",
                "best_varieties": ["PMH-1", "PMH-2", "PMH-3"],
                "fertilizer_requirement": {"N": 100, "P": 50, "K": 30},
                "pest_management": ["Fall armyworm", "Stem borer", "Ear rot"],
                "disease_resistance": "Moderate",
                "climate_suitability": "Warm and moderate rainfall"
            },
            "cotton": {
                "season": "kharif",
                "duration": 180,
                "water_requirement": "medium",
                "soil_type": "sandy_loam",
                "ph_range": (6.5, 8.0),
                "yield_per_acre": 8,  # quintals
                "market_price": 6500,
                "input_cost": 25000,
                "profit_margin": 0.45,
                "sowing_time": "April-May",
                "harvest_time": "October-December",
                "best_varieties": ["F-1861", "RCH-134", "F-2228"],
                "fertilizer_requirement": {"N": 80, "P": 40, "K": 25},
                "pest_management": ["Bollworm", "Whitefly", "Jassids"],
                "disease_resistance": "Low",
                "climate_suitability": "Hot and dry"
            },
            "sugarcane": {
                "season": "year_round",
                "duration": 365,
                "water_requirement": "high",
                "soil_type": "clay_loam",
                "ph_range": (6.0, 7.5),
                "yield_per_acre": 350,  # quintals
                "market_price": 315,  # per quintal
                "input_cost": 45000,
                "profit_margin": 0.3,
                "sowing_time": "February-March",
                "harvest_time": "November-March",
                "best_varieties": ["Co-0238", "Co-0118", "Co-0239"],
                "fertilizer_requirement": {"N": 200, "P": 100, "K": 60},
                "pest_management": ["Top borer", "Stem borer", "Scale insects"],
                "disease_resistance": "High",
                "climate_suitability": "Tropical and subtropical"
            },
            "potato": {
                "season": "rabi",
                "duration": 90,
                "water_requirement": "medium",
                "soil_type": "sandy_loam",
                "ph_range": (5.5, 6.5),
                "yield_per_acre": 120,  # quintals
                "market_price": 800,
                "input_cost": 35000,
                "profit_margin": 0.55,
                "sowing_time": "October-November",
                "harvest_time": "January-February",
                "best_varieties": ["Kufri Pukhraj", "Kufri Jyoti", "Kufri Bahar"],
                "fertilizer_requirement": {"N": 150, "P": 75, "K": 50},
                "pest_management": ["Aphids", "Cutworms", "Late blight"],
                "disease_resistance": "Moderate",
                "climate_suitability": "Cool and moderate"
            }
        }
        
        # Agronomy techniques and best practices
        self.agronomy_techniques = {
            "soil_health": {
                "soil_testing": "Every 2-3 years for nutrient analysis",
                "organic_matter": "Maintain 2-3% organic matter",
                "crop_rotation": "Wheat-Rice-Maize rotation",
                "green_manuring": "Sesbania or Dhaincha between crops",
                "mulching": "Straw mulch for moisture retention"
            },
            "water_management": {
                "drip_irrigation": "40-60% water saving",
                "laser_land_leveling": "Improves water use efficiency by 25%",
                "alternate_wetting_drying": "For rice cultivation",
                "sprinkler_irrigation": "For wheat and maize",
                "water_scheduling": "Based on crop growth stages"
            },
            "nutrient_management": {
                "integrated_nutrient_management": "Combine organic and inorganic",
                "site_specific_nutrient_management": "Based on soil testing",
                "foliar_spray": "Micronutrients during critical stages",
                "bio_fertilizers": "Rhizobium, Azotobacter, PSB",
                "precision_farming": "GPS-guided fertilizer application"
            },
            "pest_management": {
                "integrated_pest_management": "Cultural, biological, chemical",
                "pheromone_traps": "For monitoring pest populations",
                "biological_control": "Trichogramma, neem-based products",
                "resistant_varieties": "Use disease-resistant crop varieties",
                "crop_diversification": "Reduce pest pressure"
            },
            "precision_agriculture": {
                "gps_guidance": "Accurate field operations",
                "variable_rate_technology": "Site-specific input application",
                "remote_sensing": "Crop health monitoring",
                "yield_mapping": "Harvest yield data collection",
                "automated_irrigation": "Sensor-based water management"
            }
        }
        
        # Punjab-specific soil and climate data
        self.punjab_data = {
            "soil_types": {
                "alluvial": "Most common, good for all crops",
                "sandy_loam": "Good for vegetables and pulses",
                "clay_loam": "Ideal for rice and sugarcane",
                "loamy": "Best for wheat and maize"
            },
            "climate_zones": {
                "sub_mountainous": "Hoshiarpur, Ropar - Good for horticulture",
                "central_plains": "Ludhiana, Jalandhar - Wheat-rice belt",
                "south_western": "Bathinda, Mansa - Cotton and oilseeds",
                "malwa_region": "Patiala, Sangrur - Diversified farming"
            },
            "rainfall_pattern": {
                "annual_rainfall": "600-800 mm",
                "monsoon_season": "July-September",
                "winter_rainfall": "December-February",
                "irrigation_dependency": "80% of crops"
            }
        }
    
    async def process(self, query: str, user_context: Dict, language: str = "hi") -> str:
        """Process agronomy-related queries"""
        try:
            # Analyze query type
            query_type = self._analyze_agronomy_query(query)
            
            if query_type == "crop_recommendation":
                return await self._handle_crop_recommendation(user_context, language)
            elif query_type == "soil_health":
                return await self._handle_soil_health(user_context, language)
            elif query_type == "farming_practices":
                return await self._handle_farming_practices(query, user_context, language)
            elif query_type == "pest_management":
                return await self._handle_pest_management(user_context, language)
            else:
                return await self._handle_general_agronomy_query(query, user_context, language)
                
        except Exception as e:
            logger.error(f"❌ Error in Agronomy Agent: {e}")
            return self._get_error_response(language)
    
    def _analyze_agronomy_query(self, query: str) -> str:
        """Analyze the type of agronomy query"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["crop", "fasal", "beej", "plant", "grow"]):
            return "crop_recommendation"
        elif any(word in query_lower for word in ["soil", "mitti", "ph", "fertilizer", "khad"]):
            return "soil_health"
        elif any(word in query_lower for word in ["pest", "disease", "keet", "rogi"]):
            return "pest_management"
        elif any(word in query_lower for word in ["practice", "technique", "method", "tarika"]):
            return "farming_practices"
        else:
            return "general"
    
    async def _handle_crop_recommendation(self, user_context: Dict, language: str) -> str:
        """Handle crop recommendation queries"""
        soil_health = user_context.get("soil_health", {})
        land_area = user_context.get("land_area", 0)
        current_season = self._get_current_season()
        
        # Get suitable crops based on soil and season
        suitable_crops = self._get_suitable_crops(soil_health, current_season)
        
        # Calculate profitability
        profitable_crops = []
        for crop_name in suitable_crops:
            crop_data = self.crops.get(crop_name, {})
            if crop_data:
                profit_per_acre = (crop_data.get("yield_per_acre", 0) * 
                                 crop_data.get("market_price", 0) * 
                                 crop_data.get("profit_margin", 0))
                profitable_crops.append({
                    "name": crop_name,
                    "profit_per_acre": profit_per_acre,
                    "data": crop_data
                })
        
        # Sort by profitability
        profitable_crops.sort(key=lambda x: x["profit_per_acre"], reverse=True)
        
        if language == "hi":
            response = f"""🌱 आपके लिए फसल सिफारिशें ({current_season} मौसम):

📊 मिट्टी: {soil_health.get('type', 'Unknown')}
📏 जमीन: {land_area} एकड़

🏆 सर्वश्रेष्ठ फसलें:"""
            
            for i, crop in enumerate(profitable_crops[:3], 1):
                crop_data = crop["data"]
                response += f"""
{i}. {crop['name'].title()}
   💰 लाभ: ₹{crop['profit_per_acre']:,}/एकड़
   📅 अवधि: {crop_data.get('duration', 0)} दिन
   💧 पानी: {crop_data.get('water_requirement', 'Unknown')}
   🌾 उपज: {crop_data.get('yield_per_acre', 0)} क्विंटल/एकड़"""
            
            response += f"""

💡 सुझाव:
• {profitable_crops[0]['name'].title()} सबसे लाभदायक है
• बाजार के दामों पर नजर रखें
• सरकारी सब्सिडी का लाभ उठाएं"""
            
            return response
        else:
            response = f"""🌱 Crop Recommendations for You ({current_season} season):

📊 Soil: {soil_health.get('type', 'Unknown')}
📏 Land: {land_area} acres

🏆 Best Crops:"""
            
            for i, crop in enumerate(profitable_crops[:3], 1):
                crop_data = crop["data"]
                response += f"""
{i}. {crop['name'].title()}
   💰 Profit: ₹{crop['profit_per_acre']:,}/acre
   📅 Duration: {crop_data.get('duration', 0)} days
   💧 Water: {crop_data.get('water_requirement', 'Unknown')}
   🌾 Yield: {crop_data.get('yield_per_acre', 0)} quintals/acre"""
            
            response += f"""

💡 Tips:
• {profitable_crops[0]['name'].title()} is most profitable
• Monitor market prices
• Avail government subsidies"""
            
            return response
    
    def _get_suitable_crops(self, soil_health: Dict, season: str) -> List[str]:
        """Get suitable crops based on soil and season"""
        soil_type = soil_health.get("type", "loamy")
        season_crops = self.seasons.get(season, {}).get("crops", [])
        
        # Filter crops that are suitable for both soil and season
        suitable_crops = []
        for crop_name in season_crops:
            crop_data = self.crops.get(crop_name, {})
            if crop_data.get("soil_type") == soil_type:
                suitable_crops.append(crop_name)
        
        # If no exact match, return season crops
        return suitable_crops if suitable_crops else season_crops
    
    def _get_current_season(self) -> str:
        """Get current agricultural season"""
        current_month = datetime.now().month
        
        if current_month in [6, 7, 8, 9]:
            return "kharif"
        elif current_month in [10, 11, 12, 1]:
            return "rabi"
        else:
            return "zaid"
    
    async def _handle_soil_health(self, user_context: Dict, language: str) -> str:
        """Handle soil health queries"""
        soil_health = user_context.get("soil_health", {})
        ph_level = soil_health.get("ph", 7.0)
        soil_type = soil_health.get("type", "loamy")
        
        # Analyze soil health
        ph_status = "अच्छा" if 6.0 <= ph_level <= 7.5 else "सुधार की आवश्यकता"
        soil_info = self.punjab_data.get("soil_types", {}).get(soil_type, {})
        
        if language == "hi":
            return f"""🌱 आपकी मिट्टी की जानकारी:

📊 pH स्तर: {ph_level} ({ph_status})
🏗️ मिट्टी का प्रकार: {soil_type}
💧 मिट्टी की विशेषता: {soil_info}

💡 सुधार के सुझाव:
• जैविक खाद का प्रयोग करें
• नियमित मिट्टी परीक्षण करें
• फसल चक्र अपनाएं
• हरी खाद का प्रयोग करें

📞 मिट्टी परीक्षण के लिए कृषि विभाग से संपर्क करें।"""
        else:
            return f"""🌱 Your Soil Information:

📊 pH Level: {ph_level} ({ph_status})
🏗️ Soil Type: {soil_type}
💧 Soil Characteristics: {soil_info}

💡 Improvement Suggestions:
• Use organic fertilizers
• Get regular soil testing
• Follow crop rotation
• Use green manure

📞 Contact agriculture department for soil testing."""
    
    async def _handle_farming_practices(self, query: str, user_context: Dict, language: str) -> str:
        """Handle farming practices queries"""
        current_crops = user_context.get("current_crops", [])
        
        if language == "hi":
            return f"""🌾 कृषि के सर्वोत्तम तरीके:

📅 समय पर बुवाई करें
💧 सिंचाई का ध्यान रखें
🌱 उचित फसल चक्र अपनाएं
🐛 कीट प्रबंधन करें
🌿 खरपतवार नियंत्रण करें

💡 आधुनिक तकनीकें:
• ड्रिप सिंचाई
• जैविक खेती
• प्रेसिजन फार्मिंग
• मल्चिंग

📚 कृषि विभाग से प्रशिक्षण लें।"""
        else:
            return f"""🌾 Best Farming Practices:

📅 Sow at the right time
💧 Manage irrigation properly
🌱 Follow proper crop rotation
🐛 Control pests
🌿 Manage weeds

💡 Modern Techniques:
• Drip irrigation
• Organic farming
• Precision farming
• Mulching

📚 Get training from agriculture department."""
    
    async def _handle_pest_management(self, user_context: Dict, language: str) -> str:
        """Handle pest management queries"""
        current_crops = user_context.get("current_crops", [])
        
        if language == "hi":
            return f"""🐛 कीट प्रबंधन सलाह:

🔍 नियमित निरीक्षण करें
🌿 जैविक कीटनाशक प्रयोग करें
🦅 प्राकृतिक शत्रुओं को बढ़ावा दें
🌱 फसल चक्र अपनाएं
🧪 रासायनिक कीटनाशक कम प्रयोग करें

⚠️ सावधानियां:
• कीटनाशक का सही मात्रा में प्रयोग
• सुरक्षा उपकरण पहनें
• फसल कटाई से पहले अंतराल रखें

📞 कीट समस्या के लिए कृषि विभाग से संपर्क करें।"""
        else:
            return f"""🐛 Pest Management Advice:

🔍 Regular monitoring
🌿 Use organic pesticides
🦅 Promote natural enemies
🌱 Follow crop rotation
🧪 Minimize chemical pesticides

⚠️ Precautions:
• Use pesticides in correct quantity
• Wear safety equipment
• Maintain gap before harvest

📞 Contact agriculture department for pest problems."""
    
    async def _handle_general_agronomy_query(self, query: str, user_context: Dict, language: str) -> str:
        """Handle general agronomy queries"""
        if language == "hi":
            return """🌱 कृषि सलाह:

• मिट्टी की जांच नियमित करें
• उचित फसल चुनें
• सिंचाई का ध्यान रखें
• कीट प्रबंधन करें
• बाजार के दामों पर नजर रखें

क्या आप फसल, मिट्टी या कीट प्रबंधन के बारे में जानना चाहते हैं?"""
        else:
            return """🌱 Agricultural Advice:

• Get regular soil testing
• Choose appropriate crops
• Manage irrigation properly
• Control pests
• Monitor market prices

Do you want to know about crops, soil, or pest management?"""
    
    def _get_error_response(self, language: str) -> str:
        """Error response in appropriate language"""
        if language == "hi":
            return "माफ़ करें, कृषि सलाह देने में समस्या आ रही है। कृपया कुछ देर बाद फिर से कोशिश करें।"
        else:
            return "Sorry, there's an issue providing agricultural advice. Please try again later."
    
    async def get_crop_recommendations(self, user_id: str, season: str) -> Dict[str, Any]:
        """Get detailed crop recommendations for a user"""
        # Mock user context - in production would fetch from database
        user_context = {
            "user_id": user_id,
            "soil_health": {"ph": 7.2, "type": "loamy"},
            "land_area": 5.0,
            "location": "Punjab"
        }
        
        suitable_crops = self._get_suitable_crops(user_context["soil_health"], season)
        recommendations = []
        
        for crop_name in suitable_crops[:3]:
            crop_data = self.crops.get(crop_name, {})
            if crop_data:
                recommendations.append({
                    "crop": crop_name,
                    "profit_per_acre": crop_data.get("yield_per_acre", 0) * 
                                     crop_data.get("market_price", 0) * 
                                     crop_data.get("profit_margin", 0),
                    "duration": crop_data.get("duration", 0),
                    "water_requirement": crop_data.get("water_requirement", "Unknown")
                })
        
        return {
            "user_id": user_id,
            "season": season,
            "recommendations": recommendations,
            "soil_health": user_context["soil_health"]
        }
