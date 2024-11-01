#!/bin/bash

# setup_environment.sh - Environment setup script

set -e  # Exit immediately if a command exits with a non-zero status

# Define variables
VENV_DIR="venv"  # Virtual environment directory
REQUIREMENTS_FILE="requirements.txt"  # Requirements file
ENV_FILE=".env"  # Environment file

# Function to log messages
log() {
    echo "$(date +'%Y-%m-%d %H:%M:%S') - $1"
}

log "Setting up the environment..."

# Create a virtual environment
if [ ! -d "$VENV_DIR" ]; then
    log "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
else
    log "Virtual environment already exists."
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

# Install dependencies
log "Installing dependencies..."
pip install -r "$REQUIREMENTS_FILE"

# Create .env file if it doesn't exist
if [ ! -f "$ENV_FILE" ]; then
    log "Creating environment file: $ENV_FILE"
    echo "DATABASE_URL=your_database_url" > "$ENV_FILE"
    echo "SECRET_KEY=your_secret_key" >> "$ENV_FILE"
    echo "DEBUG=True" >> "$ENV_FILE"
else
    log "Environment file already exists."
fi

log "Environment setup completed successfully."
