#!/bin/bash

# run_tests.sh - Script to run all tests

set -e  # Exit immediately if a command exits with a non-zero status

# Define variables
TEST_DIR="src/tests"  # Directory containing tests
LOG_FILE="test_results.log"  # Log file for test results

# Function to log messages
log() {
    echo "$(date +'%Y-%m-%d %H:%M:%S') - $1"
}

log "Running tests..."

# Activate the virtual environment
if [ -d "venv" ]; then
    source "venv/bin/activate"
else
    log "Virtual environment not found. Please run setup_environment.sh first."
    exit 1
fi

# Run tests and log results
pytest "$TEST_DIR" > "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    log "All tests passed successfully."
else
    log "Some tests failed. Check the log file for details: $LOG_FILE"
    exit 1
fi
