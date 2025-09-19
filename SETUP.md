# HiAnime Frontend Setup Guide

This frontend is built with Next.js 15, TypeScript, and Tailwind CSS to connect with the HiAnime Django backend API.

## Prerequisites

- Node.js 18+ 
- npm or yarn
- HiAnime Django backend running (see hianime_api repository)

## Installation

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.local.example .env.local
   ```
   
   Edit `.env.local` and set your backend API URL:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

4. **Open your browser:**
   Navigate to `http://localhost:3000`

## Backend Setup

The frontend requires the HiAnime Django backend to be running. Follow these steps to set up the backend:

1. **Clone the backend repository:**
   ```bash
   git clone https://github.com/debasish-panda-22/hianime_api.git
   cd hianime_api
   ```

2. **Set up the backend:**
   ```bash
   # Install Python dependencies
   pip install -r requirements.txt
   
   # Set up environment variables
   cp .env.example .env
   # Edit .env with your configuration
   
   # Run database migrations
   python manage.py migrate
   
   # Start the development server
   python manage.py runserver
   ```

3. **Access the backend API:**
   - API Root: http://localhost:8000/api/v1/
   - API Documentation: http://localhost:8000/api/v1/schema/swagger-ui/

## Features Implemented

### 🏠 Homepage
- **Hero Section**: Featured anime with watch now and add to list buttons
- **Navigation**: Sticky header with search, theme toggle, and login
- **Multiple Tabs**: Popular, Trending, Schedule, Latest Episodes
- **Real-time Data**: Fetches data from Django backend API
- **Responsive Design**: Works on all screen sizes

### 🔍 Search Functionality
- **Live Search**: Real-time search suggestions as you type
- **Search Page**: Dedicated search page with grid/list view toggle
- **Pagination**: Navigate through search results
- **Filters**: Sort by rating, title, episodes
- **Debounced Input**: Optimized search performance

### 📺 Anime Details
- **Detailed Information**: Synopsis, genres, status, episodes count
- **Episode List**: Scrollable list of all episodes
- **Tabbed Interface**: Overview, Episodes, Related content
- **External Links**: MyAnimeList and AniList integration
- **Action Buttons**: Watch now, add to list, favorite

### 🎨 Design & UX
- **Dark Theme**: Default dark theme with light theme toggle
- **Responsive Layout**: Mobile-first responsive design
- **Loading States**: Skeleton loaders and spinners
- **Error Handling**: Graceful error messages and retry options
- **Smooth Animations**: Hover effects and transitions

### 🔧 Technical Features
- **TypeScript**: Full type safety throughout the application
- **Custom Hooks**: Reusable data fetching hooks
- **API Service Layer**: Centralized API communication
- **Environment Configuration**: Flexible backend URL configuration
- **Component Library**: Built with shadcn/ui components

## Project Structure

```
src/
├── app/
│   ├── page.tsx              # Homepage
│   ├── search/
│   │   └── page.tsx          # Search results page
│   ├── anime/
│   │   └── [id]/
│   │       └── page.tsx      # Anime detail page
│   ├── layout.tsx           # Root layout with theme provider
│   └── globals.css          # Global styles
├── components/
│   └── ui/                  # shadcn/ui components
├── hooks/
│   ├── useAnimeData.ts      # Custom data fetching hooks
│   ├── use-mobile.ts        # Mobile detection hook
│   └── use-toast.ts        # Toast notifications
├── lib/
│   ├── api.ts              # API service layer
│   ├── db.ts               # Database client (unused in frontend)
│   ├── socket.ts           # Socket.io configuration
│   └── utils.ts            # Utility functions
└── ...
```

## API Integration

The frontend integrates with the HiAnime Django backend through a centralized API service layer:

### Available Endpoints

```typescript
// Homepage data
animeApi.getHomepage()

// Search functionality
animeApi.searchAnime(keyword, page)
animeApi.getSuggestions(keyword)

// Anime details
animeApi.getAnimeDetails(animeId)
animeApi.getEpisodes(animeId)

// Anime lists
animeApi.getAnimeList(query, category, page)

// Streaming
animeApi.getServers(episodeId)
animeApi.getStreamingLinks(episodeId, server, type)

// Genres
animeApi.getGenres()
```

### Response Types

All API responses are properly typed with TypeScript interfaces:

```typescript
interface Anime {
  id: string;
  title: string;
  poster: string;
  type: 'TV' | 'Movie' | 'OVA' | 'ONA' | 'Special';
  episodes: {
    sub: number | null;
    dub: number | null;
    eps: number;
  };
  // ... other properties
}
```

## Configuration

### Environment Variables

Create a `.env.local` file in the root directory:

```env
# HiAnime Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# For production, use your deployed backend URL
# NEXT_PUBLIC_API_URL=https://your-backend-domain.com/api/v1
```

### CORS Configuration

Make sure your Django backend is configured to allow requests from your frontend:

```python
# settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    # Add your production frontend URL
]
```

## Development

### Running in Development

1. Start the backend server:
   ```bash
   cd hianime_api
   python manage.py runserver
   ```

2. Start the frontend development server:
   ```bash
   npm run dev
   ```

3. Open `http://localhost:3000` in your browser

### Building for Production

```bash
# Build the frontend
npm run build

# Start the production server
npm start
```

### Code Quality

```bash
# Run linting
npm run lint

# Type checking (if using TypeScript strict mode)
npx tsc --noEmit
```

## Troubleshooting

### Common Issues

1. **CORS Errors**: Make sure your Django backend allows requests from `http://localhost:3000`

2. **API Connection Failed**: 
   - Check if the backend is running on `http://localhost:8000`
   - Verify the `NEXT_PUBLIC_API_URL` in `.env.local`
   - Check network connectivity

3. **Build Errors**:
   - Run `npm install` to ensure all dependencies are installed
   - Clear Next.js cache: `rm -rf .next`
   - Try rebuilding: `npm run build`

4. **TypeScript Errors**:
   - Make sure all API responses match the expected types
   - Check for missing imports or type definitions

### Debug Mode

Add debug logging to see API requests and responses:

```typescript
// In lib/api.ts, add interceptors for debugging
api.interceptors.request.use((config) => {
  console.log('API Request:', config);
  return config;
});

api.interceptors.response.use((response) => {
  console.log('API Response:', response.data);
  return response;
});
```

## Deployment

### Frontend Deployment

The frontend can be deployed to any platform that supports Next.js:

1. **Vercel** (Recommended):
   - Connect your GitHub repository to Vercel
   - Set environment variables in Vercel dashboard
   - Deploy automatically on push

2. **Netlify**:
   - Build command: `npm run build`
   - Publish directory: `.next`
   - Set environment variables

3. **Docker**:
   ```dockerfile
   FROM node:18-alpine
   WORKDIR /app
   COPY package*.json ./
   RUN npm ci --only=production
   COPY . .
   RUN npm run build
   EXPOSE 3000
   CMD ["npm", "start"]
   ```

### Backend Deployment

Deploy the Django backend to a hosting service like:

- Heroku
- DigitalOcean App Platform
- AWS Elastic Beanstalk
- PythonAnywhere

Make sure to update the `NEXT_PUBLIC_API_URL` environment variable to point to your deployed backend.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for educational purposes only. The content provided by this API is not owned by the developer and belongs to their respective owners.

## Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Open an issue on the GitHub repository
3. Refer to the backend documentation for API-specific issues