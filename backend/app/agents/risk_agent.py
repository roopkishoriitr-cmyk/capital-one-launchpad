import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from loguru import logger
from app.core.config import settings

class RiskAgent:
    """
    Risk Agent - Handles weather alerts, pest outbreaks, and risk management
    for Indian farmers.
    """
    
    def __init__(self):
        self.name = "Risk Agent"
        self.description = "Specialized in weather alerts, pest management, and risk mitigation"
        self.initialized = False
        
    async def initialize(self):
        """Initialize the risk agent with weather and pest data"""
        try:
            await self._load_risk_data()
            self.initialized = True
            logger.info("⚠️ Risk Agent initialized successfully")
        except Exception as e:
            logger.error(f"❌ Error initializing Risk Agent: {e}")
            raise
    
    async def _load_risk_data(self):
        """Load weather, pest, and risk data"""
        # Weather patterns and forecasts for Punjab
        self.weather_data = {
            "current_conditions": {
                "temperature": "32°C",
                "humidity": "65%",
                "wind_speed": "12 km/h",
                "precipitation_chance": "20%",
                "uv_index": "High",
                "last_updated": "2024-08-18"
            },
            "seasonal_forecast": {
                "monsoon_2024": {
                    "start_date": "June 15, 2024",
                    "end_date": "September 30, 2024",
                    "expected_rainfall": "650mm",
                    "normal_rainfall": "600mm",
                    "deviation": "+8%",
                    "risk_level": "Low"
                },
                "winter_2024": {
                    "start_date": "December 1, 2024",
                    "end_date": "February 28, 2025",
                    "expected_rainfall": "150mm",
                    "normal_rainfall": "120mm",
                    "deviation": "+25%",
                    "risk_level": "Medium"
                }
            },
            "extreme_events": {
                "drought_risk": {
                    "probability": "15%",
                    "affected_districts": ["Bathinda", "Mansa", "Muktsar"],
                    "impact": "Crop failure, water scarcity",
                    "mitigation": "Drip irrigation, drought-resistant crops"
                },
                "flood_risk": {
                    "probability": "10%",
                    "affected_districts": ["Amritsar", "Gurdaspur", "Tarn Taran"],
                    "impact": "Crop damage, soil erosion",
                    "mitigation": "Drainage systems, elevated storage"
                },
                "heat_wave_risk": {
                    "probability": "25%",
                    "affected_districts": ["All districts"],
                    "impact": "Crop stress, reduced yield",
                    "mitigation": "Shade nets, frequent irrigation"
                },
                "frost_risk": {
                    "probability": "20%",
                    "affected_districts": ["Patiala", "Sangrur", "Ludhiana"],
                    "impact": "Winter crop damage",
                    "mitigation": "Frost protection, crop timing"
                }
            }
        }
        
        # Pest and disease monitoring
        self.pest_data = {
            "current_threats": {
                "fall_armyworm": {
                    "crops_affected": ["maize", "sugarcane"],
                    "severity": "High",
                    "affected_districts": ["Ludhiana", "Jalandhar", "Amritsar"],
                    "control_measures": ["Biological control", "Chemical pesticides", "Crop rotation"],
                    "economic_impact": "Up to 40% yield loss"
                },
                "pink_bollworm": {
                    "crops_affected": ["cotton"],
                    "severity": "Medium",
                    "affected_districts": ["Bathinda", "Mansa", "Muktsar"],
                    "control_measures": ["Bt cotton", "Pheromone traps", "Early harvest"],
                    "economic_impact": "Up to 25% yield loss"
                },
                "brown_planthopper": {
                    "crops_affected": ["rice"],
                    "severity": "Low",
                    "affected_districts": ["Patiala", "Sangrur"],
                    "control_measures": ["Resistant varieties", "Biological control", "Water management"],
                    "economic_impact": "Up to 15% yield loss"
                },
                "yellow_rust": {
                    "crops_affected": ["wheat"],
                    "severity": "Medium",
                    "affected_districts": ["All districts"],
                    "control_measures": ["Resistant varieties", "Fungicides", "Early sowing"],
                    "economic_impact": "Up to 20% yield loss"
                }
            },
            "preventive_measures": {
                "integrated_pest_management": {
                    "cultural_practices": ["Crop rotation", "Field sanitation", "Timely sowing"],
                    "biological_control": ["Trichogramma", "Neem products", "Bacillus thuringiensis"],
                    "chemical_control": ["Targeted spraying", "Resistance management", "Safe intervals"],
                    "monitoring": ["Pheromone traps", "Field scouting", "Weather-based alerts"]
                }
            }
        }
        
        # Market and financial risks
        self.market_risks = {
            "price_volatility": {
                "wheat": {
                    "volatility_index": "Medium",
                    "risk_factors": ["Export policies", "Government procurement", "Global prices"],
                    "mitigation": ["Forward contracts", "Diversification", "Storage facilities"]
                },
                "rice": {
                    "volatility_index": "High",
                    "risk_factors": ["Export demand", "Monsoon impact", "International prices"],
                    "mitigation": ["Contract farming", "Value addition", "Market timing"]
                },
                "cotton": {
                    "volatility_index": "Very High",
                    "risk_factors": ["Textile industry demand", "Import policies", "Global supply"],
                    "mitigation": ["Insurance", "Diversification", "Quality improvement"]
                },
                "sugarcane": {
                    "volatility_index": "Low",
                    "risk_factors": ["Sugar mill policies", "Government pricing", "Transport costs"],
                    "mitigation": ["Contract farming", "Cooperative membership", "Local processing"]
                }
            },
            "credit_risks": {
                "loan_default": {
                    "probability": "8%",
                    "risk_factors": ["Crop failure", "Price crash", "Natural calamities"],
                    "mitigation": ["Crop insurance", "Diversification", "Emergency funds"]
                },
                "interest_rate": {
                    "current_rate": "7.0%",
                    "trend": "Stable",
                    "risk_factors": ["RBI policies", "Inflation", "Economic conditions"],
                    "mitigation": ["Fixed rate loans", "Early repayment", "Refinancing options"]
                }
            }
        }
        
        # Climate change risks
        self.climate_risks = {
            "temperature_changes": {
                "current_trend": "+0.5°C per decade",
                "projected_2050": "+2.0°C",
                "impact": "Reduced crop yields, increased water demand",
                "adaptation": ["Heat-resistant varieties", "irrigation systems"]
            },
            "rainfall_patterns": {
                "current_trend": "Erratic rainfall",
                "projected_2050": "Increased variability",
                "impact": "Drought and flood risks",
                "adaptation": ["Water harvesting", "drainage systems"]
            },
            "extreme_events": {
                "frequency": "Increasing",
                "types": ["Heat waves", "Heavy rainfall", "Droughts"],
                "impact": "Crop damage, infrastructure loss",
                "adaptation": ["Early warning systems", "resilient infrastructure"]
            }
        }
        
        # Risk assessment matrix
        self.risk_matrix = {
            "low_risk": {
                "probability": "0-20%",
                "impact": "Minimal",
                "action": "Monitor and maintain current practices"
            },
            "medium_risk": {
                "probability": "21-50%",
                "impact": "Moderate",
                "action": "Implement preventive measures"
            },
            "high_risk": {
                "probability": "51-80%",
                "impact": "Significant",
                "action": "Develop contingency plans"
            },
            "very_high_risk": {
                "probability": "81-100%",
                "impact": "Severe",
                "action": "Immediate action required"
            }
        }
        
        # Risk mitigation strategies
        self.mitigation_strategies = {
            "weather_risks": {
                "drought": ["Drip irrigation", "Drought-resistant crops", "Water harvesting"],
                "flood": ["Drainage systems", "Elevated storage", "Flood-resistant crops"],
                "frost": ["Frost protection", "Crop timing", "Greenhouse farming"],
                "heat_wave": ["Shade nets", "Frequent irrigation", "Heat-resistant varieties"]
            },
            "pest_risks": {
                "prevention": ["Crop rotation", "Field sanitation", "Resistant varieties"],
                "control": ["Biological control", "Integrated pest management", "Monitoring"],
                "recovery": ["Replanting", "Insurance claims", "Alternative crops"]
            },
            "market_risks": {
                "price_volatility": ["Forward contracts", "Diversification", "Value addition"],
                "demand_fluctuation": ["Market research", "Contract farming", "Storage facilities"],
                "supply_chain": ["Multiple suppliers", "Local processing", "Cooperative membership"]
            },
            "financial_risks": {
                "credit": ["Crop insurance", "Emergency funds", "Diversified income"],
                "interest_rate": ["Fixed rate loans", "Early repayment", "Refinancing"],
                "currency": ["Local markets", "Forward contracts", "Hedging strategies"]
            }
        }
    
    async def process(self, query: str, user_context: Dict, language: str = "hi") -> str:
        """Process risk-related queries"""
        try:
            # Analyze query type
            query_type = self._analyze_risk_query(query)
            
            if query_type == "weather_alert":
                return await self._handle_weather_alert(user_context, language)
            elif query_type == "pest_alert":
                return await self._handle_pest_alert(user_context, language)
            elif query_type == "risk_assessment":
                return await self._handle_risk_assessment(user_context, language)
            elif query_type == "mitigation_strategy":
                return await self._handle_mitigation_strategy(user_context, language)
            else:
                return await self._handle_general_risk_query(query, user_context, language)
                
        except Exception as e:
            logger.error(f"❌ Error in Risk Agent: {e}")
            return self._get_error_response(language)
    
    def _analyze_risk_query(self, query: str) -> str:
        """Analyze the type of risk query"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["weather", "rain", "drought", "flood", "mausam"]):
            return "weather_alert"
        elif any(word in query_lower for word in ["pest", "disease", "keet", "rogi"]):
            return "pest_alert"
        elif any(word in query_lower for word in ["risk", "danger", "threat", "khatra"]):
            return "risk_assessment"
        elif any(word in query_lower for word in ["prevent", "protect", "save", "bachao"]):
            return "mitigation_strategy"
        else:
            return "general"
    
    async def _handle_weather_alert(self, user_context: Dict, language: str) -> str:
        """Handle weather alert queries"""
        location = user_context.get("location", "Punjab")
        current_crops = user_context.get("current_crops", [])
        
        # Get relevant weather alerts for the location
        relevant_alerts = []
        for alert_type, alert_data in self.weather_alerts.items():
            if location in alert_data["affected_regions"]:
                relevant_alerts.append({
                    "type": alert_type,
                    "data": alert_data
                })
        
        if language == "hi":
            if relevant_alerts:
                response = f"⚠️ {location} के लिए मौसम चेतावनी:\n\n"
                
                for alert in relevant_alerts:
                    data = alert["data"]
                    risk_emoji = "🔴" if data["risk_level"] == "high" else "🟡"
                    response += f"""{risk_emoji} {alert['type'].title()}:
