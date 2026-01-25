#!/bin/bash

# SwiftLogistics Stop Script
# This script stops all running services

set -e

echo "🛑 Stopping SwiftLogistics..."
echo "=============================="
echo ""

# Stop all services
docker-compose down

echo ""
echo "✅ All services stopped"
echo ""
echo "💡 To completely remove all data (volumes), run:"
echo "   docker-compose down -v"
echo ""
echo "💡 To remove images as well, run:"
echo "   docker-compose down -v --rmi all"
