# HiAnime Docker Setup Guide

This guide explains how to set up and run the complete HiAnime application (backend + frontend) using Docker Compose.

## 🏗️ Architecture

The Docker setup includes:
- **Backend**: Django REST API with gunicorn
- **Frontend**: Next.js application
- **Cache**: Redis for caching
- **Proxy**: Nginx (optional) for reverse proxy

## 📋 Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (v2, not v1)
- Git (for cloning repositories)

## 🚀 Quick Start

### Option 1: Production Build

```bash
# Clone the repositories
git clone https://github.com/debasish-panda-22/hianime_api.git
cd hianime_api

# Run the build script
./build_and_run.sh
```

This will:
- Build both backend and frontend Docker images
- Create necessary environment files
- Start all services
- Provide access URLs

### Option 2: Development Environment

```bash
# Clone the repositories
git clone https://github.com/debasish-panda-22/hianime_api.git
cd hianime_api

# Run the development script
./dev.sh
```

This will:
- Build development Docker images
- Start services with hot reload enabled
- Set up development environment variables

## 🐳 Docker Compose Files

### Production: `docker-compose.yml`

```yaml
services:
  backend:      # Django production server
  frontend:     # Next.js production build
  redis:        # Redis cache
  nginx:        # Reverse proxy (optional)
```

### Development: `docker-compose.dev.yml`

```yaml
services:
  backend:      # Django development server
  frontend:     # Next.js development server
  redis:        # Redis cache
```

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```env
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
```

#### Frontend (.env.local)
```env
# HiAnime Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# For production, use your deployed backend URL
# NEXT_PUBLIC_API_URL=https://your-backend-domain.com/api/v1
```

## 🌐 Access URLs

Once running, the application will be available at:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/v1/schema/swagger-ui/
- **ReDoc Documentation**: http://localhost:8000/api/v1/schema/redoc/

## 📝 Available Commands

### Production Commands

```bash
# Build and start all services
./build_and_run.sh

# Manual control
docker compose up -d                    # Start all services
docker compose down                    # Stop all services
docker compose restart                 # Restart all services
docker compose logs -f                 # View all logs
docker compose build                   # Rebuild images
docker compose ps                      # List running containers
```

### Development Commands

```bash
# Start development environment
./dev.sh

# Manual control
docker compose -f docker-compose.dev.yml up -d
docker compose -f docker-compose.dev.yml down
docker compose -f docker-compose.dev.yml logs -f backend
docker compose -f docker-compose.dev.yml logs -f frontend
```

### Service-specific Commands

```bash
# Backend only
docker compose up -d backend redis
docker compose logs backend

# Frontend only
docker compose up -d frontend
docker compose logs frontend

# Redis only
docker compose up -d redis
docker compose logs redis

# Nginx proxy (production only)
docker compose --profile proxy up -d nginx
```

## 🔧 Custom Dockerfiles

### Backend Production: `Dockerfile`
- Multi-stage build
- Uses gunicorn for production serving
- Optimized for production

### Backend Development: `Dockerfile.dev`
- Single-stage build
- Uses Django development server
- Includes development dependencies

### Frontend Production: `Dockerfile.frontend`
- Multi-stage build
- Standalone output for production
- Uses Node.js Alpine image

### Frontend Development: `Dockerfile.dev.frontend`
- Single-stage build
- Includes all dependencies
- Uses development server

## 🌐 Network Configuration

The services communicate via a custom Docker network:

```yaml
networks:
  hianime-network:
    driver: bridge
```

### Service Communication

- **Frontend → Backend**: `http://backend:8000`
- **Backend → Redis**: `http://redis:6379`
- **Nginx → Frontend**: `http://frontend:3000`
- **Nginx → Backend**: `http://backend:8000`

## 📊 Volume Management

### Named Volumes
```yaml
volumes:
  redis_data:    # Persistent Redis data
```

### Bind Mounts (Development)
```yaml
volumes:
  - .:/app              # Live code mounting
  - /app/node_modules   # Prevent node_modules override
  - /app/.next         # Prevent .next override
```

## 🔒 Security Features

### Production Security
- Non-root user for frontend
- Security headers in Nginx
- Rate limiting
- CORS configuration
- Environment variable isolation

### Development Security
- Development-only settings
- Localhost restrictions
- Debug mode enabled

## 🚀 Deployment

### Production Deployment

1. **Prepare Environment**:
   ```bash
   # Set production environment variables
   export SECRET_KEY="your-production-secret-key"
   export DEBUG=False
   ```

2. **Build and Deploy**:
   ```bash
   ./build_and_run.sh
   ```

3. **Set Up Domain**:
   - Configure DNS to point to your server
   - Set up SSL certificates (Let's Encrypt)
   - Update ALLOWED_HOSTS and CORS_ALLOWED_ORIGINS

### Development Deployment

```bash
# Quick development setup
./dev.sh

# Access services
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Port Conflicts
```bash
# Check what's using the ports
lsof -i :3000
lsof -i :8000
lsof -i :6379

# Kill processes if needed
kill -9 <PID>
```

#### 2. Build Failures
```bash
# Clean build
docker compose down
docker system prune -a
docker compose build --no-cache

# Check disk space
docker system df
```

#### 3. Container Issues
```bash
# View container logs
docker compose logs backend
docker compose logs frontend
docker compose logs redis

# Restart specific service
docker compose restart backend
docker compose restart frontend

# Enter container for debugging
docker compose exec backend bash
docker compose exec frontend sh
```

#### 4. Network Issues
```bash
# Check network connectivity
docker compose exec backend ping redis
docker compose exec frontend ping backend

# Inspect network
docker network inspect hianime_hianime-network
```

#### 5. Permission Issues
```bash
# Fix file permissions
sudo chown -R $USER:$USER .
sudo chmod -R 755 .

# Clean up Docker
docker system prune -a
docker volume prune
```

### Debug Commands

```bash
# Check container status
docker compose ps

# View resource usage
docker stats

# Inspect container
docker compose inspect backend

# Check environment variables
docker compose exec backend env
docker compose exec frontend env
```

## 📚 Advanced Usage

### Custom Configuration

1. **Custom Ports**: Modify the `ports` section in docker-compose.yml
2. **Custom Networks**: Add additional networks for isolation
3. **Resource Limits**: Add resource constraints to services
4. **Health Checks**: Add health check configurations

### Scaling Services

```bash
# Scale backend (for load balancing)
docker compose up -d --scale backend=3

# Note: Ensure your backend supports multiple instances
```

### Logging Configuration

```yaml
# Add to docker-compose.yml for better logging
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

## 🎯 Best Practices

### Development
- Use development compose file for development
- Mount code volumes for hot reload
- Keep development and production configurations separate

### Production
- Use specific image tags (not 'latest')
- Implement health checks
- Use reverse proxy (Nginx)
- Set up proper logging and monitoring
- Use environment variables for configuration

### Security
- Use non-root users
- Keep secrets in environment variables
- Implement proper CORS configuration
- Use rate limiting
- Regular security updates

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review container logs: `docker compose logs`
3. Check network connectivity between containers
4. Verify environment variables
5. Ensure all prerequisites are met

For additional support:
- Check the main project README
- Open an issue on GitHub
- Review Docker and Docker Compose documentation