📊 जोखिम स्तर: {data['risk_level'].title()}
💥 प्रभाव: {data['impact']}
🛡️ बचाव: {data['mitigation']}

"""
                
                response += "📱 अलर्ट प्राप्त करने के लिए:\n"
                response += "• IMD वेबसाइट पर जाएं\n"
                response += "• मौसम ऐप डाउनलोड करें\n"
                response += "• कृषि विभाग से संपर्क करें"
            else:
                response = f"✅ {location} में कोई मौसम चेतावनी नहीं है।\n\n"
                response += "🌤️ वर्तमान मौसम स्थिति सामान्य है।"
            
            return response
        else:
            if relevant_alerts:
                response = f"⚠️ Weather Alert for {location}:\n\n"
                
                for alert in relevant_alerts:
                    data = alert["data"]
                    risk_emoji = "🔴" if data["risk_level"] == "high" else "🟡"
                    response += f"""{risk_emoji} {alert['type'].title()}:
📊 Risk Level: {data['risk_level'].title()}
💥 Impact: {data['impact']}
🛡️ Mitigation: {data['mitigation']}

"""
                
                response += "📱 To receive alerts:\n"
                response += "• Visit IMD website\n"
                response += "• Download weather app\n"
                response += "• Contact agriculture department"
            else:
                response = f"✅ No weather alerts for {location}.\n\n"
                response += "🌤️ Current weather conditions are normal."
            
            return response
    
    async def _handle_pest_alert(self, user_context: Dict, language: str) -> str:
        """Handle pest alert queries"""
        location = user_context.get("location", "Punjab")
        current_crops = user_context.get("current_crops", [])
        
        # Get relevant pest alerts
        relevant_pests = []
        for pest_type, pest_data in self.pest_alerts.items():
            if location in pest_data["affected_regions"]:
                # Check if user's crops are affected
                affected_crops = pest_data["affected_crops"]
                user_crops = [crop.get("name", "") for crop in current_crops]
                if any(crop in affected_crops for crop in user_crops):
                    relevant_pests.append({
                        "type": pest_type,
                        "data": pest_data
                    })
        
        if language == "hi":
            if relevant_pests:
                response = f"🐛 {location} में कीट चेतावनी:\n\n"
                
                for pest in relevant_pests:
                    data = pest["data"]
                    risk_emoji = "🔴" if data["risk_level"] == "high" else "🟡"
                    response += f"""{risk_emoji} {pest['type'].replace('_', ' ').title()}:
