import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from loguru import logger
from app.core.config import settings

class PolicyAgent:
    """
    Policy Agent - Handles government schemes, subsidies, and policy information
    for Indian farmers.
    """
    
    def __init__(self):
        self.name = "Policy Agent"
        self.description = "Specialized in government schemes, subsidies, and policy guidance"
        self.initialized = False
        
    async def initialize(self):
        """Initialize the policy agent with scheme and subsidy data"""
        try:
            await self._load_policy_data()
            self.initialized = True
            logger.info("🏛️ Policy Agent initialized successfully")
        except Exception as e:
            logger.error(f"❌ Error initializing Policy Agent: {e}")
            raise
    
    async def _load_policy_data(self):
        """Load government schemes, subsidies, and policy data"""
        # Comprehensive government schemes for Punjab farmers
        self.government_schemes = {
            "pm_kisan": {
                "name": "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
                "amount": 6000,
                "frequency": "yearly",
                "eligibility": "Small and marginal farmers (up to 2 hectares)",
                "application": "Online through PM-KISAN portal",
                "disbursement": "Quarterly installments of ₹2000",
                "deadline": "Ongoing",
                "contact": "1800-180-1551",
                "website": "pmkisan.gov.in",
                "documents_required": ["Aadhaar", "Land records", "Bank account"]
            },
            "pm_fasal_bima_yojana": {
                "name": "PM Fasal Bima Yojana (Crop Insurance)",
                "amount": "Up to 100% of sum insured",
                "frequency": "per_crop_season",
                "eligibility": "All farmers growing notified crops",
                "application": "Through banks or insurance companies",
                "disbursement": "Within 10 days of loss assessment",
                "deadline": "Before sowing",
                "contact": "1800-180-1551",
                "website": "pmfby.gov.in",
                "documents_required": ["Land records", "Crop details", "Bank account"]
            },
            "kisan_credit_card": {
                "name": "Kisan Credit Card (KCC)",
                "amount": "Up to ₹3 lakhs",
                "frequency": "renewable",
                "eligibility": "All farmers including tenant farmers",
                "application": "Through banks",
                "disbursement": "Within 7 days",
                "deadline": "Anytime",
                "contact": "Local bank branches",
                "website": "nccf.in",
                "documents_required": ["Aadhaar", "Land records", "Income certificate"]
            },
            "pm_ksy": {
                "name": "PM Kisan Sampada Yojana (Food Processing)",
                "amount": "Up to ₹10 crores",
                "frequency": "one_time",
                "eligibility": "Food processing units and farmers",
                "application": "Through Ministry of Food Processing",
                "disbursement": "After project approval",
                "deadline": "31st March 2025",
                "contact": "011-26492200",
                "website": "mofpi.gov.in",
                "documents_required": ["Project proposal", "Land documents", "Financial statements"]
            },
            "pm_ksn": {
                "name": "PM Kisan Suryodaya Yojana (Solar Pumps)",
                "amount": "Up to ₹1.5 lakhs",
                "frequency": "one_time",
                "eligibility": "Farmers with 2+ acres",
                "application": "Through agriculture department",
                "disbursement": "After installation",
                "deadline": "31st December 2024",
                "contact": "1800-180-1551",
                "website": "pmksy.gov.in",
                "documents_required": ["Land records", "Electricity connection", "Bank account"]
            },
            "pm_ksy_horticulture": {
                "name": "PM Kisan Sampada Yojana - Horticulture",
                "amount": "Up to ₹50 lakhs",
                "frequency": "one_time",
                "eligibility": "Horticulture farmers",
                "application": "Through horticulture department",
                "disbursement": "After project completion",
                "deadline": "31st March 2025",
                "contact": "011-23382642",
                "website": "nhb.gov.in",
                "documents_required": ["Project proposal", "Land documents", "Technical feasibility"]
            }
        }
        
        # Punjab-specific subsidy schemes
        self.punjab_subsidies = {
            "seed_subsidy": {
                "name": "Seed Subsidy Scheme",
                "amount": 500,
                "frequency": "per_quintal",
                "eligibility": "Small and marginal farmers",
                "application": "Through agriculture department",
                "disbursement": "Subsidized seed distribution",
                "deadline": "Before sowing season",
                "contact": "0172-2700711",
                "website": "punjab.gov.in/agriculture",
                "documents_required": ["Land records", "Farmer ID", "Seed requirement"]
            },
            "fertilizer_subsidy": {
                "name": "Fertilizer Subsidy",
                "amount": 1400,
                "frequency": "per_bag",
                "eligibility": "All farmers",
                "application": "Through authorized dealers",
                "disbursement": "Direct benefit transfer",
                "deadline": "Ongoing",
                "contact": "1800-180-1551",
                "website": "fertilizer.gov.in",
                "documents_required": ["Aadhaar", "Land records", "Bank account"]
            },
            "pesticide_subsidy": {
                "name": "Pesticide Subsidy",
                "amount": 300,
                "frequency": "per_liter",
                "eligibility": "All farmers",
                "application": "Through authorized centers",
                "disbursement": "Subsidized pesticide distribution",
                "deadline": "Before pest attack",
                "contact": "0172-2700711",
                "website": "punjab.gov.in/agriculture",
                "documents_required": ["Land records", "Crop details", "Pest identification"]
            },
            "drip_irrigation_subsidy": {
                "name": "Drip Irrigation Subsidy",
                "amount": 50000,
                "frequency": "one_time",
                "eligibility": "Farmers with 2+ acres",
                "application": "Through agriculture department",
                "disbursement": "After installation verification",
                "deadline": "31st March 2025",
                "contact": "0172-2700711",
                "website": "punjab.gov.in/agriculture",
                "documents_required": ["Land records", "Water source", "Technical approval"]
            },
            "farm_machinery_subsidy": {
                "name": "Farm Machinery Subsidy",
                "amount": "Up to 40% of cost",
                "frequency": "one_time",
                "eligibility": "Farmers with 5+ acres",
                "application": "Through agriculture department",
                "disbursement": "After purchase verification",
                "deadline": "31st March 2025",
                "contact": "0172-2700711",
                "website": "punjab.gov.in/agriculture",
                "documents_required": ["Land records", "Machine quotation", "Bank loan approval"]
            }
        }
        
        # Loan policies and interest rates
        self.loan_policies = {
            "crop_loan": {
                "interest_rate": 7.0,
                "max_amount": 300000,
                "tenure": 12,
                "processing_fee": 0.5,
                "collateral": "Crop hypothecation",
                "eligibility": "All farmers with land ownership",
                "repayment": "After harvest",
                "subsidy": "Interest subvention of 2% for timely repayment"
            },
            "term_loan": {
                "interest_rate": 8.5,
                "max_amount": 1000000,
                "tenure": 60,
                "processing_fee": 1.0,
                "collateral": "Land mortgage",
                "eligibility": "Farmers with 5+ years experience",
                "repayment": "Monthly installments",
                "subsidy": "Interest subvention of 1.5% for women farmers"
            },
            "dairy_loan": {
                "interest_rate": 6.5,
                "max_amount": 500000,
                "tenure": 36,
                "processing_fee": 0.75,
                "collateral": "Livestock hypothecation",
                "eligibility": "Farmers with dairy experience",
                "repayment": "Monthly installments",
                "subsidy": "Interest subvention of 2% for small farmers"
            },
            "horticulture_loan": {
                "interest_rate": 6.8,
                "max_amount": 400000,
                "tenure": 48,
                "processing_fee": 0.8,
                "collateral": "Crop and land",
                "eligibility": "Farmers with horticulture training",
                "repayment": "After harvest",
                "subsidy": "Interest subvention of 1.5% for organic farming"
            }
        }
        
        # Application centers and support
        self.application_centers = {
            "agriculture_department": {
                "name": "Agriculture Department Office",
                "services": ["PM-KISAN", "Seed subsidy", "Crop insurance", "Drip irrigation"],
                "contact": "0172-2700711",
                "address": "Sector 17, Chandigarh",
                "working_hours": "9:00 AM - 5:00 PM",
                "online_services": True
            },
            "bank_branch": {
                "name": "Bank Branch",
                "services": ["PM-KISAN", "Crop loans", "KCC", "Insurance"],
                "contact": "Varies by bank",
                "address": "Local bank branches",
                "working_hours": "10:00 AM - 4:00 PM",
                "online_services": True
            },
            "common_service_center": {
                "name": "Common Service Center (CSC)",
                "services": ["All schemes", "Online applications", "Document verification"],
                "contact": "1800-3000-3468",
                "address": "Village panchayats",
                "working_hours": "8:00 AM - 8:00 PM",
                "online_services": True
            },
            "krishi_vigyan_kendra": {
                "name": "Krishi Vigyan Kendra",
                "services": ["Technical guidance", "Training programs", "Scheme information"],
                "contact": "0172-2700711",
                "address": "District headquarters",
                "working_hours": "9:00 AM - 6:00 PM",
                "online_services": False
            }
        }
    
    async def process(self, query: str, user_context: Dict, language: str = "hi") -> str:
        """Process policy-related queries"""
        try:
            # Analyze query type
            query_type = self._analyze_policy_query(query)
            
            if query_type == "scheme_info":
                return await self._handle_scheme_info(user_context, language)
            elif query_type == "eligibility_check":
                return await self._handle_eligibility_check(user_context, language)
            elif query_type == "application_help":
                return await self._handle_application_help(user_context, language)
            elif query_type == "subsidy_info":
                return await self._handle_subsidy_info(user_context, language)
            else:
                return await self._handle_general_policy_query(query, user_context, language)
                
        except Exception as e:
            logger.error(f"❌ Error in Policy Agent: {e}")
            return self._get_error_response(language)
    
    def _analyze_policy_query(self, query: str) -> str:
        """Analyze the type of policy query"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["scheme", "yojana", "program"]):
            return "scheme_info"
        elif any(word in query_lower for word in ["eligible", "qualify", "check"]):
            return "eligibility_check"
        elif any(word in query_lower for word in ["apply", "application", "form"]):
            return "application_help"
        elif any(word in query_lower for word in ["subsidy", "help", "support"]):
            return "subsidy_info"
        else:
            return "general"
    
    async def _handle_scheme_info(self, user_context: Dict, language: str) -> str:
        """Handle scheme information queries"""
        land_area = user_context.get("land_area", 0)
        location = user_context.get("location", "Punjab")
        
        # Get relevant schemes based on user profile
        relevant_schemes = []
        
        for scheme_id, scheme_data in self.government_schemes.items():
            if scheme_data["status"] == "active":
                # Check eligibility based on land area
                land_limit = scheme_data.get("land_limit", float('inf'))
                if land_area <= land_limit:
                    relevant_schemes.append({
                        "id": scheme_id,
                        "data": scheme_data
                    })
        
        # Add state-specific schemes
        state_schemes = self.state_schemes.get(location, {})
        for scheme_id, scheme_data in state_schemes.items():
            relevant_schemes.append({
                "id": scheme_id,
                "data": scheme_data
            })
        
        if language == "hi":
            response = f"🏛️ आपके लिए उपलब्ध सरकारी योजनाएं:\n\n"
            
            for scheme in relevant_schemes[:5]:  # Show top 5 schemes
                data = scheme["data"]
                response += f"""📋 {data['name']}:
💰 राशि: {data.get('amount', 'Variable')}
📅 आवृत्ति: {data.get('frequency', 'One-time')}
✅ पात्रता: {', '.join(data.get('eligibility', ['All farmers']))}
📝 विवरण: {data.get('description', 'No description available')}

"""
            
            response += "📞 आवेदन के लिए संपर्क करें:\n"
            response += "• कृषि विभाग कार्यालय\n"
            response += "• बैंक शाखा\n"
            response += "• कॉमन सर्विस सेंटर (CSC)\n"
            response += "• ऑनलाइन पोर्टल"
            
            return response
        else:
            response = f"🏛️ Government Schemes Available for You:\n\n"
            
            for scheme in relevant_schemes[:5]:  # Show top 5 schemes
                data = scheme["data"]
                response += f"""📋 {data['name']}:
💰 Amount: {data.get('amount', 'Variable')}
📅 Frequency: {data.get('frequency', 'One-time')}
✅ Eligibility: {', '.join(data.get('eligibility', ['All farmers']))}
📝 Description: {data.get('description', 'No description available')}

"""
            
            response += "📞 To Apply Contact:\n"
            response += "• Agriculture Department Office\n"
            response += "• Bank Branch\n"
            response += "• Common Service Center (CSC)\n"
            response += "• Online Portal"
            
            return response
    
    async def _handle_eligibility_check(self, user_context: Dict, language: str) -> str:
        """Handle eligibility check queries"""
        land_area = user_context.get("land_area", 0)
        location = user_context.get("location", "Punjab")
        
        eligibility_results = []
        
        for scheme_id, scheme_data in self.schemes.items():
            if scheme_data["status"] == "active":
                land_limit = scheme_data.get("land_limit", float('inf'))
                is_eligible = land_area <= land_limit
                
                eligibility_results.append({
                    "scheme": scheme_data["name"],
                    "eligible": is_eligible,
                    "reason": f"Land area: {land_area} acres" if is_eligible else f"Land limit: {land_limit} hectares"
                })
        
        if language == "hi":
            response = "✅ आपकी योजना पात्रता जांच:\n\n"
            
            for result in eligibility_results:
                status = "✅ पात्र" if result["eligible"] else "❌ अपात्र"
                response += f"""📋 {result['scheme']}:
{status}
📝 कारण: {result['reason']}

