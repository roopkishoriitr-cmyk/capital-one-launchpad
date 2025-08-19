import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from loguru import logger
from app.core.config import settings

class FinanceAgent:
    """
    Finance Agent - Handles debt analysis, loan optimization, and financial planning
    for Indian farmers.
    """
    
    def __init__(self):
        self.name = "Finance Agent"
        self.description = "Specialized in debt management, loan optimization, and financial planning"
        self.initialized = False
        
    async def initialize(self):
        """Initialize the finance agent with necessary data and models"""
        try:
            # Load loan schemes, interest rates, and subsidy data
            await self._load_financial_data()
            self.initialized = True
            logger.info("💰 Finance Agent initialized successfully")
        except Exception as e:
            logger.error(f"❌ Error initializing Finance Agent: {e}")
            raise
    
    async def _load_financial_data(self):
        """Load financial data including loan schemes, interest rates, etc."""
        # Comprehensive loan schemes for Punjab farmers
        self.loan_schemes = {
            "crop_loan": {
                "interest_rate": 7.0,
                "max_amount": 300000,
                "tenure": 12,
                "description": "Kharif and Rabi crop loans",
                "eligibility": "All farmers with land ownership",
                "processing_fee": 0.5,
                "collateral": "Crop hypothecation",
                "disbursement": "Within 7 days"
            },
            "equipment_loan": {
                "interest_rate": 8.5,
                "max_amount": 500000,
                "tenure": 36,
                "description": "Farm equipment and machinery loans",
                "eligibility": "Farmers with 2+ years experience",
                "processing_fee": 1.0,
                "collateral": "Equipment hypothecation",
                "disbursement": "Within 15 days"
            },
            "irrigation_loan": {
                "interest_rate": 7.5,
                "max_amount": 200000,
                "tenure": 24,
                "description": "Irrigation system and water management",
                "eligibility": "Farmers with 5+ acres",
                "processing_fee": 0.75,
                "collateral": "Land mortgage",
                "disbursement": "Within 10 days"
            },
            "dairy_loan": {
                "interest_rate": 6.5,
                "max_amount": 1000000,
                "tenure": 60,
                "description": "Dairy farming and livestock loans",
                "eligibility": "Farmers with dairy experience",
                "processing_fee": 1.0,
                "collateral": "Livestock hypothecation",
                "disbursement": "Within 20 days"
            },
            "horticulture_loan": {
                "interest_rate": 6.8,
                "max_amount": 400000,
                "tenure": 48,
                "description": "Fruit and vegetable farming loans",
                "eligibility": "Farmers with horticulture training",
                "processing_fee": 0.8,
                "collateral": "Crop and land",
                "disbursement": "Within 12 days"
            }
        }
        
        # Punjab-specific subsidy schemes
        self.subsidy_schemes = {
            "pm_kisan": {
                "amount": 6000,
                "frequency": "yearly",
                "eligibility": "Small and marginal farmers",
                "application": "Online through PM-KISAN portal",
                "disbursement": "Quarterly installments of ₹2000"
            },
            "fertilizer_subsidy": {
                "amount": 1400,
                "frequency": "per_bag",
                "eligibility": "All farmers",
                "application": "Through authorized dealers",
                "disbursement": "Direct benefit transfer"
            },
            "seed_subsidy": {
                "amount": 500,
                "frequency": "per_quintal",
                "eligibility": "Small farmers",
                "application": "Through agriculture department",
                "disbursement": "Subsidized seed distribution"
            },
            "pesticide_subsidy": {
                "amount": 300,
                "frequency": "per_liter",
                "eligibility": "All farmers",
                "application": "Through authorized centers",
                "disbursement": "Subsidized pesticide distribution"
            },
            "drip_irrigation_subsidy": {
                "amount": 50000,
                "frequency": "one_time",
                "eligibility": "Farmers with 2+ acres",
                "application": "Through agriculture department",
                "disbursement": "After installation verification"
            }
        }
        
        # Punjab-specific banks and their offerings
        self.banks = {
            "punjab_national_bank": {
                "name": "Punjab National Bank",
                "crop_loan_rate": 6.8,
                "max_amount": 350000,
                "processing_time": "5 days",
                "branches": 1200
            },
            "state_bank_of_india": {
                "name": "State Bank of India",
                "crop_loan_rate": 7.0,
                "max_amount": 300000,
                "processing_time": "7 days",
                "branches": 1500
            },
            "punjab_and_sind_bank": {
                "name": "Punjab & Sind Bank",
                "crop_loan_rate": 6.9,
                "max_amount": 320000,
                "processing_time": "6 days",
                "branches": 800
            },
            "cooperative_banks": {
                "name": "Punjab Cooperative Banks",
                "crop_loan_rate": 6.5,
                "max_amount": 250000,
                "processing_time": "3 days",
                "branches": 2000
            }
        }
    
    async def process(self, query: str, user_context: Dict, language: str = "hi") -> str:
        """Process finance-related queries"""
        try:
            # Analyze query type
            query_type = self._analyze_finance_query(query)
            
            if query_type == "debt_forecast":
                return await self._handle_debt_forecast(user_context, language)
            elif query_type == "loan_recommendation":
                return await self._handle_loan_recommendation(user_context, language)
            elif query_type == "subsidy_info":
                return await self._handle_subsidy_info(user_context, language)
            elif query_type == "repayment_strategy":
                return await self._handle_repayment_strategy(user_context, language)
            else:
                return await self._handle_general_finance_query(query, user_context, language)
                
        except Exception as e:
            logger.error(f"❌ Error in Finance Agent: {e}")
            return self._get_error_response(language)
    
    def _analyze_finance_query(self, query: str) -> str:
        """Analyze the type of finance query"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["debt", "karz", "udhar", "qarz", "free", "mukt"]):
            return "debt_forecast"
        elif any(word in query_lower for word in ["loan", "credit", "karz", "udhar"]):
            return "loan_recommendation"
        elif any(word in query_lower for word in ["subsidy", "yojana", "scheme", "help"]):
            return "subsidy_info"
        elif any(word in query_lower for word in ["repay", "payment", "installment", "kisht"]):
            return "repayment_strategy"
        else:
            return "general"
    
    async def _handle_debt_forecast(self, user_context: Dict, language: str) -> str:
        """Handle debt freedom forecast queries"""
        current_debt = sum(loan.get("remaining", 0) for loan in user_context.get("current_loans", []))
        
        if current_debt == 0:
            return self._get_no_debt_response(language)
        
        # Calculate debt freedom timeline
        forecast = await self._calculate_debt_forecast(user_context)
        
        if language == "hi":
            return f"""💰 आपका कर्ज मुक्ति पूर्वानुमान:

