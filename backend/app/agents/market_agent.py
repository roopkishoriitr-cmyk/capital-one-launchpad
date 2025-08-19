import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from loguru import logger
from app.core.config import settings

class MarketAgent:
    """
    Market Agent - Handles market prices, demand forecasting, and optimal selling strategies
    for Indian farmers.
    """
    
    def __init__(self):
        self.name = "Market Agent"
        self.description = "Specialized in market intelligence, price forecasting, and selling strategies"
        self.initialized = False
        
    async def initialize(self):
        """Initialize the market agent with price and demand data"""
        try:
            await self._load_market_data()
            self.initialized = True
            logger.info("📊 Market Agent initialized successfully")
        except Exception as e:
            logger.error(f"❌ Error initializing Market Agent: {e}")
            raise
    
    async def _load_market_data(self):
        """Load market data including prices, demand trends, etc."""
        # Current market prices for Punjab mandis
        self.current_prices = {
            "wheat": {
                "bathinda": 2150,
                "ludhiana": 2180,
                "amritsar": 2160,
                "jalandhar": 2170,
                "patiala": 2140,
                "trend": "stable",
                "last_updated": "2024-08-18"
            },
            "rice": {
                "bathinda": 1850,
                "ludhiana": 1880,
                "amritsar": 1860,
                "jalandhar": 1870,
                "patiala": 1840,
                "trend": "increasing",
                "last_updated": "2024-08-18"
            },
            "maize": {
                "bathinda": 1650,
                "ludhiana": 1680,
                "amritsar": 1660,
                "jalandhar": 1670,
                "patiala": 1640,
                "trend": "stable",
                "last_updated": "2024-08-18"
            },
            "cotton": {
                "bathinda": 6700,
                "ludhiana": 6750,
                "amritsar": 6720,
                "jalandhar": 6730,
                "patiala": 6680,
                "trend": "decreasing",
                "last_updated": "2024-08-18"
            },
            "sugarcane": {
                "bathinda": 320,
                "ludhiana": 325,
                "amritsar": 322,
                "jalandhar": 323,
                "patiala": 318,
                "trend": "stable",
                "last_updated": "2024-08-18"
            },
            "potato": {
                "bathinda": 850,
                "ludhiana": 880,
                "amritsar": 860,
                "jalandhar": 870,
                "patiala": 840,
                "trend": "increasing",
                "last_updated": "2024-08-18"
            }
        }
        
        # Demand forecasting for next 6 months
        self.demand_forecast = {
            "wheat": {
                "current_demand": "high",
                "next_3_months": "stable",
                "next_6_months": "increasing",
                "reason": "Festival season and export demand",
                "recommended_action": "Hold stocks for better prices"
            },
            "rice": {
                "current_demand": "very_high",
                "next_3_months": "increasing",
                "next_6_months": "stable",
                "reason": "Export opportunities and domestic consumption",
                "recommended_action": "Sell in next 2 months"
            },
            "maize": {
                "current_demand": "medium",
                "next_3_months": "increasing",
                "next_6_months": "high",
                "reason": "Poultry feed industry demand",
                "recommended_action": "Store for better prices"
            },
            "cotton": {
                "current_demand": "low",
                "next_3_months": "stable",
                "next_6_months": "increasing",
                "reason": "Textile industry recovery expected",
                "recommended_action": "Wait for price improvement"
            },
            "sugarcane": {
                "current_demand": "high",
                "next_3_months": "stable",
                "next_6_months": "stable",
                "reason": "Sugar mills demand",
                "recommended_action": "Sell to nearby mills"
            },
            "potato": {
                "current_demand": "very_high",
                "next_3_months": "decreasing",
                "next_6_months": "low",
                "reason": "Seasonal demand pattern",
                "recommended_action": "Sell immediately"
            }
        }
        
        # Punjab mandi information
        self.mandi_info = {
            "bathinda": {
                "name": "Bathinda Grain Market",
                "location": "Bathinda, Punjab",
                "contact": "0164-2223456",
                "specialization": "Wheat, Rice, Cotton",
                "storage_capacity": "50000 MT",
                "transport_links": "Rail and Road",
                "processing_units": 15
            },
            "ludhiana": {
                "name": "Ludhiana Grain Market",
                "location": "Ludhiana, Punjab",
                "contact": "0161-2223456",
                "specialization": "Wheat, Rice, Maize",
                "storage_capacity": "75000 MT",
                "transport_links": "Rail, Road, Air",
                "processing_units": 25
            },
            "amritsar": {
                "name": "Amritsar Grain Market",
                "location": "Amritsar, Punjab",
                "contact": "0183-2223456",
                "specialization": "Wheat, Rice, Potato",
                "storage_capacity": "40000 MT",
                "transport_links": "Rail and Road",
                "processing_units": 12
            },
            "jalandhar": {
                "name": "Jalandhar Grain Market",
                "location": "Jalandhar, Punjab",
                "contact": "0181-2223456",
                "specialization": "Wheat, Rice, Sugarcane",
                "storage_capacity": "35000 MT",
                "transport_links": "Rail and Road",
                "processing_units": 10
            },
            "patiala": {
                "name": "Patiala Grain Market",
                "location": "Patiala, Punjab",
                "contact": "0175-2223456",
                "specialization": "Wheat, Rice, Vegetables",
                "storage_capacity": "30000 MT",
                "transport_links": "Rail and Road",
                "processing_units": 8
            }
        }
        
        # Market trends and analysis
        self.market_trends = {
            "seasonal_patterns": {
                "wheat": "Peak prices in March-April, Low in September-October",
                "rice": "Peak prices in November-December, Low in June-July",
                "maize": "Peak prices in January-February, Low in August-September",
                "cotton": "Peak prices in December-January, Low in May-June",
                "sugarcane": "Stable prices throughout year",
                "potato": "Peak prices in December-January, Low in March-April"
            },
            "export_opportunities": {
                "wheat": "Middle East, Africa - High demand",
                "rice": "Gulf countries, Europe - Premium prices",
                "maize": "Southeast Asia - Growing demand",
                "cotton": "Bangladesh, Vietnam - Textile industry",
                "sugarcane": "Limited export opportunities",
                "potato": "Nepal, Bangladesh - Seasonal demand"
            },
            "price_factors": {
                "weather": "Drought/flood affects supply and prices",
                "government_policy": "MSP, export restrictions impact prices",
                "global_markets": "International prices influence local rates",
                "demand_supply": "Festival seasons, industrial demand",
                "transport_cost": "Fuel prices affect mandi prices",
                "storage_availability": "Warehouse capacity affects prices"
            }
        }
        
        # Selling strategies and recommendations
        self.selling_strategies = {
            "immediate_sale": {
                "crops": ["potato", "vegetables"],
                "reason": "Perishable nature",
                "mandi_recommendation": "Nearest mandi for freshness"
            },
            "staggered_sale": {
                "crops": ["wheat", "rice"],
                "reason": "Stable prices, storage possible",
                "mandi_recommendation": "Multiple mandis for better prices"
            },
            "contract_farming": {
                "crops": ["cotton", "sugarcane"],
                "reason": "Assured prices, market security",
                "mandi_recommendation": "Direct to processing units"
            },
            "value_addition": {
                "crops": ["maize", "pulses"],
                "reason": "Higher profit margins",
                "mandi_recommendation": "Process before selling"
            }
        }
    
    async def process(self, query: str, user_context: Dict, language: str = "hi") -> str:
        """Process market-related queries"""
        try:
            # Analyze query type
            query_type = self._analyze_market_query(query)
            
            if query_type == "price_inquiry":
                return await self._handle_price_inquiry(user_context, language)
            elif query_type == "selling_strategy":
                return await self._handle_selling_strategy(user_context, language)
            elif query_type == "mandi_info":
                return await self._handle_mandi_info(user_context, language)
            elif query_type == "demand_forecast":
                return await self._handle_demand_forecast(user_context, language)
            else:
                return await self._handle_general_market_query(query, user_context, language)
                
        except Exception as e:
            logger.error(f"❌ Error in Market Agent: {e}")
            return self._get_error_response(language)
    
    def _analyze_market_query(self, query: str) -> str:
        """Analyze the type of market query"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["price", "rate", "bhav", "dum", "cost"]):
            return "price_inquiry"
        elif any(word in query_lower for word in ["sell", "bikri", "mandi", "market"]):
            return "selling_strategy"
        elif any(word in query_lower for word in ["mandi", "market", "haat"]):
            return "mandi_info"
        elif any(word in query_lower for word in ["demand", "trend", "future", "forecast"]):
            return "demand_forecast"
        else:
            return "general"
    
    async def _handle_price_inquiry(self, user_context: Dict, language: str) -> str:
        """Handle price inquiry queries"""
        current_crops = user_context.get("current_crops", [])
        
        if not current_crops:
            return self._get_no_crops_response(language)
        
        price_info = []
        for crop in current_crops:
            crop_name = crop.get("name", "")
            if crop_name in self.current_prices:
                price_data = self.current_prices[crop_name]
                price_info.append({
                    "crop": crop_name,
                    "data": price_data
                })
        
        if language == "hi":
            response = "📊 आपकी फसलों के बाजार भाव:\n\n"
            
            for info in price_info:
                crop_name = info["crop"]
                data = info["data"]
                response += f"""🌾 {crop_name.title()}:
