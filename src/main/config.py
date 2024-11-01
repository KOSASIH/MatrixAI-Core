# src/main/config.py

import os

class Config:
    """Base configuration settings for the application."""
    
    # General settings
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key_here')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
    
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///matrixai.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable track modifications for performance

    # API settings
    API_VERSION = os.getenv('API_VERSION', 'v1')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Limit request size to 16 MB

    # CORS settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')  # Allow all origins by default

class DevelopmentConfig(Config):
    """Development configuration settings."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URI', 'sqlite:///dev_matrixai.db')

class TestingConfig(Config):
    """Testing configuration settings."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URI', 'sqlite:///test_matrixai.db')

class ProductionConfig(Config):
    """Production configuration settings."""
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///matrixai.db')

# Configuration selection based on environment variable
config_type = os.getenv('FLASK_ENV', 'development').lower()
if config_type == 'production':
    Config = ProductionConfig
elif config_type == 'testing':
    Config = TestingConfig
else:
    Config = DevelopmentConfig
