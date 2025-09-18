# HiAnime Django API

A Django-based RESTful API that utilizes web scraping to fetch anime content from hianime.bz. This is a Python/Django clone of the original hianime-API project.

## Features

- ✅ **Homepage Data**: Fetch spotlight, trending, top airing, and other homepage sections
- ✅ **Anime Details**: Get detailed information about specific anime
- ✅ **Search Functionality**: Search anime by keyword with pagination
- ✅ **Search Suggestions**: Get real-time search suggestions
- ✅ **Episode Lists**: Retrieve episode lists for anime
- ✅ **Server Information**: Get available streaming servers for episodes
- ✅ **Streaming Links**: Extract direct streaming links
- ✅ **Anime Lists**: Browse anime by categories (top airing, most popular, genres, etc.)
- ✅ **Caching**: Redis-based caching for improved performance
- ✅ **Rate Limiting**: Built-in rate limiting to prevent abuse
- ✅ **API Documentation**: OpenAPI/Swagger documentation
- ✅ **Docker Support**: Containerized deployment with Docker Compose

## Tech Stack

- **Backend**: Django 4.2 + Django REST Framework
- **Web Scraping**: BeautifulSoup4 + Requests
- **Caching**: Redis (optional, falls back to local memory)
- **Documentation**: drf-spectacular (OpenAPI 3)
- **Rate Limiting**: django-ratelimit
- **Containerization**: Docker + Docker Compose V2

## Quick Start

### Using Docker (Recommended)

1. **Clone and navigate to the project**:
   ```bash
   git clone <your-repo-url>
   cd anime_api_project
   ```

2. **Build and run with the automated script**:
   ```bash
   ./build_and_run.sh
   ```

   Or manually:
   ```bash
   # Build the Docker image
   docker buildx build --load -t hianime-django .
   
   # Run with Docker Compose
   docker compose up -d
   ```

3. **Access the API**:
   - API Root: http://localhost:8000
   - API Documentation: http://localhost:8000/api/v1/schema/swagger-ui/
   - ReDoc Documentation: http://localhost:8000/api/v1/schema/redoc/

### Manual Installation

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run database migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

## Docker Commands

### Build Image
```bash
docker buildx build --load -t hianime-django .
```

### Run with Docker Compose
```bash
# Start services
docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs -f

# Restart services
docker compose restart

# Rebuild and restart
docker compose up -d --build

# Enter container
docker compose exec web bash

# Show running containers
docker compose ps

# Remove volumes (WARNING: This will delete all data)
docker compose down -v
```

### Manual Docker Run
```bash
docker run -p 8000:8000 \
  -e DEBUG=False \
  -e SECRET_KEY=your-secret-key \
  -e REDIS_URL=redis://host.docker.internal:6379/0 \
  hianime-django
```

## API Endpoints

### Base URL
```
http://localhost:8000/api/v1/
```

### Available Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API documentation and information |
| `/home/` | GET | Homepage data (spotlight, trending, etc.) |
| `/anime/{id}/` | GET | Detailed anime information |
| `/animes/{query}/` | GET | Anime lists by category |
| `/animes/{query}/{category}/` | GET | Anime lists with category filter |
| `/search/` | GET | Search anime by keyword |
| `/suggestion/` | GET | Search suggestions |
| `/episodes/{id}/` | GET | Episode list for anime |
| `/servers/` | GET | Available servers for episode |
| `/stream/` | GET | Streaming links for episode |
| `/genres/` | GET | All available genres |

### Query Parameters

#### Search Endpoint
- `keyword` (required): Search term
- `page` (optional): Page number (default: 1)

#### Anime Lists
Valid queries:
- `top-airing`, `most-popular`, `most-favorite`, `completed`
- `recently-added`, `recently-updated`, `top-upcoming`
- `genre` (requires category), `az-list` (requires category)
- `subbed-anime`, `dubbed-anime`, `movie`, `tv`, `ova`, `ona`, `special`, `events`

