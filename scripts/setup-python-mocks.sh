#!/bin/bash

# Setup script for Python mock services
echo "Setting up Python mock services..."

# Function to setup a service
setup_service() {
    local service_path=$1
    local service_name=$2
    
    echo "Setting up $service_name..."
    cd "$service_path" || exit
    
    # Create virtual environment
    python3 -m venv venv
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # Deactivate virtual environment
    deactivate
    
    echo "$service_name setup complete!"
    cd - > /dev/null || exit
}

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$SCRIPT_DIR/.."

# Setup each service
setup_service "$BASE_DIR/services/mocks/cms-mock-python" "CMS Mock Service"
setup_service "$BASE_DIR/services/mocks/ros-mock-python" "ROS Mock Service"
setup_service "$BASE_DIR/services/mocks/wms-mock-python" "WMS Mock Service"

echo ""
echo "All Python mock services have been set up successfully!"
echo ""
echo "To run a service:"
echo "  cd services/mocks/<service-name>-python"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""
echo "Or use Docker:"
echo "  cd services/mocks/<service-name>-python"
echo "  docker build -t <service-name>-python ."
echo "  docker run -p <port>:<port> <service-name>-python"
