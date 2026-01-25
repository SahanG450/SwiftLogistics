#!/bin/bash

# SwiftLogistics Quick Start Script
# This script helps you get started with the application

set -e

echo "🚀 SwiftLogistics Quick Start"
echo "=============================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "   Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker is installed"
echo "✅ Docker Compose is installed"
echo ""

# Check if .env file exists, if not create from example
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        echo "📝 Creating .env file from .env.example..."
        cp .env.example .env
        echo "✅ .env file created"
    fi
else
    echo "✅ .env file exists"
fi
echo ""

# Build and start services
echo "🏗️  Building Docker images..."
docker-compose build

echo ""
echo "🚀 Starting services..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be healthy..."
sleep 10

# Check service status
echo ""
echo "📊 Service Status:"
docker-compose ps

echo ""
echo "✅ SwiftLogistics is running!"
echo ""
echo "📡 Available Services:"
echo "   • API Gateway:        http://localhost:3000"
echo "   • Orchestrator:       http://localhost:3001"
echo "   • Notification:       http://localhost:3002"
echo "   • RabbitMQ UI:        http://localhost:15672 (admin/admin123)"
echo "   • MongoDB:            mongodb://localhost:27017"
echo ""
echo "📚 Documentation:"
echo "   • Architecture:       ./ARCHITECTURE.md"
echo "   • Diagrams:          ./DIAGRAMS.md"
echo "   • README:            ./README.md"
echo ""
echo "🔧 Useful Commands:"
echo "   • View logs:         docker-compose logs -f"
echo "   • Stop services:     docker-compose down"
echo "   • Restart:           docker-compose restart"
echo "   • Make commands:     make help"
echo ""
echo "🎉 Happy coding!"