📊 जोखिम स्तर: {data['risk_level'].title()}
🌾 प्रभावित फसलें: {', '.join(data['affected_crops'])}
🔍 लक्षण: {data['symptoms']}
🛡️ नियंत्रण: {data['control']}

"""
                
                response += "💡 कीट प्रबंधन सुझाव:\n"
                response += "• नियमित निरीक्षण करें\n"
                response += "• जैविक कीटनाशक प्रयोग करें\n"
                response += "• फसल चक्र अपनाएं\n"
                response += "• कृषि विभाग से सलाह लें"
            else:
                response = f"✅ {location} में कोई कीट चेतावनी नहीं है।\n\n"
                response += "🌱 आपकी फसलें सुरक्षित हैं।"
            
            return response
        else:
            if relevant_pests:
                response = f"🐛 Pest Alert for {location}:\n\n"
                
                for pest in relevant_pests:
                    data = pest["data"]
                    risk_emoji = "🔴" if data["risk_level"] == "high" else "🟡"
                    response += f"""{risk_emoji} {pest['type'].replace('_', ' ').title()}:
📊 Risk Level: {data['risk_level'].title()}
🌾 Affected Crops: {', '.join(data['affected_crops'])}
🔍 Symptoms: {data['symptoms']}
🛡️ Control: {data['control']}

