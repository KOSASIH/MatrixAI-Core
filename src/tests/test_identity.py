# src/tests/test_identity.py

import pytest
from src.core.identity import IdentityManager, UserAlreadyExistsError, UserNotFoundError, InvalidCredentialsError

@pytest.fixture
def identity_manager():
    """Fixture to create an instance of IdentityManager for testing."""
    return IdentityManager()

def test_register_user(identity_manager):
    """Test user registration."""
    user_id = identity_manager.register_user("test_user", "password123")
    assert user_id is not None
    user = identity_manager.get_user(user_id)
    assert user["username"] == "test_user"
    assert user["user_id"] == user_id

def test_register_user_already_exists(identity_manager):
    """Test registering a user that already exists."""
    identity_manager.register_user("test_user", "password123")
    with pytest.raises(UserAlreadyExistsError):
        identity_manager.register_user("test_user", "password123")

def test_authenticate_user_success(identity_manager):
    """Test successful user authentication."""
    identity_manager.register_user("test_user", "password123")
    assert identity_manager.authenticate("test_user", "password123") is True

def test_authenticate_user_failure(identity_manager):
    """Test authentication failure with wrong password."""
    identity_manager.register_user("test_user", "password123")
    assert identity_manager.authenticate("test_user", "wrong_password") is False

def test_authenticate_user_not_found(identity_manager):
    """Test authentication for a non-existent user."""
    with pytest.raises(UserNotFoundError):
        identity_manager.authenticate("non_existent_user", "password123")

def test_get_user(identity_manager):
    """Test retrieving user information."""
    user_id = identity_manager.register_user("test_user", "password123")
    user = identity_manager.get_user(user_id)
    assert user["username"] == "test_user"
    assert user["user_id"] == user_id

def test_get_user_not_found(identity_manager):
    """Test retrieving a non-existent user."""
    with pytest.raises(UserNotFoundError):
        identity_manager.get_user("non_existent_user_id")

def test_change_password(identity_manager):
    """Test changing a user's password."""
    identity_manager.register_user("test_user", "password123")
    identity_manager.change_password("test_user", "new_password123")
    assert identity_manager.authenticate("test_user", "new_password123") is True
    assert identity_manager.authenticate("test_user", "password123") is False

def test_change_password_user_not_found(identity_manager):
    """Test changing password for a non-existent user."""
    with pytest.raises(UserNotFoundError):
        identity_manager.change_password("non_existent_user", "new_password123")

def test_change_password_invalid_credentials(identity_manager):
    """Test changing password with invalid current password."""
    identity_manager.register_user("test_user", "password123")
    with pytest.raises(InvalidCredentialsError):
        identity_manager.change_password("test_user", "wrong_password")