💰 वर्तमान भाव: ₹{data['bathinda']:,}/क्विंटल
📈 सर्वोच्च भाव: ₹{data['ludhiana']:,}/क्विंटल
📉 न्यूनतम भाव: ₹{data['amritsar']:,}/क्विंटल
📊 रुझान: {self._get_trend_text(data['trend'], 'hi')}
🏪 सर्वोत्तम मंडी: {data['ludhiana']}
⏰ सर्वोत्तम समय: {data['last_updated']}

"""
            
            response += "💡 सुझाव:\n"
            response += "• बाजार के रुझान पर नजर रखें\n"
            response += "• सर्वोत्तम समय पर बेचें\n"
            response += "• कई मंडियों के भाव तुलना करें"
            
            return response
        else:
            response = "📊 Market Prices for Your Crops:\n\n"
            
            for info in price_info:
                crop_name = info["crop"]
                data = info["data"]
                response += f"""🌾 {crop_name.title()}:
💰 Current Price: ₹{data['bathinda']:,}/quintal
📈 Highest Price: ₹{data['ludhiana']:,}/quintal
📉 Lowest Price: ₹{data['amritsar']:,}/quintal
📊 Trend: {self._get_trend_text(data['trend'], 'en')}
🏪 Best Mandi: {data['ludhiana']}
⏰ Best Time: {data['last_updated']}