"""
                
                response += "💡 Pest Management Tips:\n"
                response += "• Regular monitoring\n"
                response += "• Use organic pesticides\n"
                response += "• Follow crop rotation\n"
                response += "• Consult agriculture department"
            else:
                response = f"✅ No pest alerts for {location}.\n\n"
                response += "🌱 Your crops are safe."
            
            return response
    
    async def _handle_risk_assessment(self, user_context: Dict, language: str) -> str:
        """Handle risk assessment queries"""
        location = user_context.get("location", "Punjab")
        current_crops = user_context.get("current_crops", [])
        current_season = self._get_current_season()
        
        # Assess overall risk
        risk_factors = []
        
        # Weather risks
        for alert_type, alert_data in self.weather_alerts.items():
            if location in alert_data["affected_regions"]:
                risk_factors.append(f"Weather: {alert_type}")
        
        # Pest risks
        for pest_type, pest_data in self.pest_alerts.items():
            if location in pest_data["affected_regions"]:
                affected_crops = pest_data["affected_crops"]
                user_crops = [crop.get("name", "") for crop in current_crops]
                if any(crop in affected_crops for crop in user_crops):
                    risk_factors.append(f"Pest: {pest_type}")
        
        # Seasonal risks
        seasonal_risks = self.seasonal_risks.get(current_season, {})
        for risk_type, risk_desc in seasonal_risks.items():
            risk_factors.append(f"Seasonal: {risk_type}")
        
        if language == "hi":
            response = f"🔍 आपकी फसलों का जोखिम मूल्यांकन:\n\n"
            
            response += f"📍 स्थान: {location}\n"
            response += f"🌾 फसलें: {len(current_crops)} फसलें\n"
            response += f"📅 मौसम: {current_season.title()}\n\n"
            
            if risk_factors:
                response += "⚠️ पहचाने गए जोखिम:\n"
                for i, risk in enumerate(risk_factors, 1):
                    response += f"{i}. {risk}\n"
                
                response += f"\n📊 कुल जोखिम स्तर: {'उच्च' if len(risk_factors) > 3 else 'मध्यम' if len(risk_factors) > 1 else 'कम'}\n"
            else:
                response += "✅ कोई जोखिम नहीं पहचाना गया।\n"
            
            response += "\n💡 सुझाव:\n"
            response += "• नियमित निगरानी करें\n"
            response += "• बीमा करवाएं\n"
            response += "• विविधीकरण करें\n"
            response += "• आपातकालीन योजना बनाएं"
            
            return response
        else:
            response = f"🔍 Risk Assessment for Your Crops:\n\n"
            
            response += f"📍 Location: {location}\n"
            response += f"🌾 Crops: {len(current_crops)} crops\n"
            response += f"📅 Season: {current_season.title()}\n\n"
            
            if risk_factors:
                response += "⚠️ Identified Risks:\n"
                for i, risk in enumerate(risk_factors, 1):
                    response += f"{i}. {risk}\n"
                
                response += f"\n📊 Overall Risk Level: {'High' if len(risk_factors) > 3 else 'Medium' if len(risk_factors) > 1 else 'Low'}\n"
            else:
                response += "✅ No risks identified.\n"
            
            response += "\n💡 Recommendations:\n"
            response += "• Regular monitoring\n"
            response += "• Get insurance\n"
            response += "• Diversify crops\n"
            response += "• Plan for emergencies"
            
            return response
    
    async def _handle_mitigation_strategy(self, user_context: Dict, language: str) -> str:
        """Handle mitigation strategy queries"""
        location = user_context.get("location", "Punjab")
        current_crops = user_context.get("current_crops", [])
        
        if language == "hi":
            return f"""🛡️ जोखिम कम करने की रणनीतियां:

🌤️ मौसम जोखिम के लिए:
• फसल बीमा करवाएं
• सिंचाई व्यवस्था सुधारें
• मौसम पूर्वानुमान जांचें
• आपातकालीन योजना बनाएं

🐛 कीट जोखिम के लिए:
• नियमित निरीक्षण करें
• जैविक कीटनाशक प्रयोग करें
• फसल चक्र अपनाएं
• प्रतिरोधी किस्में उगाएं

💰 आर्थिक जोखिम के लिए:
• फसल विविधीकरण करें
• बाजार के दामों पर नजर रखें
• सरकारी सब्सिडी का लाभ उठाएं
• बचत और बीमा करें

📞 आपातकालीन संपर्क:
• कृषि विभाग: 1800-180-1551
• मौसम विभाग: 1800-180-1717
• बीमा कंपनी: अपने बैंक से संपर्क करें"""
        else:
            return f"""🛡️ Risk Mitigation Strategies:

🌤️ For Weather Risks:
• Get crop insurance
• Improve irrigation systems
• Check weather forecasts
• Plan for emergencies

🐛 For Pest Risks:
• Regular monitoring
• Use organic pesticides
• Follow crop rotation
• Grow resistant varieties

💰 For Financial Risks:
• Diversify crops
• Monitor market prices
• Avail government subsidies
• Save and insure

📞 Emergency Contacts:
• Agriculture Department: 1800-180-1551
• Weather Department: 1800-180-1717
• Insurance Company: Contact your bank"""
    
    async def _handle_general_risk_query(self, query: str, user_context: Dict, language: str) -> str:
        """Handle general risk queries"""
        if language == "hi":
            return """⚠️ जोखिम प्रबंधन सलाह:

• नियमित रूप से मौसम जांचें
• फसलों का निरीक्षण करें
• बीमा करवाएं
• आपातकालीन योजना बनाएं
• विविधीकरण करें

क्या आप मौसम चेतावनी, कीट प्रबंधन या जोखिम कम करने के बारे में जानना चाहते हैं?"""
        else:
            return """⚠️ Risk Management Advice:

• Check weather regularly
• Monitor crops
• Get insurance
• Plan for emergencies
• Diversify

Do you want to know about weather alerts, pest management, or risk reduction?"""
    
    def _get_current_season(self) -> str:
        """Get current agricultural season"""
        current_month = datetime.now().month
        
        if current_month in [6, 7, 8, 9]:
            return "kharif"
        elif current_month in [10, 11, 12, 1]:
            return "rabi"
        else:
            return "zaid"
    
    def _get_error_response(self, language: str) -> str:
        """Error response in appropriate language"""
        if language == "hi":
            return "माफ़ करें, जोखिम जानकारी देने में समस्या आ रही है। कृपया कुछ देर बाद फिर से कोशिश करें।"
        else:
            return "Sorry, there's an issue providing risk information. Please try again later."
    
    async def get_risk_assessment(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive risk assessment for a user"""
        # Mock user context - in production would fetch from database
        user_context = {
            "user_id": user_id,
            "location": "Punjab",
            "current_crops": [
                {"name": "wheat", "area": 5.0, "stage": "growing"}
            ],
            "land_area": 5.0
        }
        
        # Calculate risk score
        risk_score = 0
        risk_factors = []
        
        # Weather risks
        for alert_type, alert_data in self.weather_alerts.items():
            if user_context["location"] in alert_data["affected_regions"]:
                risk_score += 2 if alert_data["risk_level"] == "high" else 1
                risk_factors.append(f"Weather: {alert_type}")
        
        # Pest risks
        for pest_type, pest_data in self.pest_alerts.items():
            if user_context["location"] in pest_data["affected_regions"]:
                affected_crops = pest_data["affected_crops"]
                user_crops = [crop.get("name", "") for crop in user_context["current_crops"]]
                if any(crop in affected_crops for crop in user_crops):
                    risk_score += 2 if pest_data["risk_level"] == "high" else 1
                    risk_factors.append(f"Pest: {pest_type}")
        
        risk_level = "High" if risk_score > 4 else "Medium" if risk_score > 2 else "Low"
        
        return {
            "user_id": user_id,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "recommendations": [
                "Monitor weather forecasts regularly",
                "Implement pest control measures",
                "Consider crop insurance",
                "Diversify crop portfolio"
            ]
        }
