#!/bin/bash

# HiAnime Full Stack - Build and Run Script (Backend + Frontend)

echo "🚀 Building HiAnime Full Stack Application..."

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

# Function to create .env file
create_env_file() {
    local env_file="$1"
    local env_example="$2"
    local service_name="$3"
    
    if [ ! -f "$env_file" ]; then
        if [ -f "$env_example" ]; then
            echo "📝 Creating $env_file for $service_name from template..."
            cp "$env_example" "$env_file"
            echo "✅ $env_file created. Please edit it with your configuration."
        else
            echo "📝 Creating $env_file for $service_name with default values..."
            case $service_name in
                "backend")
                    cat > "$env_file" << EOF
# Django settings
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=False
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
                    ;;
                "frontend")
                    cat > "$env_file" << EOF
# HiAnime Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# For production, use your deployed backend URL
# NEXT_PUBLIC_API_URL=https://your-backend-domain.com/api/v1
EOF
                    ;;
            esac
            echo "✅ $env_file created with default values. Please edit it with your configuration."
        fi
    else
        echo "✅ $env_file already exists for $service_name"
    fi
}

# Create environment files
echo "🔧 Setting up environment files..."
create_env_file ".env" ".env.example" "backend"
create_env_file "../.env.local" "../.env.local.example" "frontend"

# Build Docker images
echo "🔨 Building Docker images..."

# Build backend
echo "📦 Building backend image..."
docker compose build backend

if [ $? -eq 0 ]; then
    echo "✅ Backend image built successfully!"
else
    echo "❌ Failed to build backend image."
    exit 1
fi

# Build frontend
echo "📦 Building frontend image..."
docker compose build frontend

if [ $? -eq 0 ]; then
    echo "✅ Frontend image built successfully!"
else
    echo "❌ Failed to build frontend image."
    exit 1
fi

# Ask if user wants to run the containers
echo ""
read -p "🏃 Do you want to run the containers now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 Starting containers with Docker Compose..."
    docker compose up -d
    
    if [ $? -eq 0 ]; then
        echo "✅ Containers started successfully!"
        echo ""
        echo "🌐 Frontend is available at: http://localhost:3000"
        echo "🔧 Backend API is available at: http://localhost:8000"
        echo "📚 API Documentation: http://localhost:8000/api/v1/schema/swagger-ui/"
        echo "🔍 ReDoc Documentation: http://localhost:8000/api/v1/schema/redoc/"
        echo ""
        echo "🛑 To stop the containers, run: docker compose down"
        echo "📊 To view logs, run: docker compose logs -f"
        echo "🔄 To restart containers, run: docker compose restart"
        echo ""
        echo "💡 Tip: Use 'docker compose logs [service]' to view logs for a specific service"
        echo "   Example: docker compose logs backend"
        echo "   Example: docker compose logs frontend"
        echo ""
        echo "🔧 For development, you might want to run services separately:"
        echo "   Backend only: docker compose up -d backend redis"
        echo "   Frontend only: docker compose up -d frontend"
    else
        echo "❌ Failed to start containers."
        echo "💡 Try running: docker compose logs to see what went wrong"
        exit 1
    fi
else
    echo "👍 Build complete! You can run the containers manually with:"
    echo "   docker compose up -d"
    echo ""
    echo "🎯 Available commands:"
    echo "   docker compose up -d                    # Start all services"
    echo "   docker compose up -d backend redis    # Start backend only"
    echo "   docker compose up -d frontend         # Start frontend only"
    echo "   docker compose down                    # Stop all services"
    echo "   docker compose logs -f                 # View all logs"
    echo "   docker compose logs backend           # View backend logs"
    echo "   docker compose logs frontend           # View frontend logs"
    echo "   docker compose restart                 # Restart all services"
    echo "   docker compose build                   # Rebuild images"
fi

echo ""
echo "🎉 Setup complete! Don't forget to:"
echo "   1. Edit the .env files with your configuration"
echo "   2. Ensure your backend API endpoints are accessible"
echo "   3. Test the frontend-backend connection"
echo ""
echo "📚 For more information, check the SETUP.md file"