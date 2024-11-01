# src/core/identity/cryptography.py

import bcrypt
import os
import logging
from hashlib import pbkdf2_hmac

class Cryptography:
    """Class for cryptographic functions."""

    def __init__(self):
        self.salt_length = 16  # Length of the salt
        self.iterations = 100000  # Number of iterations for PBKDF2
        self.hash_algorithm = 'sha256'  # Hash algorithm for PBKDF2

    def generate_salt(self):
        """Generate a random salt."""
        salt = os.urandom(self.salt_length)
        return salt

    def hash_password(self, password):
        """Hash a password using bcrypt and PBKDF2."""
        if not password:
            logging.error("Password cannot be empty.")
            raise ValueError("Password cannot be empty.")

        # Generate a salt
        salt = self.generate_salt()
        # Hash the password using PBKDF2
        password_hash = pbkdf2_hmac(
            self.hash_algorithm,
            password.encode('utf-8'),
            salt,
            self.iterations
        )
        # Combine salt and hash for storage
        hashed_password = salt + password_hash
        logging.info("Password hashed successfully.")
        return hashed_password

    def verify_password(self, password, hashed):
        """Verify a password against a hashed password."""
        if not hashed:
            logging.error("Hashed password cannot be empty.")
            raise ValueError("Hashed password cannot be empty.")

        # Extract the salt from the stored hash
        salt = hashed[:self.salt_length]
        stored_hash = hashed[self.salt_length:]

        # Hash the provided password with the extracted salt
        password_hash = pbkdf2_hmac(
            self.hash_algorithm,
            password.encode('utf-8'),
            salt,
            self.iterations
        )

        if password_hash == stored_hash:
            logging.info("Password verification successful.")
            return True
        logging.warning("Password verification failed.")
        return False

    def hash_with_bcrypt(self, password):
        """Hash a password using bcrypt."""
        if not password:
            logging.error("Password cannot be empty.")
            raise ValueError("Password cannot be empty.")

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        logging.info("Password hashed with bcrypt successfully.")
        return hashed.decode('utf-8')

    def verify_with_bcrypt(self, password, hashed):
        """Verify a password against a bcrypt hashed password."""
        if bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8')):
            logging.info("Password verification with bcrypt successful.")
            return True
        logging.warning("Password verification with bcrypt failed.")
        return False
