#!/bin/bash

# FBReaperV1 Streamlit Frontend Startup Script
# This script sets up and launches the Streamlit frontend

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check Python version
check_python_version() {
    if command_exists python3; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        REQUIRED_VERSION="3.8"
        
        if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
            print_success "Python $PYTHON_VERSION found"
            PYTHON_CMD="python3"
        else
            print_error "Python 3.8+ required, found $PYTHON_VERSION"
            exit 1
        fi
    elif command_exists python; then
        PYTHON_VERSION=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        if python -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
            print_success "Python $PYTHON_VERSION found"
            PYTHON_CMD="python"
        else
            print_error "Python 3.8+ required, found $PYTHON_VERSION"
            exit 1
        fi
    else
        print_error "Python not found. Please install Python 3.8 or higher."
        exit 1
    fi
}

# Function to check if virtual environment exists
check_virtual_env() {
    if [ -d "venv" ]; then
        print_status "Virtual environment found"
        return 0
    else
        print_warning "Virtual environment not found. Creating one..."
        return 1
    fi
}

# Function to create virtual environment
create_virtual_env() {
    print_status "Creating virtual environment..."
    $PYTHON_CMD -m venv venv
    print_success "Virtual environment created"
}

# Function to activate virtual environment
activate_virtual_env() {
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        # Windows
        source venv/Scripts/activate
    else
        # Unix/Linux/macOS
        source venv/bin/activate
    fi
    print_success "Virtual environment activated"
}

# Function to install dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install requirements
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        print_success "Dependencies installed successfully"
    else
        print_error "requirements.txt not found"
        exit 1
    fi
}

# Function to check backend connectivity
check_backend() {
    print_status "Checking backend connectivity..."
    
    # Default backend URL
    BACKEND_URL=${BACKEND_URL:-"http://localhost:8080"}
    
    if command_exists curl; then
        if curl -s --connect-timeout 5 "$BACKEND_URL/api/health" > /dev/null; then
            print_success "Backend is accessible at $BACKEND_URL"
        else
            print_warning "Backend is not accessible at $BACKEND_URL"
            print_warning "The frontend will work with mock data"
        fi
    else
        print_warning "curl not found, skipping backend connectivity check"
    fi
}

# Function to set environment variables
set_environment() {
    print_status "Setting up environment variables..."
    
    # Set default values
    export STREAMLIT_SERVER_PORT=${STREAMLIT_SERVER_PORT:-8501}
    export STREAMLIT_SERVER_ADDRESS=${STREAMLIT_SERVER_ADDRESS:-"0.0.0.0"}
    export STREAMLIT_SERVER_HEADLESS=${STREAMLIT_SERVER_HEADLESS:-true}
    export STREAMLIT_SERVER_ENABLE_CORS=${STREAMLIT_SERVER_ENABLE_CORS:-false}
    export STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=${STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION:-false}
    
    # Load from .env file if it exists
    if [ -f ".env" ]; then
        print_status "Loading environment variables from .env file"
        export $(cat .env | grep -v '^#' | xargs)
    fi
    
    print_success "Environment variables configured"
}

# Function to start Streamlit
start_streamlit() {
    print_status "Starting Streamlit frontend..."
    print_status "Frontend will be available at: http://localhost:$STREAMLIT_SERVER_PORT"
    print_status "Press Ctrl+C to stop the server"
    
    # Start Streamlit with configuration
    streamlit run app.py \
        --server.port=$STREAMLIT_SERVER_PORT \
        --server.address=$STREAMLIT_SERVER_ADDRESS \
        --server.headless=$STREAMLIT_SERVER_HEADLESS \
        --server.enableCORS=$STREAMLIT_SERVER_ENABLE_CORS \
        --server.enableXsrfProtection=$STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION \
        --logger.level=info
}

# Function to cleanup on exit
cleanup() {
    print_status "Shutting down Streamlit frontend..."
    exit 0
}

# Main execution
main() {
    echo "=========================================="
    echo "  FBReaperV1 Streamlit Frontend Startup"
    echo "=========================================="
    echo ""
    
    # Set up signal handlers
    trap cleanup SIGINT SIGTERM
    
    # Check Python version
    check_python_version
    
    # Check/create virtual environment
    if ! check_virtual_env; then
        create_virtual_env
    fi
    
    # Activate virtual environment
    activate_virtual_env
    
    # Install dependencies
    install_dependencies
    
    # Set environment variables
    set_environment
    
    # Check backend connectivity
    check_backend
    
    echo ""
    print_success "Setup complete! Starting Streamlit frontend..."
    echo ""
    
    # Start Streamlit
    start_streamlit
}

# Run main function
main "$@"