# examples/example_identity.py

from src.identity import IdentityManager, UserAlreadyExistsError, UserNotFoundError

def main():
    # Create an instance of IdentityManager
    identity_manager = IdentityManager()

    # Example: User Registration
    try:
        user_id = identity_manager.register_user("john_doe", "password123", "john@example.com")
        print(f"User  registered successfully with ID: {user_id}")
    except UserAlreadyExistsError as e:
        print(f"Registration failed: {e}")

    # Example: User Authentication
    try:
        user = identity_manager.authenticate_user("john_doe", "password123")
        print(f"User  authenticated successfully: {user}")
    except UserNotFoundError as e:
        print(f"Authentication failed: {e}")

    # Example: Fetch User Profile
    try:
        profile = identity_manager.get_user_profile(user_id)
        print(f"User  Profile: {profile}")
    except UserNotFoundError as e:
        print(f"Profile retrieval failed: {e}")

if __name__ == "__main__":
    main()
