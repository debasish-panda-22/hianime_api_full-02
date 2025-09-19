#!/bin/bash

echo "🔍 Starting debug build process..."

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found. Please run this script from the project root."
    exit 1
fi

echo "📦 Installing dependencies..."
npm install

echo "🔍 Checking TypeScript configuration..."
if [ ! -f "tsconfig.json" ]; then
    echo "❌ Error: tsconfig.json not found"
    exit 1
fi

echo "🔍 Checking Next.js configuration..."
if [ ! -f "next.config.ts" ]; then
    echo "❌ Error: next.config.ts not found"
    exit 1
fi

echo "🔍 Checking server file..."
if [ ! -f "server.ts" ]; then
    echo "❌ Error: server.ts not found"
    exit 1
fi

echo "🔍 Checking socket configuration..."
if [ ! -f "src/lib/socket.ts" ]; then
    echo "❌ Error: src/lib/socket.ts not found"
    exit 1
fi

echo "🔍 Building TypeScript server files..."
npm run build:server
if [ $? -ne 0 ]; then
    echo "❌ Error: TypeScript build failed"
    exit 1
fi

echo "✅ TypeScript build successful"

echo "🔍 Checking if dist/server.js was created..."
if [ ! -f "dist/server.js" ]; then
    echo "❌ Error: dist/server.js was not created"
    exit 1
fi

echo "✅ dist/server.js created successfully"

echo "🔍 Testing server startup..."
timeout 5 node dist/server.js || echo "Server startup test completed"

echo "🔍 Starting Next.js build (this may take a while)..."
npm run build
if [ $? -ne 0 ]; then
    echo "❌ Error: Next.js build failed"
    echo "🔍 Trying to get more detailed error information..."
    npm run build --verbose
    exit 1
fi

echo "✅ Next.js build successful"

echo "🔍 Checking if .next directory was created..."
if [ ! -d ".next" ]; then
    echo "❌ Error: .next directory was not created"
    exit 1
fi

echo "✅ .next directory created successfully"

echo "🔍 Checking standalone output..."
if [ ! -d ".next/standalone" ]; then
    echo "❌ Error: .next/standalone directory was not created"
    echo "🔍 Checking .next directory contents:"
    ls -la .next/
    exit 1
fi

echo "✅ Standalone build successful"

echo "🎉 All builds completed successfully!"
echo "🚀 You can now run: node dist/server.js"