"""
            
            response += "💡 सुझाव:\n"
            response += "• पात्र योजनाओं के लिए आवेदन करें\n"
            response += "• आवश्यक दस्तावेज तैयार रखें\n"
            response += "• नियमित अपडेट जांचें"
            
            return response
        else:
            response = "✅ Your Scheme Eligibility Check:\n\n"
            
            for result in eligibility_results:
                status = "✅ Eligible" if result["eligible"] else "❌ Not Eligible"
                response += f"""📋 {result['scheme']}:
{status}
📝 Reason: {result['reason']}

"""
            
            response += "💡 Tips:\n"
            response += "• Apply for eligible schemes\n"
            response += "• Keep required documents ready\n"
            response += "• Check for regular updates"
            
            return response
    
    async def _handle_application_help(self, user_context: Dict, language: str) -> str:
        """Handle application help queries"""
        if language == "hi":
            return """📝 योजना आवेदन में सहायता:

📋 आवश्यक दस्तावेज:
• आधार कार्ड
• भूमि के कागजात
• बैंक खाता विवरण
• फोटो
• जाति प्रमाण पत्र (यदि लागू)

📞 आवेदन केंद्र:
• कृषि विभाग कार्यालय
• बैंक शाखा
• कॉमन सर्विस सेंटर (CSC)
• ऑनलाइन पोर्टल

