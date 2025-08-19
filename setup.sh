#!/bin/bash

# KrishiSampann Setup Script
# This script sets up the complete KrishiSampann application

set -e

echo "🌾 Welcome to KrishiSampann Setup!"
echo "=================================="
echo "Where Crops Meet Capital"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}[SETUP]${NC} $1"
}

# Check if Docker is installed
check_docker() {
    print_header "Checking Docker installation..."
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        echo "Visit: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        echo "Visit: https://docs.docker.com/compose/install/"
        exit 1
    fi
    
    print_status "Docker and Docker Compose are installed."
}

# Check if Node.js is installed
check_nodejs() {
    print_header "Checking Node.js installation..."
    if ! command -v node &> /dev/null; then
        print_warning "Node.js is not installed. Installing via Docker instead."
        return 1
    fi
    
    NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -lt 16 ]; then
        print_warning "Node.js version is too old. Please upgrade to Node.js 16 or higher."
        return 1
    fi
    
    print_status "Node.js is installed and compatible."
    return 0
}

# Check if Python is installed
check_python() {
    print_header "Checking Python installation..."
    if ! command -v python3 &> /dev/null; then
        print_warning "Python 3 is not installed. Installing via Docker instead."
        return 1
    fi
    
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    if [ "$(echo "$PYTHON_VERSION < 3.9" | bc -l)" -eq 1 ]; then
        print_warning "Python version is too old. Please upgrade to Python 3.9 or higher."
        return 1
    fi
    
    print_status "Python 3 is installed and compatible."
    return 0
}

# Create environment file
setup_environment() {
    print_header "Setting up environment configuration..."
    
    if [ ! -f .env ]; then
        cp env.example .env
        print_status "Created .env file from template."
        print_warning "Please edit .env file with your API keys and configuration."
    else
        print_status ".env file already exists."
    fi
}

# Setup frontend
setup_frontend() {
    print_header "Setting up frontend..."
    
    if check_nodejs; then
        cd frontend
        print_status "Installing frontend dependencies..."
        npm install --legacy-peer-deps
        
        print_status "Building frontend..."
        npm run build
        cd ..
    else
        print_status "Frontend will be built via Docker."
    fi
}

# Setup backend
setup_backend() {
    print_header "Setting up backend..."
    
    if check_python; then
        cd backend
        print_status "Creating Python virtual environment..."
        python3 -m venv venv
        source venv/bin/activate
        
        print_status "Installing backend dependencies..."
        pip install -r requirements.txt
        
        cd ..
    else
        print_status "Backend will be installed via Docker."
    fi
}

# Start services with Docker
start_services() {
    print_header "Starting services with Docker Compose..."
    
    print_status "Building and starting all services..."
    docker-compose up -d --build
    
    print_status "Waiting for services to be ready..."
    sleep 30
    
    # Check if services are running
    if docker-compose ps | grep -q "Up"; then
        print_status "All services are running successfully!"
    else
        print_error "Some services failed to start. Check logs with: docker-compose logs"
        exit 1
    fi
}

# Display setup completion
show_completion() {
    echo ""
    echo "🎉 KrishiSampann Setup Complete!"
    echo "================================"
    echo ""
    echo "Services are now running:"
    echo "  🌐 Frontend: http://localhost:3000"
    echo "  🔧 Backend API: http://localhost:8000"
    echo "  📊 API Documentation: http://localhost:8000/docs"
    echo "  🗄️  Database: localhost:5432"
    echo "  🔍 Vector Database: localhost:6333"
    echo "  📦 Redis: localhost:6379"
    echo ""
    echo "Useful commands:"
    echo "  📋 View logs: docker-compose logs -f"
    echo "  🛑 Stop services: docker-compose down"
    echo "  🔄 Restart services: docker-compose restart"
    echo "  🧹 Clean up: docker-compose down -v"
    echo ""
    echo "Next steps:"
    echo "  1. Open http://localhost:3000 in your browser"
    echo "  2. Configure your API keys in the .env file"
    echo "  3. Start chatting with KrishiSampann!"
    echo ""
    echo "For support, visit: https://github.com/your-repo/krishisampann"
}

# Main setup function
main() {
    print_header "Starting KrishiSampann setup..."
    
    check_docker
    setup_environment
    setup_frontend
    setup_backend
    start_services
    show_completion
}

# Run main function
main "$@"
