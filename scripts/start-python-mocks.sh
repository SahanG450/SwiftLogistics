#!/bin/bash

# Start all Python mock services
echo "Starting Python mock services..."

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$SCRIPT_DIR/.."

# Function to start a service
start_service() {
    local service_path=$1
    local service_name=$2
    
    echo "Starting $service_name..."
    cd "$service_path" || exit
    
    # Activate virtual environment and start service
    source venv/bin/activate
    python app.py &
    echo "$!" > service.pid
    deactivate
    
    cd - > /dev/null || exit
}

# Start each service
start_service "$BASE_DIR/services/mocks/cms-mock-python" "CMS Mock Service"
start_service "$BASE_DIR/services/mocks/ros-mock-python" "ROS Mock Service"
start_service "$BASE_DIR/services/mocks/wms-mock-python" "WMS Mock Service"

echo ""
echo "All Python mock services started!"
echo "CMS Mock: http://localhost:3001"
echo "ROS Mock: http://localhost:3002"
echo "WMS Mock: http://localhost:3003"