#### Streaming Endpoint
- `id` (required): Episode ID
- `server` (required): Server name
- `type` (required): `sub` or `dub`

## Environment Variables

Create a `.env` file based on `.env.example`:

```env
# Django settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Cache settings
REDIS_URL=redis://localhost:6379/0
CACHE_TIMEOUT=3600

# Rate limiting
RATELIMIT_ENABLE=True
RATELIMIT_RATE=100/h

# Anime API configuration
ANIME_API_BASE_URL=https://hianime.bz
ANIME_API_BASE_URL_V2=https://kaido.to
ANIME_API_PROVIDERS=https://megacloud.club
```

## API Usage Examples

### Get Homepage Data
```bash
curl http://localhost:8000/api/v1/home/
```

### Search Anime
```bash
curl "http://localhost:8000/api/v1/search/?keyword=one%20piece&page=1"
```

### Get Anime Details
```bash
curl http://localhost:8000/api/v1/anime/one-piece-100/
```

### Get Episodes
```bash
curl http://localhost:8000/api/v1/episodes/one-piece-100/
```

### Get Streaming Links
```bash
curl "http://localhost:8000/api/v1/stream/?id=one-piece-100::ep=1000&server=HD-1&type=sub"
```

## Development

### Project Structure
```
anime_api_project/
├── anime_api/                 # Django app
│   ├── extractors/            # HTML parsing modules
│   ├── services/              # HTTP and configuration services
│   ├── utils/                 # Utility functions
│   ├── views/                 # API views
│   └── urls.py               # App URLs
├── anime_api_project/        # Project settings
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose configuration
└── build_and_run.sh        # Build and run script
```

### Adding New Endpoints

1. Create a new view in `anime_api/views/`
2. Add URL pattern in `anime_api/urls.py`
3. Add proper documentation with drf-spectacular decorators
4. Implement rate limiting and error handling
5. Test the endpoint

### Running Tests

```bash
# Run Django tests
python manage.py test

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Check what's using port 8000
   lsof -i :8000
   # Kill the process
   kill -9 <PID>
   ```

2. **Permission Issues**
   ```bash
   # Fix permissions
   sudo chown -R $USER:$USER .
   ```

3. **Docker Issues**
   ```bash
   # Clean up Docker
   docker system prune -a
   docker volume prune
   ```

4. **Redis Connection Issues**
   ```bash
   # Check if Redis is running
   docker compose ps redis
   # Restart Redis
   docker compose restart redis
   ```

5. **Docker Compose V2 Issues**
   ```bash
   # Check Docker Compose version
   docker compose version
   # If not available, install Docker Compose V2
   ```

### Docker Compose V2 Migration Notes

This project has been updated to use Docker Compose V2 (`docker compose`) instead of the legacy `docker-compose` command. Key changes:

- **Command Change**: Use `docker compose` instead of `docker-compose`
- **Version Spec**: Removed `version: '3.8'` from docker-compose.yml (now optional)
- **Enhanced Restart**: Added `restart: unless-stopped` policies for better reliability
- **Improved Script**: Updated build_and_run.sh with better error handling and useful commands

### Migration from Legacy docker-compose

If you were using the legacy `docker-compose` command:

1. **Update your habits**: Use `docker compose` instead of `docker-compose`
2. **Update scripts**: Replace all `docker-compose` references with `docker compose`
3. **Check compatibility**: The YAML format is mostly compatible, but version is now optional
4. **Update CI/CD**: Update any automated scripts or pipeline configurations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for educational purposes only. The content provided by this API is not owned by the developer and belongs to their respective owners.

## Disclaimer

This API is just an unofficial API for hianime.bz and is in no other way officially related to the same. The content that this API provides is not mine, nor is it hosted by me. These belong to their respective owners. This API just demonstrates how to build an API that scrapes websites and uses their content.

## Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.