"""
            
            response += "💡 Tips:\n"
            response += "• Monitor market trends\n"
            response += "• Sell at optimal time\n"
            response += "• Compare prices across mandis"
            
            return response
    
    def _get_trend_text(self, trend: str, language: str) -> str:
        """Get trend text in appropriate language"""
        if language == "hi":
            trend_map = {
                "rising": "बढ़ रहा है",
                "falling": "गिर रहा है",
                "stable": "स्थिर है"
            }
        else:
            trend_map = {
                "rising": "Rising",
                "falling": "Falling",
                "stable": "Stable"
            }
        
        return trend_map.get(trend, trend)
    
    async def _handle_selling_strategy(self, user_context: Dict, language: str) -> str:
        """Handle selling strategy queries"""
        current_crops = user_context.get("current_crops", [])
        location = user_context.get("location", "Punjab")
        
        if not current_crops:
            return self._get_no_crops_response(language)
        
        strategies = []
        for crop in current_crops:
            crop_name = crop.get("name", "")
            if crop_name in self.current_prices:
                price_data = self.current_prices[crop_name]
                mandi_data = self.mandi_info.get(price_data["ludhiana"], {}) # Assuming ludhiana is the best mandi for selling strategy
                
                # Calculate net profit after transport and commission
                transport_cost = mandi_data.get("transport_links", "Rail and Road").count("Rail") * 100 + mandi_data.get("transport_links", "Rail and Road").count("Road") * 50
                commission = mandi_data.get("processing_units", 0) * 0.5 # Simplified commission
                net_price = price_data["bathinda"] * (1 - commission/100) - transport_cost
                
                strategies.append({
                    "crop": crop_name,
                    "mandi": mandi_data["name"],
                    "net_price": net_price,
                    "timing": price_data["last_updated"]
                })
        
        if language == "hi":
            response = "💡 आपकी फसल बिक्री रणनीति:\n\n"
            
            for strategy in strategies:
                response += f"""🌾 {strategy['crop'].title()}:
