# src/main/__init__.py

"""
MatrixAI-Core Main Package

This package serves as the core of the MatrixAI decentralized trust verification system.
It includes the main application logic, configuration settings, logging utilities, and
API endpoints for user identity verification, risk assessment, and reputation management.

Version: 0.2.0
Author: Your Name
Email: your-email@example.com
License: MIT
"""

import os
import logging

# Package metadata
__version__ = "0.2.0"
__author__ = "Your Name"
__email__ = "your-email@example.com"
__license__ = "MIT"

# Set up advanced logging
def setup_logging():
    """Set up logging configuration with advanced features."""
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('matrixai.log'),
            logging.handlers.RotatingFileHandler(
                'matrixai_rotating.log', maxBytes=10*1024*1024, backupCount=5
            )
        ]
    )
    logging.info("Logging is set up with level: %s", log_level)

# Initialize logging
setup_logging()

# Import application components
from .app import app  # Import the Flask app
from .config import Config  # Import configuration settings
from .logger import setup_logging  # Import logging setup

# Initialize the application
def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)
    setup_logging()
    return app

# Initialize the application instance
app = create_app()
