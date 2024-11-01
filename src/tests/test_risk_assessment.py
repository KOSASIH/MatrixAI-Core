# src/tests/test_risk_assessment.py

import pytest
from src.core.risk_assessment import RiskAssessment, InvalidUser DataError

@pytest.fixture
def risk_assessment():
    """Fixture to create an instance of RiskAssessment for testing."""
    return RiskAssessment()

def test_assess_low_risk(risk_assessment):
    """Test assessing a user with low risk."""
    user_data = {"credit_score": 750, "transaction_history": "good"}
    risk = risk_assessment.assess(user_data)
    assert risk == "low"

def test_assess_medium_risk(risk_assessment):
    """Test assessing a user with medium risk."""
    user_data = {"credit_score": 650, "transaction_history": "average"}
    risk = risk_assessment.assess(user_data)
    assert risk == "medium"

def test_assess_high_risk(risk_assessment):
    """Test assessing a user with high risk."""
    user_data = {"credit_score": 500, "transaction_history": "poor"}
    risk = risk_assessment.assess(user_data)
    assert risk == "high"

def test_assess_invalid_user_data(risk_assessment):
    """Test assessing with invalid user data."""
    invalid_user_data = {"credit_score": "not_a_number", "transaction_history": "good"}
    with pytest.raises(InvalidUser DataError):
        risk_assessment.assess(invalid_user_data)

def test_assess_missing_credit_score(risk_assessment):
    """Test assessing a user with missing credit score."""
    user_data = {"transaction_history": "good"}
    with pytest.raises(InvalidUser DataError):
        risk_assessment.assess(user_data)

def test_assess_missing_transaction_history(risk_assessment):
    """Test assessing a user with missing transaction history."""
    user_data = {"credit_score": 700}
    with pytest.raises(InvalidUser DataError):
        risk_assessment.assess(user_data)

def test_assess_edge_case_high_credit_score(risk_assessment):
    """Test assessing a user with an edge case high credit score."""
    user_data = {"credit_score": 850, "transaction_history": "excellent"}
    risk = risk_assessment.assess(user_data)
    assert risk == "low"

def test_assess_edge_case_low_credit_score(risk_assessment):
    """Test assessing a user with an edge case low credit score."""
    user_data = {"credit_score": 300, "transaction_history": "very poor"}
    risk = risk_assessment.assess(user_data)
    assert risk == "high"
