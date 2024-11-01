# src/core/identity/identity_manager.py

import logging
from .cryptography import Cryptography
from .token_manager import TokenManager
from .user_roles import UserRoles

class IdentityManager:
    """Class to manage identity verification and user management."""

    def __init__(self):
        self.cryptography = Cryptography()
        self.token_manager = TokenManager()
        self.user_roles = UserRoles()
        self.users = {}  # In-memory user storage for demonstration

    def register_user(self, username, password):
        """Register a new user with encrypted password."""
        if username in self.users:
            logging.warning("User  already exists: %s", username)
            return {"error": "User  already exists"}, 409

        password_hash = self.cryptography.hash_password(password)
        self.users[username] = {
            "password_hash": password_hash,
            "verified": False,
            "role": None  # Role will be assigned later
        }
        logging.info("User  registered: %s", username)
        return {"message": "User  registered successfully"}, 201

    def verify_user(self, username, password):
        """Verify user credentials."""
        user = self.users.get(username)
        if not user:
            logging.warning("User  not found: %s", username)
            return {"error": "User  not found"}, 404

        if self.cryptography.verify_password(password, user["password_hash"]):
            user["verified"] = True
            logging.info("User  verified: %s", username)
            return {"message": "User  verified successfully"}, 200
        else:
            logging.warning("Invalid password for user: %s", username)
            return {"error": "Invalid password"}, 401

    def assign_role(self, username, role):
        """Assign a role to a user."""
        if username not in self.users:
            logging.warning("User  not found: %s", username)
            return {"error": "User  not found"}, 404

        try:
            self.user_roles.assign_role(username, role)
            self.users[username]["role"] = role
            logging.info("Role '%s' assigned to user: %s", role, username)
            return {"message": f"Role '{role}' assigned to user '{username}'."}, 200
        except ValueError as e:
            logging.error("Error assigning role: %s", str(e))
            return {"error": str(e)}, 400

    def generate_token(self, username):
        """Generate a JWT token for a user."""
        if username not in self.users or not self.users[username]["verified"]:
            logging.warning("Cannot generate token for unverified user: %s", username)
            return {"error": "User  not verified"}, 403

        token = self.token_manager.generate_token(username)
        logging.info("Token generated for user: %s", username)
        return {"token": token}, 200

    def is_user_verified(self, username):
        """Check if the user is verified."""
        user = self.users.get(username)
        if user and user["verified"]:
            return True
        return False

    def get_user_role(self, username):
        """Get the role of a user."""
        user = self.users.get(username)
        if user:
            return user.get("role", "No role assigned")
        return None