⏰ प्रक्रिया:
1. दस्तावेज इकट्ठा करें
2. निकटतम केंद्र पर जाएं
3. फॉर्म भरें और जमा करें
4. आवेदन संख्या नोट करें
5. स्थिति जांचें

📞 हेल्पलाइन: 1800-180-1551"""
        else:
            return """📝 Scheme Application Help:

📋 Required Documents:
• Aadhaar Card
• Land Records
• Bank Account Details
• Photos
• Caste Certificate (if applicable)

📞 Application Centers:
• Agriculture Department Office
• Bank Branch
• Common Service Center (CSC)
• Online Portal

⏰ Process:
1. Collect documents
2. Visit nearest center
3. Fill and submit form
4. Note application number
5. Check status

📞 Helpline: 1800-180-1551"""
    
    async def _handle_subsidy_info(self, user_context: Dict, language: str) -> str:
        """Handle subsidy information queries"""
        current_crops = user_context.get("current_crops", [])
        
        relevant_subsidies = []
        
        # Get subsidies relevant to user's crops
        for scheme_id, scheme_data in self.schemes.items():
            if "subsidy" in scheme_id.lower() or "fertilizer" in scheme_id.lower() or "seed" in scheme_id.lower():
                relevant_subsidies.append({
                    "id": scheme_id,
                    "data": scheme_data
                })
        
        if language == "hi":
            response = "💰 आपके लिए उपलब्ध सब्सिडी:\n\n"
            
            for subsidy in relevant_subsidies:
                data = subsidy["data"]
                response += f"""💰 {data['name']}:
