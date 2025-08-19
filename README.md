# 🌾 KrishiSampann - AI-Powered Agricultural Decision Support System

**Where Crops Meet Capital** - An intelligent voice-first platform empowering Indian farmers with AI-driven financial and agronomic guidance.

## 🚀 Quick Start

### Prerequisites

- **Docker & Docker Compose** (required)
- **OpenAI API Key** (required for voice AI functionality)
- **Node.js 18+** (for development)
- **Python 3.9+** (for development)

### 🔑 OpenAI API Key Setup (REQUIRED)

**⚠️ IMPORTANT: You MUST have a valid OpenAI API key to use the voice AI features.**

1. **Get OpenAI API Key:**
   - Visit [OpenAI Platform](https://platform.openai.com/api-keys)
   - Create a new API key
   - Ensure you have credits in your OpenAI account

2. **Set Environment Variable:**
   ```bash
   # Option 1: Export in terminal
   export OPENAI_API_KEY="your-actual-openai-api-key-here"
   
   # Option 2: Create .env file
   cp env.example .env
   # Edit .env and replace with your actual API key
   OPENAI_API_KEY=your-actual-openai-api-key-here
   ```

3. **Verify API Key:**
   ```bash
   # Test your API key
   curl -H "Authorization: Bearer $OPENAI_API_KEY" https://api.openai.com/v1/models
   ```

### 🏃‍♂️ Start the Application

1. **Clone and Navigate:**
   ```bash
   git clone <repository-url>
   cd capital-one-hackathon
   ```

2. **Start All Services:**
   ```bash
   docker-compose up -d
   ```

3. **Verify Services:**
   ```bash
   docker-compose ps
   ```

4. **Access the Application:**
   - **Frontend**: http://localhost:3000
   - **Backend API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs

### 🔧 Development Setup

1. **Install Dependencies:**
   ```bash
   # Frontend
   cd frontend
   npm install
   
   # Backend
   cd ../backend
   pip install -r requirements.txt
   ```

2. **Start Development Servers:**
   ```bash
   # Frontend (in frontend directory)
   npm start
   
   # Backend (in backend directory)
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## 🏗️ Architecture

### Core Components

- **🎤 KrishiMitra AI**: OpenAI-powered voice assistant
- **🤖 Multi-Agent System**: Specialized AI agents for different domains
- **🌐 Voice-First Interface**: Real-time voice interaction
- **📊 Financial Advisory**: Loan matching and debt management
- **🌱 Agronomy Support**: Crop recommendations and techniques

### Technology Stack

- **Frontend**: React + TypeScript + Tailwind CSS
- **Backend**: FastAPI + Python
- **AI/ML**: OpenAI GPT-4, OpenAI Realtime API
- **Database**: PostgreSQL + Qdrant (Vector DB)
- **Voice**: OpenAI Realtime API (Voice-to-Voice)
- **Containerization**: Docker + Docker Compose

## 🎯 Key Features

### 🌾 Agricultural Intelligence
- **Crop Recommendations**: AI-powered crop selection based on soil, climate, and market
- **Agronomy Techniques**: Best practices for yield optimization
- **Disease Detection**: Early warning systems for crop diseases
- **Weather Integration**: IMD weather data for planning

### 💰 Financial Advisory
- **Loan Matching**: Smart crop-loan recommendations
- **Debt Management**: Personalized debt freedom pathways
- **Government Schemes**: PM-KISAN and state-specific subsidies
- **Market Intelligence**: Real-time mandi prices and trends

### 🎤 Voice-First Interface
- **Multilingual Support**: Hindi, English, and regional languages
- **Natural Conversations**: Voice-to-voice AI interaction
- **Real-time Processing**: Low-latency voice recognition
- **Accessibility**: Designed for farmers with limited digital literacy

### 🤖 AI Agents

1. **Finance Agent**: Loan schemes, debt management, financial planning
2. **Agronomy Agent**: Crop selection, farming techniques, soil health
3. **Market Agent**: Price trends, selling strategies, demand forecasting
4. **Policy Agent**: Government schemes, subsidies, application processes
5. **Risk Agent**: Weather risks, pest management, climate adaptation

## 📊 Data Sources

- **Weather Data**: IMD Weather API
- **Market Prices**: e-NAM Mandi Prices
- **Government Schemes**: PM-Kisan & State Portals
- **Soil Health**: Soil Health Card Scheme
- **Crop Diseases**: Public Agricultural Databases

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Required: OpenAI API Key
OPENAI_API_KEY=your-openai-api-key-here

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/krishisampann
QDRANT_URL=http://localhost:6335

# External APIs
OPENWEATHER_API_KEY=your-openweather-api-key
DATA_GOV_API_KEY=your-datagov-api-key

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET=your-jwt-secret-here

# Application Settings
DEBUG=True
ENVIRONMENT=development
```

### Service Configuration

**Frontend (Port 3000):**
- React development server
- Hot reload enabled
- PWA support

**Backend (Port 8000):**
- FastAPI application
- WebSocket support
- CORS enabled

**Database Services:**
- PostgreSQL (Port 5432)
- Qdrant Vector DB (Port 6335)
- Redis Cache (Port 6379)

## 🚀 Deployment

### Production Setup

1. **Build Production Images:**
   ```bash
   docker-compose -f docker-compose.prod.yml build
   ```

2. **Set Production Environment:**
   ```bash
   export ENVIRONMENT=production
   export DEBUG=False
   ```

3. **Deploy:**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

### Environment-Specific Configs

- **Development**: `docker-compose.yml`
- **Production**: `docker-compose.prod.yml`
- **Testing**: `docker-compose.test.yml`

## 🧪 Testing

### API Testing
```bash
# Test backend health
curl http://localhost:8000/health

# Test OpenAI integration
curl -X POST http://localhost:8000/api/v1/voice/realtime/session \
  -H "Content-Type: application/json" \
  -d '{"voice": "alloy", "language": "hi"}'
```

### Frontend Testing
```bash
cd frontend
npm test
npm run build
```

## 📈 Monitoring & Logs

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Health Checks
```bash
# Backend health
curl http://localhost:8000/health

# Database connectivity
docker-compose exec backend python -c "from app.core.database import engine; print('DB OK')"
```

## 🔍 Troubleshooting

### Common Issues

1. **OpenAI API Key Error:**
   ```bash
   # Check if API key is set
   echo $OPENAI_API_KEY
   
   # Test API key validity
   curl -H "Authorization: Bearer $OPENAI_API_KEY" https://api.openai.com/v1/models
   ```

2. **Port Conflicts:**
   ```bash
   # Check what's using the ports
   lsof -i :3000
   lsof -i :8000
   lsof -i :5432
   ```

3. **Docker Issues:**
   ```bash
   # Restart Docker services
   docker-compose down
   docker-compose up -d
   
   # Clean up containers
   docker-compose down -v
   docker system prune -f
   ```

4. **Database Connection Issues:**
   ```bash
   # Check database status
   docker-compose exec postgres pg_isready
   
   # Reset database
   docker-compose down -v
   docker-compose up -d postgres
   ```

### Performance Optimization

1. **Enable GPU Support** (if available):
   ```yaml
   # In docker-compose.yml
   services:
     backend:
       deploy:
         resources:
           reservations:
             devices:
               - driver: nvidia
                 count: 1
                 capabilities: [gpu]
   ```

2. **Memory Optimization:**
   ```bash
   # Increase Docker memory limit
   # Docker Desktop → Settings → Resources → Memory: 8GB+
   ```

## 🤝 Contributing

### Development Workflow

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Make changes and test**
4. **Commit changes**: `git commit -m 'Add amazing feature'`
5. **Push to branch**: `git push origin feature/amazing-feature`
6. **Create Pull Request**

### Code Standards

- **Python**: Black, flake8, mypy
- **TypeScript**: ESLint, Prettier
- **Git**: Conventional commits

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for GPT-4 and Realtime API
- **Indian Meteorological Department** for weather data
- **e-NAM** for market price data
- **Government of India** for agricultural schemes data

## 📞 Support

- **Documentation**: [Wiki](link-to-wiki)
- **Issues**: [GitHub Issues](link-to-issues)
- **Discussions**: [GitHub Discussions](link-to-discussions)

---

**🌾 Built with ❤️ for Indian Farmers**
