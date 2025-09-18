# Docker Compose Fix Summary

## Issue Identified
The Docker Compose build was failing with the following error:
```
npm error The `npm ci` command can only install with an existing package-lock.json or
npm error npm-shrinkwrap.json with lockfileVersion >= 1.
```

## Root Cause
The `.dockerignore` file was excluding `package-lock.json` from the Docker build context. This prevented the Dockerfile from accessing the package-lock.json file when trying to run `npm ci`.

## Files Affected
- `.dockerignore` - Was excluding package-lock.json
- `Dockerfile.dev.frontend` - Uses `npm ci` for development builds
- `Dockerfile.frontend` - Uses `npm ci --only=production` for production builds

## Fix Applied
Removed `package-lock.json` from the `.dockerignore` file so it can be included in the Docker build context.

### Before:
```dockerignore
Dockerfile
.dockerignore
node_modules
npm-debug.log
README.md
.next
.git
package-lock.json  # ← This line was causing the issue
yarn.lock
pnpm-lock.yaml
test
*.log
local-*
```

### After:
```dockerignore
Dockerfile
.dockerignore
node_modules
npm-debug.log
README.md
.next
.git
yarn.lock
pnpm-lock.yaml
test
*.log
local-*
```

## How to Test
Navigate to the hianime_api directory and run the development script:

```bash
cd hianime_api
./dev.sh
```

Alternatively, you can test just the build:
```bash
cd hianime_api
docker compose -f docker-compose.dev.yml build
```

## Why This Fix Works
1. `npm ci` requires a `package-lock.json` file to be present in the build context
2. The `.dockerignore` file was preventing `package-lock.json` from being copied to the Docker build context
3. By removing the exclusion, the `package-lock.json` file is now available during the Docker build process
4. Both development and production Dockerfiles can now successfully run `npm ci`

## Additional Notes
- The fix applies to both development (`Dockerfile.dev.frontend`) and production (`Dockerfile.frontend`) builds
- The `package-lock.json` file exists in the project root and was properly committed to the repository
- No changes were needed to the Dockerfiles themselves, only to the `.dockerignore` file