# src/tests/test_smart_contracts.py

import pytest
from src.core.smart_contracts import SmartContractManager, ContractNotFoundError, InvalidContractError

@pytest.fixture
def contract_manager():
    """Fixture to create an instance of SmartContractManager for testing."""
    return SmartContractManager()

def test_deploy_contract(contract_manager):
    """Test deploying a new smart contract."""
    contract_code = "function test() { return true; }"
    contract_id = contract_manager.deploy_contract(contract_code)
    assert contract_id is not None
    assert contract_manager.get_contract(contract_id)["code"] == contract_code

def test_deploy_invalid_contract(contract_manager):
    """Test deploying an invalid smart contract."""
    invalid_contract_code = "invalid code"
    with pytest.raises(InvalidContractError):
        contract_manager.deploy_contract(invalid_contract_code)

def test_execute_contract(contract_manager):
    """Test executing a deployed smart contract."""
    contract_code = "function test() { return true; }"
    contract_id = contract_manager.deploy_contract(contract_code)
    result = contract_manager.execute_contract(contract_id, "test")
    assert result is True

def test_execute_non_existent_contract(contract_manager):
    """Test executing a non-existent smart contract."""
    with pytest.raises(ContractNotFoundError):
        contract_manager.execute_contract("non_existent_contract_id", "test")

def test_get_contract(contract_manager):
    """Test retrieving a deployed smart contract."""
    contract_code = "function test() { return true; }"
    contract_id = contract_manager.deploy_contract(contract_code)
    contract = contract_manager.get_contract(contract_id)
    assert contract["id"] == contract_id
    assert contract["code"] == contract_code

def test_get_non_existent_contract(contract_manager):
    """Test retrieving a non-existent smart contract."""
    with pytest.raises(ContractNotFoundError):
        contract_manager.get_contract("non_existent_contract_id")

def test_update_contract(contract_manager):
    """Test updating an existing smart contract."""
    contract_code = "function test() { return true; }"
    contract_id = contract_manager.deploy_contract(contract_code)
    new_contract_code = "function test() { return false; }"
    contract_manager.update_contract(contract_id, new_contract_code)
    assert contract_manager.get_contract(contract_id)["code"] == new_contract_code

def test_update_non_existent_contract(contract_manager):
    """Test updating a non-existent smart contract."""
    with pytest.raises(ContractNotFoundError):
        contract_manager.update_contract("non_existent_contract_id", "new code")

def test_execute_contract_with_invalid_function(contract_manager):
    """Test executing a contract with an invalid function name."""
    contract_code = "function test() { return true; }"
    contract_id = contract_manager.deploy_contract(contract_code)
    with pytest.raises(ValueError):
        contract_manager.execute_contract(contract_id, "non_existent_function")
