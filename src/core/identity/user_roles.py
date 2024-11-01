# src/core/identity/user_roles.py

class UserRoles:
    """Class for managing user roles and permissions."""

    ROLES = {
        'admin': 'Administrator with full access',
        'editor': 'User with editing permissions',
        'viewer': 'User with read-only access'
    }

    def __init__(self):
        self.user_roles = {}  # In-memory storage for user roles

    def assign_role(self, username, role):
        """Assign a role to a user."""
        if role not in self.ROLES:
            raise ValueError("Invalid role specified.")
        self.user_roles[username] = role
        return {"message": f"Role '{role}' assigned to user '{username}'."}

    def get_user_role(self, username):
        """Get the role of a user."""
        return self.user_roles.get(username, "No role assigned")

    def has_permission(self, username, permission):
        """Check if a user has a specific permission."""
        role = self.get_user_role(username)
        if role == 'admin':
            return True  # Admin has all permissions
        elif role == 'editor' and permission in ['edit', 'view']:
            return True
        elif role == 'viewer' and permission == 'view':
            return True
        return False
