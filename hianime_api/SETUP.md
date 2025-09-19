# HiAnime Django API - Setup Guide

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Python 3.11+ (for manual installation)

### Method 1: Using Docker (Recommended)

1. **Clone or download the project**
   ```bash
   # If you have the project files
   cd anime_api_project
   ```

2. **Run the build script**
   ```bash
   chmod +x build_and_run.sh
   ./build_and_run.sh
   ```

3. **Access the API**
   - API Root: http://localhost:8000
   - Swagger UI: http://localhost:8000/api/v1/schema/swagger-ui/
   - ReDoc: http://localhost:8000/api/v1/schema/redoc/

### Method 2: Manual Installation

1. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Run Django migrations**
   ```bash
   python manage.py migrate
   ```

4. **Start the server**
   ```bash
   python manage.py runserver
   ```

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. Port Already in Use
**Error**: `Address already in use` or port conflicts

**Solution**:
```bash
# Find what's using port 8000
lsof -i :8000
# Kill the process
kill -9 <PID>
# Or use a different port
python manage.py runserver 8001
```

#### 2. Docker Build Fails
**Error**: `failed to solve: "/requirements.txt": not found`

**Solution**:
```bash
# Make sure you're in the correct directory
ls -la requirements.txt
# If missing, create it
echo "Django==4.2.7" > requirements.txt
# Add other dependencies from the README
```

#### 3. Permission Issues
**Error**: Permission denied errors

**Solution**:
```bash
# Fix file permissions
sudo chown -R $USER:$USER .
# Make scripts executable
chmod +x build_and_run.sh
```

#### 4. Redis Connection Issues
**Error**: Redis connection refused

**Solution**:
```bash
# Check if Redis is running
docker-compose ps redis
# Restart Redis
docker-compose restart redis
# Or use local memory cache (no Redis)
# Set REDIS_URL= in .env file
```

#### 5. Import Errors
**Error**: ModuleNotFoundError or import errors

**Solution**:
```bash
# Install missing dependencies
pip install -r requirements.txt
# Check Python path
python -c "import sys; print(sys.path)"
# Reinstall packages if needed
pip install --force-reinstall -r requirements.txt
```

#### 6. Docker Issues
**Error**: Docker daemon not running

**Solution**:
```bash
# Start Docker service
sudo systemctl start docker
# Check Docker status
sudo systemctl status docker
# Add user to docker group
sudo usermod -aG docker $USER
# Log out and back in
```

#### 7. Environment Variables Not Loading
**Error**: Settings not loading from .env

**Solution**:
```bash
# Check if .env exists
ls -la .env
# Create from example if missing
cp .env.example .env
# Verify format
cat .env
```

#### 8. CORS Issues
**Error**: CORS policy blocking requests

**Solution**:
```bash
# Check .env CORS settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
# Make sure your frontend URL is included
# Add development URLs if needed
```

### Testing the API

After starting the server, test it with:

```bash
# Test root endpoint
curl http://localhost:8000/api/v1/

# Test homepage
curl http://localhost:8000/api/v1/home/

# Test search
curl "http://localhost:8000/api/v1/search/?keyword=one+piece"

# Run comprehensive test
python test_api.py
```

### Docker Commands

```bash
# Build image
docker buildx build --load -t hianime-django .

# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Clean up
docker system prune -a
docker volume prune
```

### Development Tips

1. **Enable Debug Mode**: Set `DEBUG=True` in .env for development
2. **Use Local Cache**: Comment out Redis URL for local development
3. **Monitor Logs**: Use `docker-compose logs -f web` to see real-time logs
4. **Test Endpoints**: Use the provided test script or curl commands
5. **Check Documentation**: Always check Swagger UI for available endpoints

### Production Deployment

1. **Set Environment Variables**:
   ```env
   DEBUG=False
   SECRET_KEY=your-production-secret-key
   ALLOWED_HOSTS=your-domain.com
   ```

2. **Use Redis**: Enable Redis for production caching
3. **Set Up Reverse Proxy**: Use Nginx or Apache as reverse proxy
4. **Enable HTTPS**: Use SSL certificates
5. **Monitor Performance**: Set up logging and monitoring

### Getting Help

If you encounter issues:

1. Check the logs: `docker-compose logs -f`
2. Verify environment variables in .env
3. Check port availability
4. Ensure Docker is running properly
5. Review the troubleshooting steps above

For additional support:
- Check the README.md for detailed documentation
- Review the API documentation at `/api/v1/schema/swagger-ui/`
- Test individual endpoints with curl or Postman