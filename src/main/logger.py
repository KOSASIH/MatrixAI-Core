# src/main/logger.py

import logging
import os
import sys
from logging.handlers import RotatingFileHandler, SMTPHandler

def setup_logging():
    """Set up logging configuration with advanced features."""
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    
    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Create console handler for output to stdout
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Create file handler for logging to a file
    file_handler = RotatingFileHandler('matrixai.log', maxBytes=10*1024*1024, backupCount=5)
    file_handler.setLevel(log_level)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Optional: Email notifications for critical errors
    if os.getenv('MAIL_SERVER'):
        mail_handler = SMTPHandler(
            mailhost=(os.getenv('MAIL_SERVER'), int(os.getenv('MAIL_PORT', 25))),
            fromaddr=os.getenv('MAIL_FROM'),
            toaddrs=os.getenv('MAIL_TO').split(','),
            subject='Critical Error in MatrixAI-Core',
            credentials=(os.getenv('MAIL_USERNAME'), os.getenv('MAIL_PASSWORD')),
            secure=None
        )
        mail_handler.setLevel(logging.ERROR)
        mail_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s\n%(message)s')
        mail_handler.setFormatter(mail_formatter)
        logger.addHandler(mail_handler)

    logging.info("Logging is set up with level: %s", log_level)

# Example usage of the logger
if __name__ == "__main__":
    setup_logging()
    logging.info("Logger is set up and ready to use.")
