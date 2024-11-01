# src/core/smart_contracts/__init__.py

import logging
from .deployment import deploy_contract, compile_contract
from .contract import MySmartContract

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

__all__ = ['deploy_contract', 'compile_contract', 'MySmartContract']

class SmartContractManager:
    """Manager for deploying and interacting with smart contracts."""

    def __init__(self, web3_instance, contract_interface):
        self.web3 = web3_instance
        self.contract_interface = contract_interface
        self.contract_instance = None

    def deploy(self, initial_value: int):
        """Deploy the smart contract."""
        try:
            contract_address = deploy_contract(self.web3, self.contract_interface, initial_value)
            self.contract_instance = self.web3.eth.contract(address=contract_address, abi=self.contract_interface['abi'])
            logger.info(f"Smart contract deployed at address: {contract_address}")
            return contract_address
        except Exception as e:
            logger.error(f"Failed to deploy contract: {str(e)}")
            raise

    def set_value(self, new_value: int):
        """Set a new value in the smart contract."""
        if not self.contract_instance:
            logger.error("Contract instance is not initialized. Please deploy the contract first.")
            return

        try:
            account = self.web3.eth.accounts[0]
            transaction = self.contract_instance.functions.setValue(new_value).buildTransaction({
                'chainId': 1,  # Mainnet
                'gas': 200000,
                'gasPrice': self.web3.toWei('50', 'gwei'),
                'nonce': self.web3.eth.getTransactionCount(account),
            })

            signed_txn = self.web3.eth.account.signTransaction(transaction, private_key=os.getenv("PRIVATE_KEY"))
            tx_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
            tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)

            logger.info(f"Value set to {new_value}. Transaction receipt: {tx_receipt}")
        except Exception as e:
            logger.error(f"Failed to set value: {str(e)}")
            raise

    def get_value(self):
        """Get the current value from the smart contract."""
        if not self.contract_instance:
            logger.error("Contract instance is not initialized. Please deploy the contract first.")
            return None

        try:
            current_value = self.contract_instance.functions.getValue().call()
            logger.info(f"Current value retrieved: {current_value}")
            return current_value
        except Exception as e:
            logger.error(f"Failed to retrieve value: {str(e)}")
            return None

# Example usage
if __name__ == "__main__":
    from web3 import Web3
    from dotenv import load_dotenv
    import os

    # Load environment variables
    load_dotenv()

    # Connect to the Ethereum network
    w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"))

    # Compile the contract
    contract_interface = compile_contract()

    # Initialize the SmartContractManager
    manager = SmartContractManager(w3, contract_interface)

    # Deploy the contract with an initial value
    initial_value = 100
    manager.deploy(initial_value)

    # Set a new value
    manager.set_value(200)

    # Get the current value
    current_value = manager.get_value()
