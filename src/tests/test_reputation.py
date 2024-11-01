# src/tests/test_reputation.py

import pytest
from src.core.reputation import ReputationManager, UserNotFoundError

@pytest.fixture
def reputation_manager():
    """Fixture to create an instance of ReputationManager for testing."""
    return ReputationManager()

def test_initialize_reputation(reputation_manager):
    """Test initializing a user's reputation."""
    user_id = "user_123"
    reputation_manager.initialize_reputation(user_id)
    assert reputation_manager.get_reputation(user_id) == 0

def test_update_reputation_positive(reputation_manager):
    """Test updating a user's reputation positively."""
    user_id = "user_123"
    reputation_manager.initialize_reputation(user_id)
    reputation_manager.update_reputation(user_id, 10)
    assert reputation_manager.get_reputation(user_id) == 10

def test_update_reputation_negative(reputation_manager):
    """Test updating a user's reputation negatively."""
    user_id = "user_123"
    reputation_manager.initialize_reputation(user_id)
    reputation_manager.update_reputation(user_id, -5)
    assert reputation_manager.get_reputation(user_id) == -5

def test_update_reputation_multiple_updates(reputation_manager):
    """Test multiple updates to a user's reputation."""
    user_id = "user_123"
    reputation_manager.initialize_reputation(user_id)
    reputation_manager.update_reputation(user_id, 10)
    reputation_manager.update_reputation(user_id, -3)
    reputation_manager.update_reputation(user_id, 5)
    assert reputation_manager.get_reputation(user_id) == 12  # 10 - 3 + 5

def test_get_reputation_user_not_found(reputation_manager):
    """Test getting reputation for a non-existent user."""
    with pytest.raises(UserNotFoundError):
        reputation_manager.get_reputation("non_existent_user")

def test_initialize_reputation_already_exists(reputation_manager):
    """Test initializing reputation for a user that already exists."""
    user_id = "user_123"
    reputation_manager.initialize_reputation(user_id)
    with pytest.raises(ValueError):
        reputation_manager.initialize_reputation(user_id)

def test_update_reputation_user_not_found(reputation_manager):
    """Test updating reputation for a non-existent user."""
    with pytest.raises(UserNotFoundError):
        reputation_manager.update_reputation("non_existent_user", 10)

def test_reputation_bounds(reputation_manager):
    """Test that reputation does not exceed defined bounds."""
    user_id = "user_123"
    reputation_manager.initialize_reputation(user_id)
    reputation_manager.update_reputation(user_id, 100)  # Assuming max reputation is 100
    assert reputation_manager.get_reputation(user_id) <= 100

    reputation_manager.update_reputation(user_id, -200)  # Assuming min reputation is -100
    assert reputation_manager.get_reputation(user_id) >= -100
