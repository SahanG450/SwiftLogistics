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
setup_service "$BASE_DIR/services/mocks/cms-mock" "CMS Mock Service"
setup_service "$BASE_DIR/services/mocks/ros-mock" "ROS Mock Service"
setup_service "$BASE_DIR/services/mocks/wms-mock" "WMS Mock Service"

echo ""
echo "All Python mock services have been set up successfully!"
echo ""
echo "To run a service manually:"
echo "  cd services/mocks/<service-name>"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""
echo "Or use the start script:"
echo "  ./scripts/start-python-mocks.sh"
echo ""
echo "Services will be available at:"
echo "  CMS Mock: http://localhost:3001"
echo "  ROS Mock: http://localhost:3002"
echo "  WMS Mock: http://localhost:3003"
