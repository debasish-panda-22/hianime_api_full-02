#!/bin/bash

# HiAnime Development Script

echo "🚀 Starting HiAnime Development Environment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "   Note: This script uses 'docker compose' (v2), not 'docker-compose' (v1)"
    exit 1
fi

# Create development environment files
echo "🔧 Setting up development environment files..."

# Backend .env
if [ ! -f ".env" ]; then
    echo "📝 Creating .env for backend..."
    cat > .env << EOF
# Django settings (Development)
SECRET_KEY=dev-secret-key-not-for-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,frontend

# CORS settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Cache settings
REDIS_URL=redis://redis:6379/0
CACHE_TIMEOUT=3600

# Rate limiting
RATELIMIT_ENABLE=True
RATELIMIT_RATE=100/h

# Anime API configuration
ANIME_API_BASE_URL=https://hianime.bz
ANIME_API_BASE_URL_V2=https://kaido.to
ANIME_API_PROVIDERS=https://megacloud.club
EOF
fi

# Frontend .env.local
if [ ! -f "../.env.local" ]; then
    echo "📝 Creating .env.local for frontend..."
    cat > "../.env.local" << EOF
# HiAnime Backend API URL (Development)
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
EOF
fi

echo "✅ Environment files created"

# Build development images
echo "🔨 Building development images..."
docker compose -f docker-compose.dev.yml build

if [ $? -eq 0 ]; then
    echo "✅ Development images built successfully!"
else
    echo "❌ Failed to build development images."
    exit 1
fi

# Start development containers
echo "🚀 Starting development containers..."
docker compose -f docker-compose.dev.yml up -d

if [ $? -eq 0 ]; then
    echo "✅ Development containers started successfully!"
    echo ""
    echo "🌐 Frontend: http://localhost:3000"
    echo "🔧 Backend API: http://localhost:8000"
    echo "📚 API Docs: http://localhost:8000/api/v1/schema/swagger-ui/"
    echo ""
    echo "📋 Development Tips:"
    echo "   • Code changes are automatically reflected (hot reload)"
    echo "   • Backend logs: docker compose -f docker-compose.dev.yml logs -f backend"
    echo "   • Frontend logs: docker compose -f docker-compose.dev.yml logs -f frontend"
    echo "   • Stop containers: docker compose -f docker-compose.dev.yml down"
    echo "   • Restart containers: docker compose -f docker-compose.dev.yml restart"
    echo ""
    echo "🔧 For production build, use: ./build_and_run.sh"
else
    echo "❌ Failed to start development containers."
    exit 1
fi