💵 राशि: {data.get('amount', 'Variable')}
📅 आवृत्ति: {data.get('frequency', 'One-time')}
✅ पात्रता: {', '.join(data.get('eligibility', ['All farmers']))}
📝 विवरण: {data.get('description', 'No description available')}

"""
            
            response += "💡 सब्सिडी के लाभ:\n"
            response += "• कृषि लागत कम होती है\n"
            response += "• लाभ बढ़ता है\n"
            response += "• जोखिम कम होता है\n"
            response += "• आधुनिक तकनीक अपनाने में मदद"
            
            return response
        else:
            response = "💰 Subsidies Available for You:\n\n"
            
            for subsidy in relevant_subsidies:
                data = subsidy["data"]
                response += f"""💰 {data['name']}:
💵 Amount: {data.get('amount', 'Variable')}
📅 Frequency: {data.get('frequency', 'One-time')}
✅ Eligibility: {', '.join(data.get('eligibility', ['All farmers']))}
📝 Description: {data.get('description', 'No description available')}

"""
            
            response += "💡 Benefits of Subsidies:\n"
            response += "• Reduces agricultural costs\n"
            response += "• Increases profits\n"
            response += "• Reduces risk\n"
            response += "• Helps adopt modern technology"
            
            return response
    
    async def _handle_general_policy_query(self, query: str, user_context: Dict, language: str) -> str:
        """Handle general policy queries"""
        if language == "hi":
            return """🏛️ सरकारी योजना सलाह:

• नियमित रूप से नई योजनाएं जांचें
• पात्रता मापदंड समझें
• आवश्यक दस्तावेज तैयार रखें
• समय पर आवेदन करें
• आवेदन स्थिति जांचें

क्या आप किसी विशेष योजना, सब्सिडी या आवेदन प्रक्रिया के बारे में जानना चाहते हैं?"""
        else:
            return """🏛️ Government Scheme Advice:

• Check for new schemes regularly
• Understand eligibility criteria
• Keep required documents ready
• Apply on time
• Check application status

Do you want to know about specific schemes, subsidies, or application process?"""
    
    def _get_error_response(self, language: str) -> str:
        """Error response in appropriate language"""
        if language == "hi":
            return "माफ़ करें, सरकारी योजनाओं की जानकारी देने में समस्या आ रही है। कृपया कुछ देर बाद फिर से कोशिश करें।"
        else:
            return "Sorry, there's an issue providing government scheme information. Please try again later."
    
    async def get_scheme_recommendations(self, user_id: str) -> Dict[str, Any]:
        """Get personalized scheme recommendations for a user"""
        # Mock user context - in production would fetch from database
        user_context = {
            "user_id": user_id,
            "land_area": 5.0,
            "location": "Punjab"
        }
        
        relevant_schemes = []
        for scheme_id, scheme_data in self.schemes.items():
            if scheme_data["status"] == "active":
                land_limit = scheme_data.get("land_limit", float('inf'))
                if user_context["land_area"] <= land_limit:
                    relevant_schemes.append({
                        "scheme_id": scheme_id,
                        "name": scheme_data["name"],
                        "amount": scheme_data.get("amount", "Variable"),
                        "eligibility": scheme_data.get("eligibility", [])
                    })
        
        return {
            "user_id": user_id,
            "recommended_schemes": relevant_schemes,
            "total_benefit": sum(scheme.get("amount", 0) for scheme in relevant_schemes if isinstance(scheme.get("amount"), (int, float)))
        }
