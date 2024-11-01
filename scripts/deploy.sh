#!/bin/bash

# deploy.sh - Deployment script for the application

set -e  # Exit immediately if a command exits with a non-zero status

# Define variables
APP_DIR="/path/to/your/app"  # Change this to your application directory
ENV_FILE=".env"              # Environment file
LOG_FILE="deploy.log"        # Log file for deployment

# Function to log messages
log() {
    echo "$(date +'%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Load environment variables
if [ -f "$APP_DIR/$ENV_FILE" ]; then
    export $(grep -v '^#' "$APP_DIR/$ENV_FILE" | xargs)
else
    log "Environment file not found: $APP_DIR/$ENV_FILE"
    exit 1
fi

log "Starting deployment..."

# Navigate to the application directory
cd "$APP_DIR"

# Pull the latest code from the repository
log "Pulling latest code from repository..."
git pull origin main

# Install dependencies
log "Installing dependencies..."
pip install -r requirements.txt

# Run database migrations
log "Running database migrations..."
python manage.py migrate

# Start the application (example for a Flask app)
log "Starting the application..."
nohup python app.py > app.log 2>&1 &

log "Deployment completed successfully."
