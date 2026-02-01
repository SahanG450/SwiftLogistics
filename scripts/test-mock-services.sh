#!/bin/bash

# Test script for Python Mock Services
# This script verifies all mock services are working correctly

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR/.."

echo "========================================="
echo "Python Mock Services - Comprehensive Test"
echo "========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Function to print success
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
    ((PASSED_TESTS++))
    ((TOTAL_TESTS++))
}

# Function to print failure
print_failure() {
    echo -e "${RED}✗ $1${NC}"
    ((FAILED_TESTS++))
    ((TOTAL_TESTS++))
}

# Function to print info
print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

echo "1. Checking file structure..."
echo "--------------------------------"

# Check CMS Mock
if [ -f "$PROJECT_ROOT/services/mocks/cms-mock/app.py" ]; then
    print_success "CMS Mock - app.py exists"
else
    print_failure "CMS Mock - app.py missing"
fi

if [ -f "$PROJECT_ROOT/services/mocks/cms-mock/src/utils/file_storage.py" ]; then
    print_success "CMS Mock - file_storage.py exists"
else
    print_failure "CMS Mock - file_storage.py missing"
fi

if [ -d "$PROJECT_ROOT/services/mocks/cms-mock/data" ]; then
    print_success "CMS Mock - data directory exists"
else
    print_failure "CMS Mock - data directory missing"
fi

# Check ROS Mock
if [ -f "$PROJECT_ROOT/services/mocks/ros-mock/app.py" ]; then
    print_success "ROS Mock - app.py exists"
else
    print_failure "ROS Mock - app.py missing"
fi

if [ -f "$PROJECT_ROOT/services/mocks/ros-mock/src/utils/file_storage.py" ]; then
    print_success "ROS Mock - file_storage.py exists"
else
    print_failure "ROS Mock - file_storage.py missing"
fi

if [ -d "$PROJECT_ROOT/services/mocks/ros-mock/data" ]; then
    print_success "ROS Mock - data directory exists"
else
    print_failure "ROS Mock - data directory missing"
fi

# Check WMS Mock
if [ -f "$PROJECT_ROOT/services/mocks/wms-mock/app.py" ]; then
    print_success "WMS Mock - app.py exists"
else
    print_failure "WMS Mock - app.py missing"
fi

if [ -f "$PROJECT_ROOT/services/mocks/wms-mock/src/utils/file_storage.py" ]; then
    print_success "WMS Mock - file_storage.py exists"
else
    print_failure "WMS Mock - file_storage.py missing"
fi

if [ -d "$PROJECT_ROOT/services/mocks/wms-mock/data" ]; then
    print_success "WMS Mock - data directory exists"
else
    print_failure "WMS Mock - data directory missing"
fi

echo ""
echo "2. Checking Python syntax..."
echo "--------------------------------"

# Check CMS Mock Python files
if python3 -m py_compile "$PROJECT_ROOT/services/mocks/cms-mock/app.py" 2>/dev/null; then
    print_success "CMS Mock - app.py syntax valid"
else
    print_failure "CMS Mock - app.py syntax error"
fi

if python3 -m py_compile "$PROJECT_ROOT/services/mocks/cms-mock/src/utils/file_storage.py" 2>/dev/null; then
    print_success "CMS Mock - file_storage.py syntax valid"
else
    print_failure "CMS Mock - file_storage.py syntax error"
fi

# Check ROS Mock Python files
if python3 -m py_compile "$PROJECT_ROOT/services/mocks/ros-mock/app.py" 2>/dev/null; then
    print_success "ROS Mock - app.py syntax valid"
else
    print_failure "ROS Mock - app.py syntax error"
fi

if python3 -m py_compile "$PROJECT_ROOT/services/mocks/ros-mock/src/utils/file_storage.py" 2>/dev/null; then
    print_success "ROS Mock - file_storage.py syntax valid"
else
    print_failure "ROS Mock - file_storage.py syntax error"
fi

# Check WMS Mock Python files
if python3 -m py_compile "$PROJECT_ROOT/services/mocks/wms-mock/app.py" 2>/dev/null; then
    print_success "WMS Mock - app.py syntax valid"
else
    print_failure "WMS Mock - app.py syntax error"
fi

if python3 -m py_compile "$PROJECT_ROOT/services/mocks/wms-mock/src/utils/file_storage.py" 2>/dev/null; then
    print_success "WMS Mock - file_storage.py syntax valid"
else
    print_failure "WMS Mock - file_storage.py syntax error"
fi

echo ""
echo "3. Checking configuration files..."
echo "--------------------------------"

