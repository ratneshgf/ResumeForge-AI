#!/bin/bash

# ResumeForge AI - Quick Deployment Script
# This script helps you deploy the application quickly

set -e

echo "🚀 ResumeForge AI Deployment Script"
echo "======================================"
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from backend/.env.example..."
    cp backend/.env.example .env
    echo "✅ Created .env file"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file and add your actual API keys before continuing!"
    echo "   - GEMINI_API_KEY"
    echo "   - RAZORPAY_KEY_ID"
    echo "   - RAZORPAY_KEY_SECRET"
    echo ""
    read -p "Have you updated the .env file with your keys? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Deployment cancelled. Please update .env and run again."
        exit 1
    fi
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first:"
    echo "   https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first:"
    echo "   https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose found"
echo ""

# Ask deployment type
echo "Select deployment option:"
echo "1) Production (Docker Compose)"
echo "2) Development (Local)"
echo ""
read -p "Enter choice (1 or 2): " choice

case $choice in
    1)
        echo ""
        echo "🏭 Starting Production Deployment..."
        echo ""
        
        # Build and start containers
        echo "📦 Building Docker images..."
        docker-compose build
        
        echo ""
        echo "🚀 Starting containers..."
        docker-compose up -d
        
        echo ""
        echo "✅ Deployment complete!"
        echo ""
        echo "🌐 Your application is running:"
        echo "   - Frontend: http://localhost:3000"
        echo "   - Backend:  http://localhost:8000"
        echo "   - API Docs: http://localhost:8000/docs"
        echo ""
        echo "📊 Check status: docker-compose ps"
        echo "📜 View logs:    docker-compose logs -f"
        echo "🛑 Stop:         docker-compose down"
        ;;
        
    2)
        echo ""
        echo "💻 Starting Development Setup..."
        echo ""
        
        # Backend setup
        echo "🐍 Setting up backend..."
        cd backend
        
        if [ ! -d "venv" ]; then
            echo "Creating virtual environment..."
            python3 -m venv venv
        fi
        
        echo "Installing backend dependencies..."
        source venv/bin/activate
        pip install -r requirements.txt
        
        # Copy .env if not exists
        if [ ! -f ".env" ]; then
            cp ../.env .env
        fi
        
        echo ""
        echo "✅ Backend setup complete!"
        echo "   To start: cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
        
        cd ..
        
        # Frontend setup
        echo ""
        echo "📦 Setting up frontend..."
        cd frontend
        
        if [ ! -d "node_modules" ]; then
            echo "Installing frontend dependencies..."
            npm install
        fi
        
        echo ""
        echo "✅ Frontend setup complete!"
        echo "   To start: cd frontend && npm run dev"
        
        cd ..
        
        echo ""
        echo "✅ Development setup complete!"
        echo ""
        echo "To start development:"
        echo "1. Terminal 1: cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
        echo "2. Terminal 2: cd frontend && npm run dev"
        ;;
        
    *)
        echo "❌ Invalid choice. Exiting."
        exit 1
        ;;
esac

echo ""
echo "🎉 All done! Happy coding!"