🏪 सर्वोत्तम मंडी: {strategy['mandi']}
💰 शुद्ध भाव: ₹{strategy['net_price']:,}/क्विंटल
⏰ सर्वोत्तम समय: {strategy['timing']}

"""
            
            response += "📋 बिक्री के लिए सुझाव:\n"
            response += "• फसल की गुणवत्ता बनाए रखें\n"
            response += "• सही पैकिंग करें\n"
            response += "• परिवहन की व्यवस्था पहले करें\n"
            response += "• बैंक गारंटी लें"
            
            return response
        else:
            response = "💡 Selling Strategy for Your Crops:\n\n"
            
            for strategy in strategies:
                response += f"""🌾 {strategy['crop'].title()}:
🏪 Best Mandi: {strategy['mandi']}
💰 Net Price: ₹{strategy['net_price']:,}/quintal
⏰ Best Time: {strategy['timing']}

"""
            
            response += "📋 Selling Tips:\n"
            response += "• Maintain crop quality\n"
            response += "• Proper packaging\n"
            response += "• Arrange transport in advance\n"
            response += "• Get bank guarantee"
            
            return response
    
    async def _handle_mandi_info(self, user_context: Dict, language: str) -> str:
        """Handle mandi information queries"""
        location = user_context.get("location", "Punjab")
        
        # Get nearby mandis
        nearby_mandis = []
        for mandi_name, mandi_data in self.mandi_info.items():
            if mandi_data["location"].startswith(location):
                nearby_mandis.append({
                    "name": mandi_data["name"],
                    "data": mandi_data
                })
        
        if language == "hi":
            response = f"🏪 {location} के निकटवर्ती मंडी:\n\n"
            
            for mandi in nearby_mandis:
                data = mandi["data"]
                response += f"""🏪 {mandi['name']}:
🌾 विशेषज्ञता: {data['specialization']}
🚚 परिवहन लागत: ₹{data['transport_links'].count('Rail') * 100 + data['transport_links'].count('Road') * 50:,}
💼 कमीशन: {data['processing_units'] * 0.5}%

"""
            
            response += "📞 मंडी से संपर्क करने के लिए:\n"
            response += "• कृषि विभाग कार्यालय\n"
            response += "• मंडी समिति\n"
            response += "• ऑनलाइन पोर्टल"
            
            return response
        else:
            response = f"🏪 Nearby Mandis in {location}:\n\n"
            
            for mandi in nearby_mandis:
                data = mandi["data"]
                response += f"""🏪 {mandi['name']}:
🌾 Specialization: {data['specialization']}
🚚 Transport Cost: ₹{data['transport_links'].count('Rail') * 100 + data['transport_links'].count('Road') * 50:,}
💼 Commission: {data['processing_units'] * 0.5}%

