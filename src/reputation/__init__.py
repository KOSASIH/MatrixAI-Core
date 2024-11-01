# reputation/__init__.py

import logging
import os
import json

# Set up logging for the reputation module
def setup_logging(log_file='reputation.log', log_level=logging.INFO):
    """Set up logging configuration."""
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    logging.info("Logging initialized.")

# Load configuration from a JSON file
def load_config(config_file='config.json'):
    """Load configuration settings from a JSON file."""
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
            logging.info("Configuration loaded from %s.", config_file)
            return config
    else:
        logging.warning("Configuration file %s not found. Using default settings.", config_file)
        return {}

# Initialize the reputation module
def initialize_reputation_module(config_file='config.json'):
    """Initialize the reputation module with logging and configuration."""
    setup_logging()
    config = load_config(config_file)
    logging.info("Reputation module initialized with version %s.", __version__)
    return config

__version__ = "1.0.0"

# Example of a function to validate configuration settings
def validate_config(config):
    """Validate the loaded configuration settings."""
    required_keys = ['default_algorithm', 'log_level']
    for key in required_keys:
        if key not in config:
            logging.error("Missing required configuration key: %s", key)
            raise ValueError(f"Missing required configuration key: {key}")
    logging.info("Configuration validated successfully.")

# Example of a function to set default values for configuration
def set_default_config():
    """Set default configuration values."""
    default_config = {
        'default_algorithm': 'SimpleAverageScore',
        'log_level': 'INFO'
    }
    with open('config.json', 'w') as f:
        json.dump(default_config, f, indent=4)
    logging.info("Default configuration created.")

# Check if the config file exists, if not create it
if not os.path.exists('config.json'):
    set_default_config()
