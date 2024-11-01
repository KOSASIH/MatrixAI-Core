// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts/utils/Strings.sol";

contract MySmartContract is Ownable, Initializable {
    using Strings for uint256;

    event ValueChanged(uint256 indexed oldValue, uint256 indexed newValue);
    event ContractUpgraded(address indexed newImplementation);

    uint256 private value;

    // Optional: Store a version number for the contract
    string public version;

    // Optional: Mapping to store additional data
    mapping(address => uint256) public balances;

    // Initializer function for upgradable contracts
    function initialize(uint256 initialValue, string memory contractVersion) public initializer {
        value = initialValue;
        version = contractVersion;
    }

    function setValue(uint256 newValue) public onlyOwner {
        uint256 oldValue = value;
        value = newValue;
        emit ValueChanged(oldValue, newValue);
    }

    function getValue() public view returns (uint256) {
        return value;
    }

    function deposit() public payable {
        require(msg.value > 0, "Must send ETH to deposit");
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint256 amount) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        balances[msg.sender] -= amount;
        payable(msg.sender).transfer(amount);
    }

    function getBalance() public view returns (uint256) {
        return balances[msg.sender];
    }

    // Function to upgrade the contract (for demonstration purposes)
    function upgradeContract(address newImplementation) public onlyOwner {
        require(newImplementation != address(0), "Invalid address");
        emit ContractUpgraded(newImplementation);
        // Logic to upgrade the contract would go here (e.g., using a proxy pattern)
    }

    // Utility function to get the contract version
    function getVersion() public view returns (string memory) {
        return version;
    }
}
