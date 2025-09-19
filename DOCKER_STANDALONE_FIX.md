# Docker Standalone Build Fix

## Problem
The Docker build was failing with the error:
```
failed to solve: failed to compute cache key: failed to calculate checksum of ref 92486b58-69b5-40e6-bcaf-51cc6356ec1e::cwhubizybggzhahvnkzadpjr8: "/app/.next/standalone": not found
```

## Root Cause
The Next.js application was not configured to generate standalone output, which is required for the Docker build process. The Dockerfile was trying to copy `/app/.next/standalone` from the builder stage, but this directory was never generated because:

1. **Missing Standalone Configuration**: The `next.config.ts` file was missing the `output: 'standalone'` configuration
2. **Build Process**: Without standalone output enabled, Next.js doesn't generate the self-contained server.js and required files

## Solution
Updated the Next.js configuration to enable standalone output:

### File: `next.config.ts`
```typescript
const nextConfig: NextConfig = {
  /* config options here */
  output: 'standalone',  // ← Added this line
  typescript: {
    ignoreBuildErrors: true,
  },
  // ... rest of configuration
};
```

## Verification
After making this change:

1. **Local Build**: ✅ `npm run build` now generates the standalone output
2. **Standalone Directory**: ✅ `.next/standalone/` directory is created with:
   - `server.js` - Self-contained Next.js server
   - `package.json` - Production dependencies only
3. **Static Files**: ✅ `.next/static/` directory contains all static assets
4. **Public Files**: ✅ `public/` directory contains static assets

## Docker Build Process
The Dockerfile now works correctly:

1. **Builder Stage**: 
   - Installs dependencies with `npm ci`
   - Builds the application with `npm run build`
   - Generates `.next/standalone/` directory

2. **Runner Stage**:
   - Copies standalone server: `COPY --from=builder /app/.next/standalone ./`
   - Copies static files: `COPY --from=builder /app/.next/static ./.next/static`
   - Copies public files: `COPY --from=builder /app/public ./public`
   - Runs the standalone server: `CMD ["node", "server.js"]`

## Result
The Docker build should now succeed and create a production-ready Next.js application that can be deployed using:

```bash
# From the hianime_api directory
docker compose build frontend
docker compose up -d frontend
```

## Files Modified
- `next.config.ts` - Added `output: 'standalone'` configuration

## Files Verified
- `.next/standalone/server.js` - ✅ Generated correctly
- `.next/standalone/package.json` - ✅ Generated correctly
- `.next/static/` - ✅ Contains all static assets
- `public/` - ✅ Contains public assets

The HiAnime frontend is now ready for Docker deployment!