# Docker Build Fix Guide

## Problem Analysis
The Docker build is failing at the `npm run build` step, which is taking 134.4 seconds and then hanging. This is typically caused by:

1. **Memory issues**: Next.js builds can be memory-intensive
2. **Build dependencies**: Missing build tools in the Docker image
3. **Configuration issues**: Next.js configuration problems
4. **File permissions**: Permission issues during build

## Immediate Solutions

### Solution 1: Use the Improved Dockerfile

Replace your current `Dockerfile.frontend` with this improved version:

```dockerfile
# Build stage
FROM node:18-alpine AS builder

# Install build dependencies
RUN apk add --no-cache python3 make g++

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies with verbose output
RUN npm ci --verbose

# Copy source code
COPY . .

# Create .next directory and set permissions
RUN mkdir -p .next && chown -R node:node /app

# Switch to node user for build
USER node

# Build the application with increased memory and verbose output
ENV NODE_OPTIONS="--max-old-space-size=4096"
RUN npm run build --verbose

# Build server files
RUN npm run build:server

# Production stage
FROM node:18-alpine AS runner

WORKDIR /app

# Create non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy package files for production dependencies
COPY package*.json ./

# Install production dependencies only
RUN npm ci --only=production --verbose

# Copy built application
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public
COPY --from=builder /app/server.ts ./
COPY --from=builder /app/dist ./dist

# Set correct permissions
RUN chown -R nextjs:nodejs /app

USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"
ENV NODE_ENV production

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/api/health', (res) => { process.exit(res.statusCode === 200 ? 0 : 1) }).on('error', () => process.exit(1))"

CMD ["node", "dist/server.js"]
```

### Solution 2: Use the Simple Dockerfile

If the improved version still has issues, try this simpler version:

```dockerfile
# Build stage
FROM node:18-alpine AS builder

# Install build dependencies
RUN apk add --no-cache python3 make g++

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build the application with error handling
RUN npm run build:server || { echo "Server build failed"; exit 1; }
RUN npm run build || { echo "Next.js build failed"; exit 1; }

# Production stage
FROM node:18-alpine AS runner

WORKDIR /app

# Create non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy package files
COPY package*.json ./

# Install production dependencies
RUN npm ci --only=production

# Copy built application
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public
COPY --from=builder /app/server.ts ./
COPY --from=builder /app/dist ./dist

# Set correct permissions
RUN chown -R nextjs:nodejs /app

USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"
ENV NODE_ENV production

CMD ["node", "dist/server.js"]
```

### Solution 3: Debug the Build Process

1. **Run the debug script locally**:
   ```bash
   chmod +x debug-build.sh
   ./debug-build.sh
   ```

2. **Check for specific errors**:
   ```bash
   npm run build --verbose
   ```

3. **Clear Next.js cache**:
   ```bash
   rm -rf .next
   npm run build
   ```

### Solution 4: Modify next.config.ts

Update your `next.config.ts` to include more build optimizations:

```typescript
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'standalone',
  typescript: {
    ignoreBuildErrors: true,
  },
  eslint: {
    ignoreDuringBuilds: true,
  },
  // Add these optimizations
  swcMinify: true,
  compress: true,
  poweredByHeader: false,
  // Increase memory for build
  experimental: {
    serverComponentsExternalPackages: [],
  },
  // Handle large builds
  webpack: (config, { dev }) => {
    if (dev) {
      config.watchOptions = {
        ignored: ['**/*'],
      };
    }
    // Add performance optimizations
    config.performance = {
      maxEntrypointSize: 512000,
      maxAssetSize: 512000,
    };
    return config;
  },
};

export default nextConfig;
```

### Solution 5: Manual Build and Copy

If Docker builds continue to fail, try building locally and copying:

1. **Build locally**:
   ```bash
   npm install
   npm run build:server
   npm run build
   ```

2. **Create a manual Dockerfile**:
   ```dockerfile
   FROM node:18-alpine

   WORKDIR /app

   # Copy package files
   COPY package*.json ./

   # Install production dependencies
   RUN npm ci --only=production

   # Copy pre-built files
   COPY .next/standalone ./
   COPY .next/static ./.next/static
   COPY public ./public
   COPY server.ts ./
   COPY dist ./dist

   # Create non-root user
   RUN addgroup --system --gid 1001 nodejs
   RUN adduser --system --uid 1001 nextjs
   RUN chown -R nextjs:nodejs /app

   USER nextjs

   EXPOSE 3000

   ENV PORT 3000
   ENV HOSTNAME "0.0.0.0"
   ENV NODE_ENV production

   CMD ["node", "dist/server.js"]
   ```

## Testing the Fix

After applying any of these solutions, test the build:

```bash
# Clean build
docker-compose down
docker system prune -f

# Rebuild
docker-compose up --build -d frontend

# Check logs
docker-compose logs frontend
```

## Common Issues and Fixes

### Issue 1: Memory Limit
**Symptom**: Build hangs at `npm run build`
**Fix**: Add `ENV NODE_OPTIONS="--max-old-space-size=4096"` to Dockerfile

### Issue 2: Missing Build Tools
**Symptom**: Build fails with compilation errors
**Fix**: Add `RUN apk add --no-cache python3 make g++` to Dockerfile

### Issue 3: Permission Issues
**Symptom**: Build fails with permission denied errors
**Fix**: Add proper user permissions and directory creation

### Issue 4: Next.js Cache Issues
**Symptom**: Build fails with cache-related errors
**Fix**: Add `RUN rm -rf .next` before build step

## Troubleshooting Commands

```bash
# Check Docker build logs
docker-compose logs --tail=50 frontend

# Check container status
docker-compose ps frontend

# Enter container for debugging
docker-compose exec frontend sh

# Check Next.js build output
docker-compose exec frontend ls -la .next/

# Test server startup
docker-compose exec frontend node dist/server.js
```

Choose the solution that best fits your environment and test thoroughly. The improved Dockerfile with memory limits and build dependencies should resolve most issues.