📊 वर्तमान कर्ज: ₹{current_debt:,}
📅 अनुमानित कर्ज मुक्ति: {forecast['debt_free_date']}
💵 मासिक भुगतान आवश्यक: ₹{forecast['monthly_payment']:,}

🌱 सुझाव: {forecast['recommendations']}

🎯 लक्ष्य: {forecast['motivational_message']}"""
        else:
            return f"""💰 Your Debt Freedom Forecast:

📊 Current Debt: ₹{current_debt:,}
📅 Estimated Debt-Free Date: {forecast['debt_free_date']}
💵 Monthly Payment Needed: ₹{forecast['monthly_payment']:,}

🌱 Recommendations: {forecast['recommendations']}

🎯 Goal: {forecast['motivational_message']}"""
    
    async def _calculate_debt_forecast(self, user_context: Dict) -> Dict[str, Any]:
        """Calculate debt freedom forecast based on user context"""
        current_debt = sum(loan.get("remaining", 0) for loan in user_context.get("current_loans", []))
        monthly_income = 15000  # Mock - would come from crop yields and market prices
        
        # Simple calculation - in production would use more sophisticated models
        monthly_payment = min(monthly_income * 0.4, current_debt * 0.1)  # 40% of income or 10% of debt
        months_to_freedom = current_debt / monthly_payment if monthly_payment > 0 else 0
        
        debt_free_date = datetime.now() + timedelta(days=months_to_freedom * 30)
        
        recommendations = [
            "उच्च मूल्य वाली फसलें उगाएं (बाजरा, दालें)",
            "सरकारी सब्सिडी का लाभ उठाएं",
            "मंडी में बेहतर दाम के लिए समय चुनें"
        ]
        
        motivational_messages = [
            "हर फसल आपको कर्ज मुक्ति की ओर ले जाती है",
            "आपका कठिन परिश्रम आपको स्वतंत्र बनाएगा",
            "कर्ज का बोझ जल्द ही उतर जाएगा"
        ]
        
        return {
            "debt_free_date": debt_free_date.strftime("%B %Y"),
            "monthly_payment": int(monthly_payment),
            "recommendations": " | ".join(recommendations),
            "motivational_message": motivational_messages[0]
        }
    
    async def _handle_loan_recommendation(self, user_context: Dict, language: str) -> str:
        """Handle loan recommendation queries"""
        land_area = user_context.get("land_area", 0)
        current_loans = user_context.get("current_loans", [])
        
        # Recommend appropriate loan schemes
        recommendations = []
        
        if land_area > 0:
            crop_loan_amount = min(land_area * 50000, 300000)  # ₹50k per acre, max ₹3L
            recommendations.append(f"फसल ऋण: ₹{crop_loan_amount:,} (7% ब्याज)")
        
        if not any(loan.get("type") == "equipment" for loan in current_loans):
            recommendations.append("उपकरण ऋण: ₹2,00,000 (8.5% ब्याज)")
        
        if language == "hi":
            return f"""💳 आपके लिए ऋण सिफारिशें:

{chr(10).join(f"• {rec}" for rec in recommendations)}

📋 आवेदन के लिए आवश्यक दस्तावेज:
• आधार कार्ड
• भूमि के कागजात
• बैंक खाता
• फोटो

🏦 निकटतम बैंक या कृषि सहकारी समिति से संपर्क करें।"""
        else:
            return f"""💳 Loan Recommendations for You:

{chr(10).join(f"• {rec}" for rec in recommendations)}

📋 Documents Required:
• Aadhaar Card
• Land Documents
• Bank Account
• Photos

