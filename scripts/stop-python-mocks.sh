#!/bin/bash

# Stop all Python mock services
echo "Stopping Python mock services..."

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$SCRIPT_DIR/.."

# Function to stop a service
stop_service() {
    local service_path=$1
    local service_name=$2
    
    if [ -f "$service_path/service.pid" ]; then
        echo "Stopping $service_name..."
        kill $(cat "$service_path/service.pid") 2>/dev/null
        rm "$service_path/service.pid"
    fi
}

# Stop each service
stop_service "$BASE_DIR/services/mocks/cms-mock-python" "CMS Mock Service"
stop_service "$BASE_DIR/services/mocks/ros-mock-python" "ROS Mock Service"
stop_service "$BASE_DIR/services/mocks/wms-mock-python" "WMS Mock Service"

echo "All Python mock services stopped!"
