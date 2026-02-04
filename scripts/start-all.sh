#!/bin/bash

# SwiftLogistics - Master Start Script

echo "🚀 Starting SwiftLogistics Platform..."

# Ensure we are in the project root
cd "$(dirname "$0")/.."

# 1. Start Infrastructure (DB, Queue)
echo "📦 Starting Infrastructure..."
docker compose up -d mongodb rabbitmq

echo "⏳ Waiting for infrastructure (10s)..."
sleep 10

# 2. Start Mock Services
echo "🎭 Starting Mock Services..."
docker compose up -d cms-mock wms-mock ros-mock

# 3. Start Core Services
echo "🧠 Starting Core Services..."
docker compose up -d api-gateway orchestrator notification-service
# Also start adapters if they are separate containers
docker compose up -d cms-adapter ros-adapter wms-adapter

echo "✨ All services command sent."
echo "   Use 'make logs' to monitor startup."
echo "   Use 'make test' to verify health."