"""
            
            response += "📞 To Contact Mandi:\n"
            response += "• Agriculture Department Office\n"
            response += "• Mandi Committee\n"
            response += "• Online Portal"
            
            return response
    
    async def _handle_demand_forecast(self, user_context: Dict, language: str) -> str:
        """Handle demand forecasting queries"""
        current_crops = user_context.get("current_crops", [])
        
        if not current_crops:
            return self._get_no_crops_response(language)
        
        forecasts = []
        for crop in current_crops:
            crop_name = crop.get("name", "")
            if crop_name in self.demand_forecast:
                forecast_data = self.demand_forecast[crop_name]
                forecasts.append({
                    "crop": crop_name,
                    "trend": forecast_data["next_6_months"],
                    "reason": forecast_data["reason"]
                })
        
        if language == "hi":
            response = "🔮 आपकी फसलों की मांग पूर्वानुमान:\n\n"
            
            for forecast in forecasts:
                response += f"""🌾 {forecast['crop'].title()}:
📊 रुझान: {self._get_trend_text(forecast['trend'], 'hi')}
📝 कारण: {forecast['reason']}

"""
            
            response += "💡 सुझाव:\n"
            response += "• बढ़ती मांग वाली फसलें उगाएं\n"
            response += "• बाजार के रुझान पर नजर रखें\n"
            response += "• भविष्य की योजना बनाएं"
            
            return response
        else:
            response = "🔮 Demand Forecast for Your Crops:\n\n"
            
            for forecast in forecasts:
                response += f"""🌾 {forecast['crop'].title()}:
📊 Trend: {self._get_trend_text(forecast['trend'], 'en')}
📝 Reason: {forecast['reason']}

"""
            
            response += "💡 Tips:\n"
            response += "• Grow crops with rising demand\n"
            response += "• Monitor market trends\n"
            response += "• Plan for the future"
            
            return response
    
    async def _handle_general_market_query(self, query: str, user_context: Dict, language: str) -> str:
        """Handle general market queries"""
        if language == "hi":
            return """📊 बाजार सलाह:

• नियमित रूप से मंडी भाव जांचें
• सर्वोत्तम समय पर फसल बेचें
• कई मंडियों के भाव तुलना करें
• परिवहन और कमीशन लागत ध्यान रखें
• बाजार के रुझान पर नजर रखें

क्या आप फसल के भाव, बिक्री रणनीति या मंडी की जानकारी चाहते हैं?"""
        else:
            return """📊 Market Advice:

• Check mandi prices regularly
• Sell crops at optimal time
• Compare prices across mandis
• Consider transport and commission costs
• Monitor market trends

Do you want crop prices, selling strategy, or mandi information?"""
    
    def _get_no_crops_response(self, language: str) -> str:
        """Response when user has no current crops"""
        if language == "hi":
            return "🌾 आपकी कोई वर्तमान फसल नहीं है। कृपया पहले फसल की जानकारी दें।"
        else:
            return "🌾 You have no current crops. Please provide crop information first."
    
    def _get_error_response(self, language: str) -> str:
        """Error response in appropriate language"""
        if language == "hi":
            return "माफ़ करें, बाजार की जानकारी देने में समस्या आ रही है। कृपया कुछ देर बाद फिर से कोशिश करें।"
        else:
            return "Sorry, there's an issue providing market information. Please try again later."
    
    async def get_market_insights(self, crop_name: str, location: str) -> Dict[str, Any]:
        """Get detailed market insights for a specific crop and location"""
        price_data = self.current_prices.get(crop_name, {})
        demand_data = self.demand_forecast.get(crop_name, {})
        
        return {
            "crop": crop_name,
            "location": location,
            "current_price": price_data.get("bathinda", 0),
            "price_trend": price_data.get("trend", "stable"),
            "demand_trend": demand_data.get("next_6_months", "stable"),
            "best_mandi": price_data.get("ludhiana", ""),
            "best_time": price_data.get("last_updated", ""),
            "recommendations": [
                f"Monitor {crop_name} prices regularly",
                f"Consider selling at {price_data.get('last_updated', 'optimal time')}",
                f"Check prices at {price_data.get('ludhiana', 'nearby mandis')}"
            ]
        }