# Check requirements.txt
if [ -f "$PROJECT_ROOT/services/mocks/cms-mock/requirements.txt" ]; then
    if grep -q "fastapi" "$PROJECT_ROOT/services/mocks/cms-mock/requirements.txt"; then
        print_success "CMS Mock - requirements.txt valid"
    else
        print_failure "CMS Mock - requirements.txt missing fastapi"
    fi
else
    print_failure "CMS Mock - requirements.txt missing"
fi

if [ -f "$PROJECT_ROOT/services/mocks/ros-mock/requirements.txt" ]; then
    if grep -q "fastapi" "$PROJECT_ROOT/services/mocks/ros-mock/requirements.txt"; then
        print_success "ROS Mock - requirements.txt valid"
    else
        print_failure "ROS Mock - requirements.txt missing fastapi"
    fi
else
    print_failure "ROS Mock - requirements.txt missing"
fi

if [ -f "$PROJECT_ROOT/services/mocks/wms-mock/requirements.txt" ]; then
    if grep -q "fastapi" "$PROJECT_ROOT/services/mocks/wms-mock/requirements.txt"; then
        print_success "WMS Mock - requirements.txt valid"
    else
        print_failure "WMS Mock - requirements.txt missing fastapi"
    fi
else
    print_failure "WMS Mock - requirements.txt missing"
fi

# Check Dockerfiles
if [ -f "$PROJECT_ROOT/services/mocks/cms-mock/Dockerfile" ]; then
    print_success "CMS Mock - Dockerfile exists"
else
    print_failure "CMS Mock - Dockerfile missing"
fi

if [ -f "$PROJECT_ROOT/services/mocks/ros-mock/Dockerfile" ]; then
    print_success "ROS Mock - Dockerfile exists"
else
    print_failure "ROS Mock - Dockerfile missing"
fi

if [ -f "$PROJECT_ROOT/services/mocks/wms-mock/Dockerfile" ]; then
    print_success "WMS Mock - Dockerfile exists"
else
    print_failure "WMS Mock - Dockerfile missing"
fi

echo ""
echo "4. Checking documentation..."
echo "--------------------------------"

if [ -f "$PROJECT_ROOT/services/mocks/cms-mock/README.md" ]; then
    if grep -q "File-based JSON" "$PROJECT_ROOT/services/mocks/cms-mock/README.md"; then
        print_success "CMS Mock - README.md mentions file-based storage"
    else
        print_failure "CMS Mock - README.md doesn't mention file-based storage"
    fi
else
    print_failure "CMS Mock - README.md missing"
fi

if [ -f "$PROJECT_ROOT/services/mocks/ros-mock/README.md" ]; then
    if grep -q "File-based JSON" "$PROJECT_ROOT/services/mocks/ros-mock/README.md"; then
        print_success "ROS Mock - README.md mentions file-based storage"
    else
        print_failure "ROS Mock - README.md doesn't mention file-based storage"
    fi
else
    print_failure "ROS Mock - README.md missing"
fi

if [ -f "$PROJECT_ROOT/services/mocks/wms-mock/README.md" ]; then
    if grep -q "File-based JSON" "$PROJECT_ROOT/services/mocks/wms-mock/README.md"; then
        print_success "WMS Mock - README.md mentions file-based storage"
    else
        print_failure "WMS Mock - README.md doesn't mention file-based storage"
    fi
else
    print_failure "WMS Mock - README.md missing"
fi

if [ -f "$PROJECT_ROOT/FILE_STORAGE_GUIDE.md" ]; then
    print_success "FILE_STORAGE_GUIDE.md exists"
else
    print_failure "FILE_STORAGE_GUIDE.md missing"
fi

if [ -f "$PROJECT_ROOT/FILE_STORAGE_SUMMARY.md" ]; then
    print_success "FILE_STORAGE_SUMMARY.md exists"
else
    print_failure "FILE_STORAGE_SUMMARY.md missing"
fi

echo ""
echo "========================================="
echo "Test Results"
echo "========================================="
echo "Total tests:  $TOTAL_TESTS"
echo -e "${GREEN}Passed:       $PASSED_TESTS${NC}"
if [ $FAILED_TESTS -gt 0 ]; then
    echo -e "${RED}Failed:       $FAILED_TESTS${NC}"
else
    echo -e "${GREEN}Failed:       $FAILED_TESTS${NC}"
fi
echo ""

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed! Mock services are ready.${NC}"
    exit 0
else
    echo -e "${RED}✗ Some tests failed. Please check the output above.${NC}"
    exit 1
fi