🏦 Contact nearest bank or agricultural cooperative society."""
    
    async def _handle_subsidy_info(self, user_context: Dict, language: str) -> str:
        """Handle subsidy information queries"""
        subsidies = []
        
        for scheme_name, scheme_data in self.subsidy_schemes.items():
            if scheme_name == "pm_kisan":
                subsidies.append(f"PM-KISAN: ₹{scheme_data['amount']:,} सालाना")
            elif scheme_name == "fertilizer_subsidy":
                subsidies.append(f"खाद सब्सिडी: ₹{scheme_data['amount']:,} प्रति बोरी")
            elif scheme_name == "seed_subsidy":
                subsidies.append(f"बीज सब्सिडी: ₹{scheme_data['amount']:,} प्रति क्विंटल")
        
        if language == "hi":
            return f"""🏛️ आपके लिए उपलब्ध सरकारी योजनाएं:

{chr(10).join(f"• {subsidy}" for subsidy in subsidies)}

📞 आवेदन के लिए:
• कृषि विभाग कार्यालय
• बैंक शाखा
• ऑनलाइन पोर्टल

✅ सभी छोटे और सीमांत किसानों के लिए उपलब्ध"""
        else:
            return f"""🏛️ Government Schemes Available for You:

{chr(10).join(f"• {subsidy}" for subsidy in subsidies)}

📞 To Apply:
• Agriculture Department Office
• Bank Branch
• Online Portal

✅ Available for all small and marginal farmers"""
    
    async def _handle_repayment_strategy(self, user_context: Dict, language: str) -> str:
        """Handle repayment strategy queries"""
        current_loans = user_context.get("current_loans", [])
        
        if not current_loans:
            return self._get_no_debt_response(language)
        
        strategies = [
            "फसल बिक्री से प्राप्त राशि का 60% कर्ज चुकाने में लगाएं",
            "मंडी में उच्च दाम पर बेचने का इंतजार करें",
            "सरकारी सब्सिडी का लाभ उठाकर कर्ज चुकाएं",
            "अगली फसल के लिए कम लागत वाली फसलें चुनें"
        ]
        
        if language == "hi":
            return f"""💡 कर्ज चुकाने की रणनीति:

{chr(10).join(f"• {strategy}" for strategy in strategies)}

📊 प्राथमिकता क्रम:
1. उच्च ब्याज वाले कर्ज पहले चुकाएं
2. फसल बिक्री से तुरंत भुगतान करें
3. नई फसल के लिए बचत रखें

🎯 लक्ष्य: अगले 2 साल में कर्ज मुक्त हो जाएं"""
        else:
            return f"""💡 Repayment Strategy:

{chr(10).join(f"• {strategy}" for strategy in strategies)}

📊 Priority Order:
1. Pay high-interest loans first
2. Make immediate payment from crop sales
3. Save for next crop season

🎯 Goal: Become debt-free in next 2 years"""
    
    async def _handle_general_finance_query(self, query: str, user_context: Dict, language: str) -> str:
        """Handle general finance queries"""
        if language == "hi":
            return """💰 वित्तीय सलाह:

• अपनी फसल का रिकॉर्ड रखें
• बाजार के दामों पर नजर रखें
• सरकारी योजनाओं का लाभ उठाएं
• कर्ज को समझदारी से प्रबंधित करें

क्या आप कर्ज, सब्सिडी या फसल बिक्री के बारे में जानना चाहते हैं?"""
        else:
            return """💰 Financial Advice:

• Keep records of your crops
• Monitor market prices
• Avail government schemes
• Manage loans wisely

Do you want to know about loans, subsidies, or crop sales?"""
    
    def _get_no_debt_response(self, language: str) -> str:
        """Response when user has no debt"""
        if language == "hi":
            return "🎉 बधाई हो! आप कर्ज मुक्त हैं। अपनी बचत को स्मार्ट तरीके से निवेश करें।"
        else:
            return "🎉 Congratulations! You are debt-free. Invest your savings wisely."
    
    def _get_error_response(self, language: str) -> str:
        """Error response in appropriate language"""
        if language == "hi":
            return "माफ़ करें, वित्तीय सलाह देने में समस्या आ रही है। कृपया कुछ देर बाद फिर से कोशिश करें।"
        else:
            return "Sorry, there's an issue providing financial advice. Please try again later."
    
    async def get_debt_forecast(self, user_id: str) -> Dict[str, Any]:
        """Get detailed debt forecast for a user"""
        # Mock user context - in production would fetch from database
        user_context = {
            "user_id": user_id,
            "current_loans": [
                {"amount": 50000, "interest_rate": 7.5, "remaining": 35000, "type": "crop_loan"}
            ],
            "land_area": 5.0,
            "location": "Punjab"
        }
        
        forecast = await self._calculate_debt_forecast(user_context)
        return {
            "user_id": user_id,
            "current_debt": 35000,
            "forecast": forecast,
            "recommendations": [
                "Grow high-value crops like pulses and millets",
                "Apply for PM-KISAN subsidy",
                "Time your crop sales for better prices"
            ]
        }
