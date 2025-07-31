#!/bin/bash

echo "🚀 Starting FastDrive deployment with nginx proxy..."

# Build frontend
echo "📦 Building frontend..."
cd frontend/FastDrive
npm install
npm run build
cd ../..

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Build and start services
echo "🏗️ Building and starting services..."
docker-compose up --build -d

echo "✅ Deployment complete!"
echo "🌐 Application is now available at: http://localhost:8081"
echo "📁 Frontend files are served by nginx"
echo "🔗 API requests (/api/*) are proxied to backend"
