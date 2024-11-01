# src/core/identity/token_manager.py

import jwt
import datetime
import logging
from flask import current_app

class TokenManager:
    """Class for managing JWT tokens."""

    def __init__(self):
        self.secret_key = current_app.config['SECRET_KEY']
        self.algorithm = 'HS256'
        self.expiration_time = 3600  # Token expiration time in seconds (1 hour)

    def generate_token(self, username):
        """Generate a JWT token for a user."""
        expiration = datetime.datetime.utcnow() + datetime.timedelta(seconds=self.expiration_time)
        token = jwt.encode({
            'sub': username,
            'exp': expiration
        }, self.secret_key, algorithm=self.algorithm)
        logging.info("Token generated for user: %s", username)
        return token

    def verify_token(self, token):
        """Verify a JWT token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            logging.info("Token verified successfully for user: %s", payload['sub'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            logging.warning("Token has expired.")
            return None
        except jwt.InvalidTokenError:
            logging.warning("Invalid token.")
            return None
